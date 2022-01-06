from Engine.BaseTraderEngine import *
from Engine.Engine_Y.util import *


class TraderEngine_momentum_cap_5(BaseTraderEngine):
    """윤동진 엔진

    :param dict params: parameters
    :ivar dict raw_datas: raw datas
    """
    def __init__(self, params):
        super().__init__(params)
        self.raw_datas = get_raw_datas(params)

    @L
    def get_portfolio(self, trading_date):
        """다음 시간의 포트폴리오를 선택

        :param str trading_date: 거래 날짜
        """
        ## 1. 데이터 받아오기
        data = self.get_train_data(trading_date)

        print("get_portfolio() in", trading_date)


    @L
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
