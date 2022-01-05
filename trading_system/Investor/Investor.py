from common import *


class Investor:
    """투자를 수행하는 class

    :param dict params: 투자 설정
    :ivar list engines: 사용될 InvestorEngine list
    """
    def __init__(self, params):
        self.params  = params
        self.engines = self.load_engines()


    @L
    def run(self):
        """각 :class:`trading_system.InvestorEngine` 별 취할 매매 action을 받아오고 최종적으로 투자를 수행
        """
        ## 1. 각 Engine별 매매 action 가져오기
        actions = self.get_actions()

        ## 2. actions를 최종 action으로 처리
        final_action = self.process_actions(actions)

        ## 3. 투자 수행
        self.invest(final_action)

    @L
    def get_actions(self):
        """각 :class:`trading_system.InvestorEngine` 별 취할 매매 action을 받아오기

        :return: 각 :class:`trading_system.InvestorEngine` 별 취할 매매 action
        :rtype: dict
        """
        return {id: eng.get_action() for id, eng in self.engines.items()}
    @L
    def process_actions(self, actions):
        """actions를 최종 action으로 처리

        :param dict actions: 각 :class:`trading_system.InvestorEngine` 별 취할 매매 action tuple
        :return: 최종적으로 취할 매매 action
        :rtype: dict
        """
        if len(self.params['ENGINE']) == 1:
            return actions[self.params['ENGINE']]
        else:
            ## ensemble
            raise NotImplementedError

    @L
    def invest(self, final_action):
        """투자 수행

        :param dict final_action: 취할 매매 action
        """
        with Switch(self.params['INVEST_METHOD']) as case:
            if case('backtracking'):
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
            id: getattr(import_module(f"Engine.Engine_{id}.InvestorEngine_{id}"), f"InvestorEngine_{id}")(self.params)
            for id in self.params['ENGINE']
        }
