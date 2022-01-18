from Engine.BaseTraderEngine import *
from Engine.Engine_Y.util import *


class TraderEngine_Momentum(BaseTraderEngine):
    """윤동진 엔진

    :ivar dict params: Parameter
    :ivar Client client: 투자자 상태
    :ivar dict raw_datas: 데이터
    """
    def get_portfolio(self, trading_date):
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
