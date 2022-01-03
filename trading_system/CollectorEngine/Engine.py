from common import *


class Engine(metaclass=ABCMeta):
    """InvestorEngine class(superclass)
    :class:`Engine_Y`, :class:`Engine_J`, :class:`Engine_L` 이 상속받아야 하는 class

    :param dict params: Parameter
    """
    def __init__(self, params):
        self.params = params

    @abstractmethod
    def collect_data(self):
        """데이터를 수집
        """
        pass
