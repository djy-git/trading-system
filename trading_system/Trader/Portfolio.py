from Trader.util import *


class Portfolio:
    """포트폴리오 class

    :param dict data_dict: 포트폴리오 데이터 ({symbol: weight})
        e.g.
        (datetime)   (str)    (int)
        date       | symbol   | num
        --------------------------------
        2019-01-01 | '005930' | 5
    :param str date: 투자 날짜
    :ivar pd.DataFrame data: 포트폴리오 데이터
    """
    def __init__(self, data_dict=None, date=None):
        self.data = self.generate_data(data_dict, date)

    def generate_data(self, data_dict, date):
        """포트폴리오 데이터를 생성

        :param dict data_dict: 포트폴리오 데이터 ({symbol: weight})
        :param str date: 날짜
        :return data: 포트폴리오 데이터
        :rtype: pd.DataFrame
        """
        if data_dict is None:
            data = pd.DataFrame(columns=['symbol', 'num'], index=pd.DatetimeIndex([], name='date'))
        else:
            assert isinstance(data_dict, dict), "data should be dict with {symbol: num}"
            assert len(data_dict) > 0, "new_data가 비어있습니다."
            data = pd.DataFrame({'symbol': data_dict.keys(), 'num': data_dict.values()}, columns=['symbol', 'num'], index=pd.DatetimeIndex(len(data_dict) * [date], name='date'))
        data.symbol = data.symbol.astype(str)
        data.num    = data.num.astype(np.int32)
        return data

    def add(self, portfolio, date=None):
        """
        포트폴리오 데이터를 추가

        :param Portfolio|dict portfolio: 추가될 포트폴리오 객체
        :param str date: 추가될 날짜, default=None
        """
        if date:
            self.data = self.data.append(self.generate_data(portfolio, date))
        else:
            self.data = self.data.append(portfolio.data)

    def get_data_by_date(self, date):
        """특정 날짜의 포트폴리오 정보를 반환

        :param Timestamp date: 날짜
        :return: 특정 날짜의 포트폴리오 정보
        :rtype: pd.DataFrame
        """
        return self.data[self.data.index == date]
    def get_latest_data(self):
        """최근 날짜의 포트폴리오 정보를 반환

        :return: 최근 날짜의 포트폴리오 정보
        :rtype: pd.DataFrame
        """
        if len(self.data) > 0:
            data = self.data.loc[self.data.index.max()]
            if isinstance(data, pd.Series):  # 데이터 하나만 있을 경우, pd.Series로 반환
                data = pd.DataFrame(data).T
            return data
        else:
            return self.generate_data(None, None)
    def get_latest_date(self):
        """가장 최근 포트폴리오의 날짜를 반환

        :return: 가장 최근 포트폴리오의 날짜
        :rtype: Timestamp
        """
        return self.data.index.unique()[0]
    def df2dict(self):
        """포트폴리오 데이터를 dict로 변환

        :return: 포트폴리오 데이터
        :rtype: dict
        """
        return {symbol: num for symbol, num in zip(self.data.symbol, self.data.num)}
