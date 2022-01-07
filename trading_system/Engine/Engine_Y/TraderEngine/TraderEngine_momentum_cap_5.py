from Engine.BaseTraderEngine import *
from Engine.Engine_Y.util import *
from Trader.Portfolio import *


class TraderEngine_momentum_cap_5(BaseTraderEngine):
    """윤동진 엔진

    :param dict params: parameters
    :ivar dict raw_datas: raw datas
    """
    def __init__(self, params):
        super().__init__(params)
        self.raw_datas = get_raw_datas(params)

    def get_portfolio(self, trading_date, client):
        """다음 시간의 포트폴리오를 선택

        :param Timestamp trading_date: 거래 날짜
        :param Client client: 투자자 상태
        :return: 포트폴리오
        :rtype: :class:`Trader.Portfolio`
        """
        ## 1. 데이터 받아오기
        # data = self.get_train_data(trading_date)

        holding_data = client.portfolio.get_holding_data()
        if len(holding_data) > 0:
            num = holding_data.query("symbol == '005930'").num[0]
        else:
            num = 0
        return Portfolio({'005930': num+1}, trading_date)

    def get_train_data(self, trading_date):
        """DB로부터 데이터를 받아오기

        :param str trading_date: 거래 날짜
        :return: 데이터
        :rtype: :class:`pandas.DataFrame`
        """
        ## 1. 학습 구간 추출
        datas = {}
        for data_id in self.raw_datas:
            if data_id in ['stock', 'index']:
                datas[data_id] = self.raw_datas[data_id].loc[self.raw_datas[data_id].index < trading_date]
            elif data_id == 'info':
                datas[data_id] = self.raw_datas[data_id].loc[self.raw_datas[data_id].listingdate < trading_date]
        return datas
