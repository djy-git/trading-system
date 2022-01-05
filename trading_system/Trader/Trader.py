from Trader.Backtester import *


class Trader:
    """투자를 수행하는 class

    :param dict params: 투자 설정
    :ivar list engines: 사용될 TraderEngine list
    """
    def __init__(self, params):
        self.params  = params


    @L
    def run(self):
        """각 :class:`trading_system.TraderEngine` 별 취할 매매 action을 받아오고 최종적으로 투자를 수행
        """
        with Switch(self.params['TRADE_METHOD']) as case:
            if case('backtesting'):
                Backtester(self.params).run()
            if case.default:
                raise NotImplementedError
