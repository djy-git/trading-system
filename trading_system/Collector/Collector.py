from Engine.Engine_Y import *
from Engine.Engine_J import *
from Engine.Engine_L import *


class Collector:
    """데이터 수집기

    :param dict params: 수집 설정
    """
    def __init__(self, params):
        self.params = params


    def run(self):
        """데이터를 수집하고 DB에 입력
        """
        ## 1. Load Engines
        # engines = [Eng(self.params) for Eng in [Engine_Y, Engine_J, Engine_L]]
        engines = [Eng(self.params) for Eng in [Engine_Y]]


        ## 2. 데이터 수집
        datas = self.collect(engines)


        ## 3. DB에 추가
        self.insert_into_db(engines, datas)


    def collect(self, engines):
        """
        각 :class:`trading_system.Engine` 별 필요한 데이터를 수집

        :return: 수집된 데이터
        :rtype: :class:`pandas.DataFrame`
        """
        tasks = [delayed(eng.collect_data)() for eng in engines]
        return compute(*tasks, scheduler='processes')


    def insert_into_db(self, engines, datas):
        """각 :class:`trading_system.Engine` 별 데이터를 DB에 입력
        """
        tasks = [delayed(eng.insert_into_db)(data) for eng, data in zip(engines, datas)]
        compute(*tasks, scheduler='processes')
