from Engine.BaseTraderEngine import *


class TraderEngine(BaseTraderEngine):
    """윤동진 엔진
    """
    def __init__(self, params):
        super().__init__(params)

    @L
    def get_portfolio(self, trading_date):
        """다음 시간의 포트폴리오를 선택
        """
        cls = getattr(import_module(f"Engine.Engine_Y.TraderEngine.TraderEngine_{self.params['Y_ALGORITHM']}"),
                      f"TraderEngine_{self.params['Y_ALGORITHM']}")
        return cls(self.params).get_portfolio(trading_date)
