from common import *


class Collector:
    """데이터 수집기

    :param dict params: 수집 설정
    :ivar list engines: 사용될 CollectorEngine list
    """
    def __init__(self, params):
        self.params  = params
        self.engines = self.load_engines()


    @L
    def run(self):
        """
        각 :class:`trading_system.TraderEngine` 별 필요한 데이터를 수집

        :return: 수집된 데이터
        :rtype: :class:`pandas.DataFrame`
        """
        for eng in self.engines.values():
            eng.collect_data()


    @L
    def load_engines(self):
        """``engine`` 으로 지정된 Engine들을 로드

        :return: 지정된 Engine들
        :rtype: dict
        """
        return {
            id: getattr(import_module(f"Engine.Engine_{id}.CollectorEngine.CollectorEngine"), "CollectorEngine")(self.params)
            for id in self.params['ENGINE']
        }
