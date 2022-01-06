from Engine.TraderEngine import *
from Engine.Engine_Y.util import *


class TraderEngine_Y_momentum_cap_5(TraderEngine):
    """윤동진 엔진
    """
    def __init__(self, params):
        super().__init__(params)

    @L
    def get_portfolio(self):
        """다음 시간의 포트폴리오를 선택
        """
        ## 1. 데이터 받아오기
        data = self.get_data()


    @L
    def get_data(self):
        """DB로부터 데이터를 받아오기

        :return: 데이터
        :rtype: :class:`pandas.DataFrame`
        """

        ## 1. 데이터 받아오고 전처리 (TODO: update to DB)
        raw_datas = get_raw_datas()  # keys: ['stock', 'index', 'info']