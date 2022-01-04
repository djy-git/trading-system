from common import *


class Collector:
    """데이터 수집기

    :param dict params: 수집 설정
    :ivar list engines: 사용될 CollectorEngine list
    """
    def __init__(self, params):
        self.params  = params
        self.engines = self.load_engines(params)


    @L
    def run(self):
        """
        각 :class:`trading_system.InvestorEngine` 별 필요한 데이터를 수집

        :return: 수집된 데이터
        :rtype: :class:`pandas.DataFrame`
        """
        for eng in self.engines:
            eng.collect_data()


    @L
    def load_engines(self, params):
        """params['ENGINE']으로 지정된 Engine들을 로드

        :return: 지정된 Engine들
        :rtype: list
        """
        classes = [getattr(import_module(f"CollectorEngine.Engine_{id}"), f"Engine_{id}") for id in params['ENGINE']]
        return [cls(params) for cls in classes]
