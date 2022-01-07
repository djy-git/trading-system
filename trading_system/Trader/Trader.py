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
            if case('fake_trading') or case('real_trading'):
                ## 증권사 API 등을 이용하여 실제 투자 후 투자 결과를 반환
                raise NotImplementedError
            if case.default:
                raise ValueError(self.params['TRADE_METHOD'])
