from common import *


class BaseTraderEngine(metaclass=ABCMeta):
    """BaseTraderEngine class(superclass)
    :class:`Engine_Y`, :class:`Engine_J`, :class:`Engine_L` 이 상속받아야 하는 class

    :param dict params: Parameter
    """
    def __init__(self, params):
        self.params = params

    @abstractmethod
    def get_portfolio(self, trading_date, status):
        """``trading_date`` 시점에 취해야 할 매매 portfolio를 반환

        :param Timestamp trading_date: 시점의 날짜
        :param Status status: 투자자 상태
        """
        pass
