from Engine.BaseTraderEngine import *
from Engine.Engine_Y.util import *


class TraderEngine_SMA(BaseTraderEngine):
    """윤동진 엔진

    :ivar dict params: Parameter
    :ivar Client client: 투자자 상태
    :ivar dict raw_datas: 데이터
    """
    def get_portfolio(self, trading_date):
        """다음 시간의 포트폴리오를 선택

        :param Timestamp trading_date: 거래 날짜
        :return: 포트폴리오
        :rtype: :class:`Trader.Portfolio`
        """
        ## 월요일에만 거래
        if trading_date.weekday() != 0:
            return Portfolio(self.client.portfolio.get_holding_dic(), trading_date)

        ## 1. 학습 데이터 선택
        datas      = self.select_datas(trading_date)
        stock_data = datas['stock']

        ## 2. 각 종목에 대하여 포지션 결정(long, short)
        dic = {}
        symbols = stock_data.loc[stock_data.index[-1]].sort_values(by='cap', ascending=False).symbol
        for symbol in [symbols[i] for i in range(5)]:
            cur_data = self.generate_MA(stock_data, symbol)
            if pd.isnull(cur_data['SMA2']):  # 데이터 부족은 패스
                continue

            ## 2.1 포지션 결정
            position = 'long' if cur_data['SMA1'] > cur_data['SMA2'] else 'short'

            ## 3. 포트폴리오 생성
            num = self.client.portfolio.get_holding_ser().get(symbol, 0)
            if position == 'long':
                num = num + 1
            else:
                num = num - 1 if num > 0 else 0
            if num > 0:
                dic[symbol] = num

        return Portfolio(dic, trading_date)

    def generate_MA(self, stock_data, symbol):
        """``symbol`` 종가에 대한 SMA 데이터 생성
        
        :param cudf.DataFrame stock_data: 주가 데이터
        :param str symbol: 종목 코드
        :return: SMA 데이터
        :rtype: dict
        """
        ## 2. Index ETF(KODEX200) 선택
        prices = stock_data[stock_data.symbol == symbol].close.iloc[-252:]
        return {'SMA1': prices.rolling(42).mean()[-1],
                'SMA2': prices.rolling(252).mean()[-1]}
