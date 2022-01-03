from Engine import *


class Investor:
    """투자를 수행하는 class

    :param list engines: 사용될 Engine list
    :param dict params: 수집 설정
    """
    def __init__(self, engines, params):
        self.engines = engines
        self.params  = params

    @L
    def run(self):
        """각 :class:`trading_system.Engine` 별 취할 매매 action을 받아오고 최종적으로 투자를 수행
        """
        ## 1. 각 Engine별 매매 action 가져오기
        actions = self.get_actions()


        ## 3. actions를 최종 action으로 처리
        final_action = self.process_actions(actions)


        ## 4. 투자 수행
        self.invest(final_action)

    @L
    def get_actions(self):
        """각 :class:`trading_system.Engine` 별 취할 매매 action을 받아오기

        :return: 각 :class:`trading_system.Engine` 별 취할 매매 action
        :rtype: tuple
        """
        tasks = [delayed(eng.get_action)() for eng in self.engines]
        return compute(*tasks, scheduler='processes')

    @L
    def process_actions(self, actions):
        """actions를 최종 action으로 처리

        :param tuple actions: 각 :class:`trading_system.Engine` 별 취할 매매 action tuple
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
