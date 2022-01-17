from Engine.BaseTraderEngine import *


class TraderEngine(BaseTraderEngine):
    """윤동진 엔진
    """
    def __init__(self, params, client):
        super().__init__(params, client)
        algorithm      = self.params['ALGORITHM']
        self.engine    = getattr(import_module(f"Engine.Engine_Y.TraderEngine.TraderEngine_{algorithm}"), f"TraderEngine_{algorithm}")(self.params, self.client)

    def get_portfolio(self, trading_date):
        """다음 시간의 포트폴리오를 선택
        
        :param Timestamp trading_date: 투자 날짜
        """
        return self.engine.get_portfolio(trading_date)
