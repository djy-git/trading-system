from Trader.util import *


class Backtester:
    """Backtesting class

    :param dict params: Backtesting을 위한 parameters
    """
    def __init__(self, params):
        self.params  = params
        self.engines = self.load_engines()

    @L
    def run(self):
        """Backtesting 실행"""
        ## 1. 데이터 가져오기
        ## 1.1 전체 데이터 선택
        datas = get_raw_datas(self.params)
        
        ## 1.2 벤치마크 데이터 선택
        base_data = self.get_benchmark_data(datas, 'KOSPI200')




        # ## 1. 각 Engine별 매매 action 가져오기
        # actions = self.get_actions()
        #
        # ## 2. actions를 최종 action으로 처리
        # final_action = self.process_actions(actions)
        #
        # ## 3. 투자 수행
        # self.trade(final_action)

    def get_benchmark_data(self, datas, symbol):
        """벤치마크 데이터 가져오기

        :param dict datas: raw data
        :param str symbol: 벤치마크 종목
        :return: 데이터
        :rtype: pandas.DataFrame
        """
        for key in ['stock', 'index']:
            if symbol in list(datas[key].symbol):
                ## 1. 데이터 선택
                data = datas[key].query(f"symbol == '{symbol}'")

                ## 2. 기간 선택
                return data.loc[(self.params['TRADE_START_DATE'] <= data.index) & (data.index <= self.params['TRADE_END_DATE'])]
        raise ValueError(symbol)


    #################################

    @L
    def get_actions(self):
        """각 :class:`trading_system.TraderEngine` 별 취할 매매 action을 받아오기

        :return: 각 :class:`trading_system.TraderEngine` 별 취할 매매 action
        :rtype: dict
        """
        return {id: eng.get_action() for id, eng in self.engines.items()}
    @L
    def process_actions(self, actions):
        """actions를 최종 action으로 처리

        :param dict actions: 각 :class:`trading_system.TraderEngine` 별 취할 매매 action tuple
        :return: 최종적으로 취할 매매 action
        :rtype: dict
        """
        if len(self.params['ENGINE']) == 1:
            return actions[self.params['ENGINE']]
        else:
            ## ensemble
            raise NotImplementedError

    @L
    def trade(self, final_action):
        """투자 수행

        :param dict final_action: 취할 매매 action
        """
        with Switch(self.params['TRADE_METHOD']) as case:
            if case('backtesting'):
                pass

            if case('fake_trading') or case('real_trading'):
                ## 증권사 API 등을 이용하여 실제 투자 후 투자 결과를 반환
                raise NotImplementedError

    @L
    def load_engines(self):
        """``engine`` 으로 지정된 Engine들을 로드

        :return: 지정된 Engine들
        :rtype: dict
        """
        return {
            id: getattr(import_module(f"Engine.Engine_{id}.TraderEngine_{id}"), f"TraderEngine_{id}")(self.params)
            for id in self.params['ENGINE']
        }
