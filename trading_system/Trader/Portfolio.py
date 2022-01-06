from Trader.util import *


class Portfolio:
    """포트폴리오 class

    :param dict data: 포트폴리오 데이터 ({symbol: weight})
    """
    def __init__(self, data):
        self.data = data
