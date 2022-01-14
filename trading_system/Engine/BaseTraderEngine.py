from common import *


class BaseTraderEngine(metaclass=ABCMeta):
    """BaseTraderEngine class(superclass)
    :class:`Engine_Y`, :class:`Engine_J`, :class:`Engine_L` 이 상속받아야 하는 class

    :param dict params: Parameter
    :param Client client: 투자자 상태
    :ivar dict params: Parameter
    :ivar Client client: 투자자 상태
    """
    def __init__(self, params, client):
        self.params = params
        self.client = client

    @abstractmethod
    def get_portfolio(self, trading_date):
        """``trading_date`` 시점에 취해야 할 매매 portfolio를 반환

        :param Timestamp trading_date: 시점의 날짜
        """
        pass

    def get_holding_num(self, symbol):
        """주식 종목 ``symbol``의 현재 보유 개수를 반환

        :param str symbol: 종목코드
        :return: 보유 개수
        :rtype: int
        """
        return self.client.get(symbol, 0)
