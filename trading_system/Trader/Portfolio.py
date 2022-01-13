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
    :ivar cudf.DataFrame df: 포트폴리오 데이터
    """
    def __init__(self, dic=None, date=None):
        self.df           = self.generate_df(dic, date)
    def __repr__(self):
        """포트폴리오 정보를 문자열로 반환

        :return: 최근 포트폴리오 정보
        :rtype: str
        """
        return str(self.df2dict())

    def generate_df(self, dic, date):
        """포트폴리오 데이터를 생성

        :param dict dic: 포트폴리오 데이터 ({symbol: weight})
        :param str date: 날짜
        :return df: 포트폴리오 데이터
        :rtype: cudf.DataFrame
        """
        if dic is None:
            df = cudf.DataFrame(columns=['symbol', 'num'], index=pd.DatetimeIndex([], name='date'))
        else:
            assert isinstance(dic, dict), "df should be dict with {symbol: num}"
            assert len(dic) > 0, "new_data가 비어있습니다."
            assert all([num >= 0 for num in dic.values()]), "공매도 비허용"
            df = cudf.DataFrame({'symbol': dic.keys(), 'num': dic.values()}, columns=['symbol', 'num'], index=pd.DatetimeIndex(len(dic) * [date], name='date'))
        df.symbol = df.symbol.astype(str)
        df.num    = df.num.astype(np.int32)
        return df
    def add(self, new_dic, new_date):
        """
        포트폴리오 데이터를 추가

        :param dict new_dic: 추가될 포트폴리오 객체
        :param str new_date: 추가될 날짜
        """
        self.df = cudf.concat([self.df, self.generate_df(new_dic, new_date)])

    def get_data_by_date(self, date):
        """특정 날짜의 포트폴리오 정보를 반환

        :param Timestamp date: 날짜
        :return: 특정 날짜의 포트폴리오 정보
        :rtype: pd.DataFrame
        """
        return self.df[self.df.index == date]
    def get_holding_df(self):
        """최근 날짜의 포트폴리오 정보를 반환

        :return: 최근 날짜의 포트폴리오 정보
        :rtype: cudf.DataFrame
        """
        if len(self.df) > 0:
            df = self.df.loc[self.df.index[-1]]
            if isinstance(df, cudf.Series):  # 데이터 하나만 있을 경우, cudf.Series로 반환
                df = cudf.from_pandas(df).T
            return df
        else:
            return self.generate_df(None, None)
    def get_latest_date(self):
        """가장 최근 포트폴리오의 날짜를 반환

        :return: 가장 최근 포트폴리오의 날짜
        :rtype: Timestamp
        """
        return pd.Timestamp(self.df.index[-1])  # np.datetime -> Timestamp
    def df2dict(self):
        """포트폴리오 데이터를 dict로 변환

        :return: 포트폴리오 데이터
        :rtype: dict
        """
        return {symbol: num for symbol, num in self.get_holding_df().to_pandas().itertuples(index=False)}
