from Engine.BaseTraderEngine import *
from Engine.Engine_Y.util import *


class TraderEngine_EnhancedIndexTracking(BaseTraderEngine):
    """윤동진 엔진

    :ivar dict params: Parameter
    :ivar Client client: 투자자 상태
    :ivar dict raw_datas: 데이터
    """
    def get_portfolio(self, trading_date):
        ## 1. 종목 선정
        ## 1.1 학습 데이터 선택
        datas      = self.select_datas(trading_date)
        stock_data = datas['stock']
