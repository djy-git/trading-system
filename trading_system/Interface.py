from Collector.Collector import *
from Investor.Investor import *


class Interface:
    """Parameter를 입력받아 작업을 수행하는 class

    :param dict params: 처리해야할 작업의 정보
    """
    def __init__(self, params):
        self.params = params


    def run(self):
        """``self.params['CMD']`` 작업을 수행
        """
        with Switch(self.params['CMD']) as case:
            if case('collect'):
                collector = Collector(self.params)
                collector.run()

            if case('invest'):
                investor = Investor(self.params)
                investor.run()

            if case('clean'):
                PATH.clean()

            if case.default:
                raise ValueError(f"Unknown command: {self.params['CMD']}")
