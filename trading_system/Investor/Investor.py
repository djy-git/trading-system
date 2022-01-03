from common import *


class Investor:
    """투자를 수행하는 class

    :param dict params: 투자 설정
    :ivar list engines: 사용될 InvestorEngine list
    """
    def __init__(self, params):
        self.params  = params
        self.engines = self.load_engines(params)


    @L
    def run(self):
        """각 :class:`trading_system.InvestorEngine` 별 취할 매매 action을 받아오고 최종적으로 투자를 수행
        """
        ## 1. 각 Engine별 매매 action 가져오기
        actions = self.get_actions()


        ## 3. actions를 최종 action으로 처리
        final_action = self.process_actions(actions)


        ## 4. 투자 수행
        self.invest(final_action)

    @L
    def get_actions(self):
        """각 :class:`trading_system.InvestorEngine` 별 취할 매매 action을 받아오기

        :return: 각 :class:`trading_system.InvestorEngine` 별 취할 매매 action
        :rtype: tuple
        """
        tasks = [delayed(eng.get_action)() for eng in self.engines]
        return compute(*tasks, scheduler='processes')

    @L
    def process_actions(self, actions):
        """actions를 최종 action으로 처리

        :param tuple actions: 각 :class:`trading_system.InvestorEngine` 별 취할 매매 action tuple
        :return: 최종적으로 취할 매매 action
        :rtype: tuple
        """
        ## Simple soft voting
        return np.mean(actions)

    @L
    def invest(self, final_action):
        """투자 수행

        :param :class:`numpy.ndArray` final_action: 최종적으로 취할 매매 action
        """
        ## 증권사 API 등을 이용하여 실제 투자 후 투자 결과를 반환
        raise NotImplementedError

    @L
    def load_engines(self, params):
        """params['ENGINE']으로 지정된 Engine들을 로드

        :return: 지정된 Engine들
        :rtype: list
        """
        classes = [getattr(import_module(f"InvestorEngine.Engine_{id}"), f"Engine_{id}") for id in params['ENGINE']]
        return [cls(params) for cls in classes]
