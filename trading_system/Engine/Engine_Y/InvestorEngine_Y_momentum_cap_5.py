from Engine.InvestorEngine import *
from Engine.Engine_Y.util import *


class InvestorEngine_Y_momentum_cap_5(InvestorEngine):
    """윤동진 엔진
    """
    def __init__(self, params):
        super().__init__(params)

    @L
    def get_action(self):
        """다음 시간에 수행할 액션을 선택
        """
        ## 1. 데이터 받아오기
        data = self.get_data()


    @L
    def get_data(self):
        """DB로부터 데이터를 받아오기

        :return: 데이터
        :rtype: :class:`pandas.DataFrame`
        """

        ## 1. 데이터 받아오고 전처리 (TODO: update to DB)
        raw_datas = self.get_raw_datas()  # keys: ['stock', 'index', 'info']
        datas     = self.process_datas(raw_datas)

    @L
    def get_raw_datas(self):
        """Cache된 file 혹은 DB에서 받아오기

        :return: raw data
        :rtype: :class:`pandas.DataFrame`
        """
        ## 1. 주가, 지수, 종목정보 받아오기
        datas = {}
        for data_id in ['stock', 'index', 'info']:
            ## 2. Cache or DB에서 데이터 받아오기
            file_name = 'stock_info_kr.ftr' if data_id == 'info' else f'{data_id}_daily_kr.ftr'
            cache_path = join(PATH.TRAIN, file_name)
            try:
                data = pd.read_feather(cache_path)
            except:
                generate_dir(dirname(cache_path))
                data = read_sql("select * from stock_daily_kr")
                to_feather(data, cache_path)
            data.date = pd.to_datetime(data.date)

            ## 3. 기간 선택
            data = data.loc[(self.params['START_DATE'] <= data.date) & (data.date <= self.params['END_DATE'])]

            ## 2. ``date`` index로 설정
            datas[data_id] = data.set_index(data.date).drop(columns='date')

        return datas
    @L
    def process_datas(self, raw_datas):
        """데이터 전처리

        :param raw_datas: 원본 데이터
        :type raw_data: :class:`pandas.DataFrame`
        :return: 전처리된 데이터
        :rtype: :class:`pandas.DataFrame`
        """
        return raw_datas