from Engine.TraderEngine import *


class TraderEngine_Y(TraderEngine):
    """윤동진 엔진
    """
    def __init__(self, params):
        super().__init__(params)

    @L
    def get_action(self):
        """다음 시간에 수행할 액션을 선택
        """
        cls = getattr(import_module(f"Engine.Engine_Y.TraderEngine_Y_{self.params['TRADE_STRATEGY_Y']}"),
                      f"TraderEngine_Y_{self.params['TRADE_STRATEGY_Y']}")
        return cls(self.params).get_action()
