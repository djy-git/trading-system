from InvestorEngine.Engine import *


class Engine_Y(Engine):
    """윤동진 엔진
    """
    def __init__(self, params):
        super().__init__(params)

    @L
    def get_action(self):
        """다음 시간에 수행할 액션을 선택
        """

        with Switch(self.params['INVEST_STRATEGY_Y']) as case:
            if case('momentum_cap_5'):
                ## 1. 데이터 받아오기
                data = self.get_data()

            if case.default:
                raise ValueError(self.params['INVEST_STRATEGY_Y'])

    @L
    def get_data(self):
        """DB로부터 데이터를 받아오기

        :return: 데이터
        :rtype: :class:`pandas.DataFrame`
        """

        ## 1. 데이터 받아오고 전처리 (TODO: update to DB)
        raw_data = pd.read_feather(join(PATH.TRAIN, 'stock_daily_kr.ftr'))
        # raw_data = read_sql("select date, close, return from stock_daily_kr")
        data     = self.process_data(raw_data)

    @L
    def process_data(self, raw_data):
        """데이터 전처리

        :param raw_data: 원본 데이터
        :type raw_data: :class:`pandas.DataFrame`
        :return: 전처리된 데이터
        :rtype: :class:`pandas.DataFrame`
        """
        pass