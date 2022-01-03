from Engine import *


class Collector:
    """데이터 수집기

    :param list engines: 사용될 Engine list
    :param dict params: 수집 설정
    """
    def __init__(self, engines, params):
        self.engines = engines
        self.params  = params


    @L
    def run(self):
        """데이터를 수집하고 DB에 입력
        """
        ## 1. 데이터 수집
        datas = self.collect()


        ## 2. DB에 추가
        self.insert_into_db(datas)

    @L
    def collect(self):
        """
        각 :class:`trading_system.Engine` 별 필요한 데이터를 수집

        :return: 수집된 데이터
        :rtype: :class:`pandas.DataFrame`
        """
        tasks = [delayed(eng.collect_data)() for eng in self.engines]
        return compute(*tasks, scheduler='processes')

    @L
    def insert_into_db(self, datas):
        """각 :class:`trading_system.Engine` 별 데이터를 DB에 입력
        """
        tasks = [delayed(eng.insert_into_db)(data) for eng, data in zip(self.engines, datas)]
        compute(*tasks, scheduler='processes')
