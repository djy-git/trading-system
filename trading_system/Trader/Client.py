from Trader.Portfolio import *
from collections import Counter


class Client:
    """투자자의 상태를 관리하는 class

    :param dict params: parameters
    :param dict datas: 데이터
    :param Timestamp updating_date: 최신 투자 날짜
    
    :ivar dict params: parameters
    :ivar dict datas: 데이터
    :ivar Timestamp updating_date: 최신 투자 날짜
    :ivar Portfolio portfolio: 포트폴리오
    :ivar int balance: 현금자산(잔고)
    :ivar float net_wealth: 순자산
    """
    def __init__(self, params, datas):
        self.params        = params
        self.datas         = datas
        self.updating_date = None
        self.initialize()

    def initialize(self):
        """투자자의 상태를 초기화"""
        self.portfolio  = Portfolio()
        self.balance    = self.params['BALANCE']
        self.net_wealth = self.balance
        
    def update_net_wealth(self):
        """투자자의 총 자산을 계산"""
        ## 1. 잔고
        new_net_wealth = self.params['BALANCE']

        ## 2. 주식
        data = self.portfolio.get_data_by_date(self.updating_date)
        for symbol, num in data.itertuples(index=False):
            new_net_wealth += num * self.get_price(symbol, self.updating_date)

        self.net_wealth = new_net_wealth

    def get_price(self, symbol, date):
        """주식의 가격을 가져옴

        :param str symbol: 주식의 종목명
        :param Timestamp date: 주식의 가격을 가져올 날짜
        :return: 주식의 가격
        :rtype: float
        """
        return self.datas['stock'].loc[date].query("symbol == @symbol").close[0]

    def trade(self, portfolio):
        """포트폴리오를 거래

        :param Portfolio portfolio: 투자 포트폴리오
        """
        ## 1. 투자 날짜 갱신
        self.updating_date = portfolio.get_latest_date()

        ## 2. 매도 후 매수 수행 (잔고 부족 방지)
        # sell(), buy()에서 self.portfolio가 변해도 df2dict()는 deepcopy 객체를 반환
        port_dict, port_dict_hold = portfolio.df2dict(), self.portfolio.df2dict()
        self.sell(port_dict, port_dict_hold)
        self.buy(port_dict, port_dict_hold)

        ## 3. 잔고 갱신
        self.update_net_wealth()

    def sell(self, port_dict, port_dict_hold):
        """자산을 매도

        :param dict port_dict: 투자 포트폴리오
        :param dict port_dict_hold: 보유 포트폴리오
        """
        ## 1. 매도 자산 선택
        sell_data = -(Counter(port_dict) - Counter(port_dict_hold))

        ## 2. 매도 수행
        for symbol, num in sell_data.items():
            self.balance += num * self.get_price(symbol, self.updating_date)
            self.portfolio.add({symbol: portfolio.df2dict()['symbol']}, self.updating_date)

    def buy(self, port_dict, port_dict_hold):
        """자산을 매수

        :param dict port_dict: 투자 포트폴리오
        :param dict port_dict_hold: 보유 포트폴리오
        """
        ## 1. 매수 자산 선택
        buy_data = +(Counter(port_dict) - Counter(port_dict_hold))

        ## 2. 매도 수행
        for symbol, num in buy_data.items():
            price = num * self.get_price(symbol, self.updating_date)
            if price < self.balance:
                self.balance -= price
                self.portfolio.add({symbol: port_dict[symbol]}, self.updating_date)
            else:
                LOGGER.info(f"{symbol}: {num} 매수 실패 (잔고 부족, 잔고: {self.balance}, 가격: {price})")
