from Engine.BaseTraderEngine import *


class TraderEngine(BaseTraderEngine):
    """윤동진 엔진
    """
    def __init__(self, params):
        super().__init__(params)
        self.engine = getattr(import_module(f"Engine.Engine_Y.TraderEngine.TraderEngine_{self.params['Y_ALGORITHM']}"),
                      f"TraderEngine_{self.params['Y_ALGORITHM']}")(self.params)

    def get_portfolio(self, trading_date, status):
        """다음 시간의 포트폴리오를 선택
        
        :param Timestamp trading_date: 투자 날짜
        :param Status status: 투자자 상태
        """
        return self.engine.get_portfolio(trading_date, status)
