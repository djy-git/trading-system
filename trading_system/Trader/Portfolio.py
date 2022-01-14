from Trader.util import *


class Portfolio:
    """포트폴리오 class

    :param dict dic: 포트폴리오 데이터 ({symbol: weight})
        e.g.
        (Timestamp)  (str)      (int)
        date       | symbol   | num
        --------------------------------
        2019-01-01 | '005930' | 5
    :param Timestamp date: 투자 날짜
    :ivar pandas.DataFrame df: 포트폴리오 데이터
    :ivar Timestamp latest_date: 최신 투자 날짜
    """
    def __init__(self, dic=None, date=None):
        self.df          = self.generate_df(dic, date)
        self.latest_date = date
    def __repr__(self):
        """포트폴리오 정보를 문자열로 반환

        :return: 최근 포트폴리오 정보
        :rtype: str
        """
        return str(self.get_holding_ser().to_dict())

    def generate_df(self, dic, date):
        """포트폴리오 데이터를 생성

        :param dict dic: 포트폴리오 데이터 ({symbol: weight})
        :param str date: 날짜
        :return df: 포트폴리오 데이터
        :rtype: pandas.DataFrame
        """
        if dic is None or len(dic) == 0:
            df = pd.DataFrame(columns=['symbol', 'num'], index=pd.DatetimeIndex([], name='date'))
        else:
            assert isinstance(dic, dict), "df should be dict with {symbol: num}"
            assert all([num >= 0 for num in dic.values()]), "공매도 비허용"
            df = pd.DataFrame({'symbol': dic.keys(), 'num': dic.values()}, columns=['symbol', 'num'], index=pd.DatetimeIndex(len(dic) * [date], name='date'))
        df.symbol = df.symbol.astype(str)
        df.num    = df.num.astype(np.int32)
        return df
    def add(self, new_dic, new_date):
        """
        포트폴리오 데이터를 추가

        :param dict new_dic: 추가될 포트폴리오 객체
        :param str new_date: 추가될 날짜
        """
        self.df          = pd.concat([self.df, self.generate_df(new_dic, new_date)])
        self.latest_date = new_date
    def get_data_by_date(self, date):
        """특정 날짜의 포트폴리오 정보를 반환

        :param Timestamp date: 날짜
        :return: 특정 날짜의 포트폴리오 정보
        :rtype: pandas.DataFrame
        """
        return self.df[self.df.index == date]
    def get_holding_ser(self):
        """최근 날짜의 포트폴리오 정보를 반환

        :return: 최근 날짜의 포트폴리오 정보
        :rtype: pandas.Series
        """
        if len(self.df) == 0:
            return pd.Series()

        holding_df = self.df.loc[self.latest_date]
        if isinstance(holding_df, pd.Series):
            holding_df = pd.DataFrame(holding_df).T
        return pd.Series({symbol: num for symbol, num in zip(holding_df.symbol, holding_df.num)}, name=self.latest_date)
