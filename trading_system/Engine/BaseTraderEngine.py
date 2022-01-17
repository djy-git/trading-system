from Trader.Portfolio import *


class BaseTraderEngine(metaclass=ABCMeta):
    """BaseTraderEngine class(superclass)
    :class:`Engine_Y`, :class:`Engine_J`, :class:`Engine_L` 이 상속받아야 하는 class

    :param dict params: Parameter
    :param Client client: 투자자 상태
    :ivar dict params: Parameter
    :ivar Client client: 투자자 상태
    """
    def __init__(self, params, client):
        self.params    = params
        self.client    = client
        self.raw_datas = get_raw_datas(self.params['START_DATE'], self.params['END_DATE'])

    @abstractmethod
    def get_portfolio(self, trading_date):
        """``trading_date`` 시점에 취해야 할 매매 portfolio를 반환

        :param Timestamp trading_date: 시점의 날짜
        """
        pass

    def select_datas(self, trading_date):
        """데이터 선택

        :param Timestamp trading_date: 거래 날짜
        :return: 현재, 미래 구간이 제외된 학습 데이터
        :rtype: dict
        """
        datas = {}
        for data_id, data in self.raw_datas.items():
            if data_id in ['stock', 'index']:
                datas[data_id] = data.loc[data.index < trading_date]
            elif data_id == 'info':
                datas[data_id] = data.loc[data.listingdate.notnull() & (data.listingdate < trading_date)]
            else:
                raise ValueError(data_id)
        return datas
