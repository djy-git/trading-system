from Trader.Portfolio import *
from collections import Counter


class Client:
    """투자자의 상태를 관리하는 class

    :param dict params: parameters
    :param dict raw_datas: 데이터
    :param Timestamp updating_date: 최신 투자 날짜
    
    :ivar dict params: parameters
    :ivar dict raw_datas: 데이터
    :ivar Timestamp updating_date: 최신 투자 날짜
    :ivar Portfolio portfolio: 포트폴리오
    :ivar float balance: 현금자산(잔고)
    :ivar float stock_wealth: 주식 평가액
    :ivar float net_wealth: 순자산
    """
    def __init__(self, params, raw_datas):
        self.params    = params
        self.raw_datas = raw_datas
        self.initialize()
    def initialize(self):
        """투자자의 상태를 초기화"""
        self.updating_date = None
        self.portfolio     = Portfolio()
        self.balance       = self.params['BALANCE']
        self.stock_wealth  = 0
        self.net_wealth    = self.balance

    def trade(self, portfolio):
        """포트폴리오를 거래

        :param Portfolio portfolio: 투자 포트폴리오
        """
        ## 1. 투자 날짜, 주식 평가액 갱신
        self.updating_date = portfolio.latest_date
        self.stock_wealth  = 0

        ## 2. 매수, 매도 판단
        # sell(), buy()에서 self.portfolio가 변해도 df2dict()는 deepcopy 객체를 반환
        port_dict, port_dict_hold = portfolio.get_holding_ser().to_dict(), self.portfolio.get_holding_ser().to_dict()
        port_cnt, port_cnt_hold   = Counter(port_dict), Counter(port_dict_hold)
        port_cnt.subtract(port_cnt_hold)
        port_cnt_diff = port_cnt
        
        ## 3. 매도 후 매수 수행 (잔고 부족 방지)
        self.sell(-port_cnt_diff, port_dict_hold)
        self.buy(+port_cnt_diff, port_dict_hold)
        self.hold(port_dict, port_dict_hold)
    def sell(self, port_cnt_sell, port_dict_hold):
        """자산을 매도

        :param Counter port_cnt_sell: 매도 포트폴리오
        :param dict port_dict_hold: 보유 포트폴리오
        """
        ## 1. 매도 수행
        for symbol, num in port_cnt_sell.items():
            if price := get_price(self.raw_datas['stock'], symbol, self.updating_date):
                price_sell       = num * price
                transaction_cost = price_sell * (TAX_RATE_KR + FEE_RATE_KR)
                if transaction_cost <= self.balance:
                    if (num_hold := port_dict_hold.get(symbol, 0) - num) > 0:
                        ## Success case
                        self.add_portfolio({symbol: num_hold}, self.updating_date, transaction_cost, price_sell=price_sell)
                        continue
                    else:
                        ## Failure case 1
                        msg_fail = f"보유 주식 수 부족 (보유 주식 수: {port_dict_hold.get(symbol, 0)}개, 매도 주식 수: {num})"
                else:
                    ## Failure case 2
                    msg_fail = f"잔고 부족 (잔고: {self.balance:,.0f}, 거래비용: {transaction_cost:,.0f})"
            else:
                ## Failure case 3
                msg_fail = "거래 데이터 없음"

            ## Failure case
            LOGGER.info(f"[{self.updating_date} {symbol} 매도 실패] {msg_fail}")
            self.add_portfolio({symbol: port_dict_hold[symbol]}, self.updating_date)
    def buy(self, port_cnt_buy, port_dict_hold):
        """자산을 매수

        :param Counter port_cnt_buy: 매수 포트폴리오
        :param dict port_dict_hold: 보유 포트폴리오
        """
        ## 1. 매도 수행
        for symbol, num in port_cnt_buy.items():
            if price := get_price(self.raw_datas['stock'], symbol, self.updating_date):
                price_buy        = num * price
                transaction_cost = price_buy * FEE_RATE_KR
                if price_buy + transaction_cost <= self.balance:
                    ## Success case
                    self.add_portfolio({symbol: port_dict_hold.get(symbol, 0) + num}, self.updating_date, transaction_cost, price_buy=price_buy)
                    continue
                else:
                    ## Failure case 1
                    msg_fail = f"잔고 부족 (잔고: {self.balance:,.0f}, 가격: {price_buy:,.0f} = {num:,d}주 x {price:,.0f}, 거래비용: {transaction_cost:,.0f})"
            else:
                ## Failure case 2
                msg_fail = "거래 데이터 없음"

            ## Failure case
            LOGGER.info(f"[{self.updating_date} {symbol} 매수 실패] {msg_fail}")
            if symbol in port_dict_hold:
                self.add_portfolio({symbol: port_dict_hold[symbol]}, self.updating_date)
    def hold(self, port_dict, port_dict_hold):
        """자산을 유지
        
        :param dict port_dict: 투자 포트폴리오
        :param dict port_dict_hold: 보유 포트폴리오
        """
        ## 1. 보유 유지
        port_dict_no_diff = {symbol: num for symbol, num in port_dict.items() if num == port_dict_hold.get(symbol)}
        if len(port_dict_no_diff) > 0:
            self.add_portfolio(port_dict_no_diff, self.updating_date)
    def add_portfolio(self, dic, date, transaction_cost=None, price_buy=None, price_sell=None):
        """포트폴리오 추가 및 순자산 갱신
        
        :param dict dic: 추가할 포트폴리오
        :param Timestamp date: 투자 날짜
        :param float transaction_cost: 거래비용, default=None
        :param float price_buy: 매수금액, default=None
        :param float price_sell: 매도금액, default=None
        """
        ## 1. 포트폴리오 추가
        self.portfolio.add(dic, date)

        ## 2. 순자산 갱신
        if transaction_cost is not None:
            ## 2.1 거래 발생
            self.balance -= transaction_cost
            if price_buy is not None:
                self.balance -= price_buy
            else:
                self.balance += price_sell

        ## 2.2 순자산 갱신
        for symbol, num in dic.items():
            self.stock_wealth += num * get_price(self.raw_datas['stock'], symbol, date, nearest=True)
        self.net_wealth = self.balance + self.stock_wealth
