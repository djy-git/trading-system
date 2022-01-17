from Engine.BaseTraderEngine import *
from Engine.Engine_Y.util import *


class TraderEngine_Momentum(BaseTraderEngine):
    """윤동진 엔진

    :param dict params: parameters
    :param Client client: Client 정보
    :ivar dict raw_datas: raw datas
    """
    def get_portfolio(self, trading_date):
        """다음 시간의 포트폴리오를 선택

        :param Timestamp trading_date: 거래 날짜
        :return: 포트폴리오
        :rtype: :class:`Trader.Portfolio`
        """
        datas = self.select_datas(trading_date)
        return Portfolio(self.client.portfolio.get_holding_dic(), trading_date)
