from Engine.BaseTraderEngine import *
from Engine.Engine_Y.util import *
from Trader.Portfolio import *


class TraderEngine_SMA(BaseTraderEngine):
    """윤동진 엔진

    :param dict params: parameters
    :ivar dict raw_datas: raw datas
    """
    def __init__(self, params, client):
        super().__init__(params, client)
        self.raw_datas = get_raw_datas()

    def get_portfolio(self, trading_date):
        """다음 시간의 포트폴리오를 선택

        :param Timestamp trading_date: 거래 날짜
        :return: 포트폴리오
        :rtype: :class:`Trader.Portfolio`
        """
        ## 1. 데이터 선택
        # data = self.generate_data(trading_date, '069500')
        # data.to_pandas().plot(figsize=self.params['FIGSIZE']);  plt.show()

        holding_ser = self.client.portfolio.get_holding_ser()
        return Portfolio({'005930': holding_ser.get('005930', 0)+2}, trading_date)



    def generate_data(self, trading_date, symbol):
        """``symbol`` 종가에 대한 SMA 데이터 생성
        
        :param Timestamp trading_date: 거래 날짜
        :param str symbol: 종목 코드
        :return: SMA 데이터
        :rtype: cudf.DataFrame
        """
        datas      = get_train_data(trading_date, self.raw_datas)
        stock_data = datas['stock']

        ## 2. Index ETF(KODEX200) 선택
        prices  = stock_data[stock_data.symbol == symbol]['close']
        return cudf.DataFrame({
            'price': prices,
            'SMA1': prices.rolling(42).mean(),
            'SMA2': prices.rolling(252).mean()
        })
