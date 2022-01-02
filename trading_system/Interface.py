from Collector.Collector import *
from Investor.Investor import *


class Interface:
    def run(self, params):
        """params['CMD'] 작업을 수행

        :param dict params: 처리해야할 작업의 정보
        """
        with Switch(params['CMD']) as case:
            if case('collect'):
                collector = Collector(params)
                collector.run()

            if case('invest'):
                investor = Investor(params)
                investor.run()

            if case('clean'):
                PATH.clean()

            if case.default:
                raise ValueError(f"Unknown command: {args.CMD}")
