from Engine.InvestorEngine import *


class InvestorEngine_Y(InvestorEngine):
    """윤동진 엔진
    """
    def __init__(self, params):
        super().__init__(params)

    @L
    def get_action(self):
        """다음 시간에 수행할 액션을 선택
        """
        cls = getattr(import_module(f"Engine.Engine_Y.InvestorEngine_Y_{self.params['INVEST_STRATEGY_Y']}"),
                      f"InvestorEngine_Y_{self.params['INVEST_STRATEGY_Y']}")
        return cls(self.params).get_action()
