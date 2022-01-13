from Engine.BaseTraderEngine import *
from Engine.Engine_Y.util import *
from Trader.Portfolio import *


class TraderEngine_SMA(BaseTraderEngine):
    """윤동진 엔진

    :param dict params: parameters
    :ivar dict raw_datas: raw datas
    """
    def __init__(self, params):
        super().__init__(params)
        self.raw_datas = get_raw_datas()

    def get_portfolio(self, trading_date, client):
        """다음 시간의 포트폴리오를 선택

        :param Timestamp trading_date: 거래 날짜
        :param Client client: 투자자 상태
        :return: 포트폴리오
        :rtype: :class:`Trader.Portfolio`
        """
        ## 1. 데이터 선택
        datas = get_train_data(trading_date, self.raw_datas)
        return Portfolio({'005930': 1, '069500': 10}, trading_date)
