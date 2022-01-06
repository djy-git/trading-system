from common import *


class BaseTraderEngine(metaclass=ABCMeta):
    """BaseTraderEngine class(superclass)
    :class:`Engine_Y`, :class:`Engine_J`, :class:`Engine_L` 이 상속받아야 하는 class

    :param dict params: Parameter
    """
    def __init__(self, params):
        self.params = params

    @abstractmethod
    def get_portfolio(self, trading_date):
        """``trading_date`` 시점에 취해야 할 매매 portfolio를 반환

        :param str trading_date: 시점의 날짜
        """
        pass
