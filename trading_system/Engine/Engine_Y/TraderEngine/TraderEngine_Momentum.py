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
        ## 1. Parameters
        symbol      = '069500'  # KODEX200
        window      = 5
        trading_num = 10


        ## 2. 종목 선택
        datas = self.select_datas(trading_date)
        data = datas['stock'][datas['stock'].symbol == symbol]['return'].iloc[-5:]


        ## 3. Time-series momentum
        position    = 'long' if data.rolling(window).mean()[-1] >= 0 else 'short'
        holding_num = self.client.portfolio.get_holding_dic().get(symbol, 0)
        if position == 'long':
            return Portfolio({symbol: holding_num + trading_num}, trading_date)
        else:
            if holding_num <= 1:
                return Portfolio({}, trading_date)
            else:
                return Portfolio({symbol: holding_num - trading_num}, trading_date)
