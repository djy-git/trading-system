from Collector.Collector import *
from Investor.Investor import *


class Interface:
    def run(self, params):
        """params['CMD'] 작업을 수행

        :param dict params: 처리해야할 작업의 정보
        """

        ## 1. Load engines
        engines = self.load_engines(params)


        ## 2. Run params['CMD']
        with Switch(params['CMD']) as case:
            if case('collect'):
                collector = Collector(engines, params)
                collector.run()

            if case('invest'):
                investor = Investor(engines, params)
                investor.run()

            if case('clean'):
                PATH.clean()

            if case.default:
                raise ValueError(f"Unknown command: {args.CMD}")

    @L
    def load_engines(self, params):
        """params['ENGINE']으로 지정된 Engine들을 로드

        :return: 지정된 Engine들
        :rtype: list
        """
        return [eval(f"Engine_{id}")(params) for id in list(params['ENGINE'])]
