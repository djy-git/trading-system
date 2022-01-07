from Engine.Engine_Y.util import *
from Trader.util import *
from Trader.Client import *


class Backtester:
    """Backtesting class

    :param dict params: Backtesting을 위한 parameters
    :ivar dict engines: 엔진 객체들
    :ivar dict raw_datas: raw 데이터
    """
    def __init__(self, params):
        self.params  = params
        self.engines = self.load_engines()
        self.raw_datas = {}
        
    @L
    def run(self):
        """Backtesting 실행"""
        ## 1. 벤치마크 데이터 가져오기
        benchmark_data = self.get_benchmark_data('KOSPI200')

        ## 2. 투자 진행
        self.trade(benchmark_data)

    @L
    def trade(self, benchmark_data):
        """투자 수행
        
        :param pd.DataFrame benchmark_data: 벤치마크 데이터
        """
        ## 1. 투자자의 상태를 관리하는 Status 객체 생성
        client = Client(self.params, self.raw_datas)

        ## 2. 시간에 따라 투자 진행
        for date in benchmark_data.index:
            ## 2.1 각 엔진 별 포트폴리오 선택
            portfolios = self.get_portfolios(date, client)

            ## 2.2 최종 포트폴리오 선택
            final_portfolio = self.get_final_portfolio(portfolios)

            ## 3. 투자 수행
            client.trade(final_portfolio)
            LOGGER.info(f"{dt2str(client.updating_date)} 순자산: {client.net_wealth}")

    def get_benchmark_data(self, symbol):
        """벤치마크 데이터 가져오기

        :param dict datas: raw data
        :param str symbol: 벤치마크 종목
        :return: 데이터
        :rtype: pandas.DataFrame
        """
        self.raw_datas = get_raw_datas(self.params)
        for key in ['stock', 'index']:
            if symbol in list(self.raw_datas[key].symbol):
                ## 1. 데이터 선택
                data = self.raw_datas[key].query('symbol == @symbol')

                ## 2. 기간 선택
                return data.loc[(self.params['TRADE_START_DATE'] <= data.index) & (data.index <= self.params['TRADE_END_DATE'])]
        raise ValueError(symbol)

    @L
    def load_engines(self):
        """``engine`` 으로 지정된 Engine들을 로드

        :return: 지정된 Engine들
        :rtype: dict
        """
        return {
            id: getattr(import_module(f"Engine.Engine_{id}.TraderEngine.TraderEngine"), "TraderEngine")(self.params)
            for id in self.params['ENGINE']
        }

    @L
    def get_portfolios(self, trading_date, client):
        """각 :class:`trading_system.TraderEngine` 별 취할 매매 포트폴리오 받아오기

        :param Timestamp trading_date: 거래 날짜
        :param Client client: 투자자 상태
        :return: 각 :class:`trading_system.TraderEngine` 별 취할 매매 action
        :rtype: dict
        """
        return {id: eng.get_portfolio(trading_date, client) for id, eng in self.engines.items()}
    @L
    def get_final_portfolio(self, portfolios):
        """각 엔진들의 portfolio들로부터 최종 portfolio를 생성

        :param dict portfolios: 각 Engine 별 portfolio들
        :return: 최종적으로 선택된 portfolio
        :rtype: Portfolio
        """
        if len(self.params['ENGINE']) == 1:
            return portfolios[self.params['ENGINE']]
        else:
            ## ensemble
            raise NotImplementedError
