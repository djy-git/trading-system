from Engine.TraderEngine import *


class TraderEngine_Y(TraderEngine):
    """윤동진 엔진
    """
    def __init__(self, params):
        super().__init__(params)

    @L
    def get_portfolio(self):
        """다음 시간의 포트폴리오를 선택
        """
        cls = getattr(import_module(f"Engine.Engine_Y.TraderEngine_Y_{self.params['Y_ALGORITHM']}"),
                      f"TraderEngine_Y_{self.params['Y_ALGORITHM']}")
        return cls(self.params).get_portfolio()
