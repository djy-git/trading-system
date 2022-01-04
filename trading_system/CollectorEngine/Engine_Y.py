from CollectorEngine.Engine import *
import FinanceDataReader as fdr
import pandas_datareader.data as web
from pykrx.stock import get_market_cap


class Engine_Y(Engine):
    """윤동진 엔진
    """
    def __init__(self, params):
        super().__init__(params)

    @L
    def collect_data(self):
        """
        1. 상장된 종목들의 일데이터를 가져오기
        """
        ## 1. 상장된 종목들의 일데이터를 가져오기
        # TODO: country = 'us'
        for country in ['kr']:
            self.save_daily(country)


    @L
    def save_daily(self, country):
        """주가와 지수 데이터 저장하기

        :param str country: 국호
        """
        ## 1. Save stock price
        markets = self.get_markets(country)
        for market in markets:
            self.save_stock_data(market)

        ## 2. Save index price
        names, symbols = self.get_indexs(country)
        self.save_index_data(names, symbols)


    @L
    def get_markets(self, country):
        """``country`` 국가의 시장들을 가져오기
        
        :param str country: 국호
        """
        ## TODO: DB에서 가져오기
        if country == 'kr':
            markets = ['KRX']
        elif country == 'us':
            markets = ['NYSE', 'NASDAQ']
        else:
            raise ValueError(country)
        return markets
    @L
    def get_indexs(self, country):
        """``country`` 국가의 지수 가져오기

        :param str country: 국호
        """
        ## TODO: DB에서 가져오기
        if country == 'kr':
            names   = ['KOSPI', 'KOSDAQ', 'KOSPI50', 'KOSPI100', 'KRX100', 'KOSPI200']
            symbols = ['KS11', 'KQ11', 'KS50', 'KS100', 'KRX100', 'KS200']
        elif country == 'us':
            names   = ['DowJones', 'NASDAQ', 'SP500', 'SP500_VIX']
            symbols = ['DJI',      'IXIC',   'US500', 'VIX']
        else:
            raise ValueError(country)
        return names, symbols


    @L
    def save_stock_data(self, market):
        """[FinanceDataReader](https://financedata.github.io/posts/finance-data-reader-users-guide.html) 참고
        주가 일데이터 받아오고 저장하기

        :param str market: 시장
        """
        def get_price(symbol, start, end):
            try:
                data = self.download_data(symbol, start=start, end=end)
                data['symbol'] = symbol
                return data
            except:
                return pd.DataFrame()

        ## 1. ``market`` 상장된 종목명 가져오기
        df_info = fdr.StockListing(market)
        symbols = df_info.Symbol

        ## 2. 데이터 가져오기
        with ProgressBar():
            tasks = [delayed(get_price)(symbol, self.params['START_DATE'], self.params['END_DATE']) for symbol in symbols]
            df_stock  = pd.concat(compute(*tasks, scheduler='processes'))
            assert len(df_stock) > 0, "df_stock is empty"
        # tasks = [delayed(get_price)(symbol, self.params['START_DATE'], self.params['END_DATE']) for symbol in symbols]
        # df_stock  = pd.concat(compute(*tasks, scheduler='single-threaded'))

        df_stock.sort_values('date', inplace=True)

        ## 3. File로 저장 (TODO: update)
        generate_dir(PATH.TRAIN)
        df_info.reset_index(drop=True).to_feather(join(PATH.TRAIN, "stock_info_kr.ftr"))
        df_stock.reset_index(drop=True).to_feather(join(PATH.TRAIN, "stock_daily_kr.ftr"))


        # ## 3. DB에 저장
        # ## 3.1 ``df_info`` 저장
        # query = """
        #         replace into stock_info_kr (symbol, market, name, sector, industry, listingdate, settlemonth, representative, homepage, region)
        #         values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        #         """
        # to_sql(query, df_info)
        #
        # ## 3.2 ``df_stock`` 저장
        # query = """
        #         replace into stock_daily_kr (date, open, high, low, close, volume, `return`, symbol)
        #         values (%s, %s, %s, %s, %s, %s, %s, %s)
        #         """
        # to_sql(query, df_stock)
    @L
    def save_index_data(self, names, symbols):
        """[FinanceDataReader](https://financedata.github.io/posts/finance-data-reader-users-guide.html) 참고
        지수 일데이터 받아오고 저장하기

        :param list names: 지수 이름 리스트
        :param list symbols: 종목코드 리스트
        """
        def get_data(symbol, name, start, end):
            try:
                data = self.download_data(symbol, start=start, end=end)
                data['symbol'] = name
                return data
            except:
                return pd.DataFrame()

        ## 1. 데이터 가져오기
        with ProgressBar():
            tasks = [delayed(get_data)(symbol, name, self.params['START_DATE'], self.params['END_DATE']) for symbol, name in zip(symbols, names)]
            df_index  = pd.concat(compute(*tasks, scheduler='processes'))
            assert len(df_index) > 0, "df_index is empty"
        df_index.sort_values('date', inplace=True)

        ## 2. File로 저장 (TODO: update)
        df_index.reset_index(drop=True).to_feather(join(PATH.TRAIN, "index_daily_kr.ftr"))


        # ## 2. DB에 저장
        # query = """
        #         replace into index_daily_kr (date, open, high, low, close, volume, `return`, symbol)
        #         values (%s, %s, %s, %s, %s, %s, %s, %s)
        #         """
        # to_sql(query, df_index)


    def download_data(self, symbol, start, end):
        """주가 일데이터 받아오기
        FinanceDataReader, YahooFinance에서 데이터를 가져온다

        :param str symbol: 종목코드
        :param str start: 시작일
        :param str end: 종료일
        """
        ## 1. 주가 데이터
        try:
            df_price = fdr.DataReader(symbol, start=start, end=end)
        except:
            ## 지수의 경우 에러 발생
            df_price = web.DataReader(f"^{symbol}", 'yahoo', start=start, end=end)
            df_price['Change'] = df_price['Close'].pct_change()
        df_price = df_price.astype(np.float32)
        df_price.rename(columns={'Change': 'Return'}, inplace=True)
        df_price.reset_index(inplace=True)
        df_price.columns = df_price.columns.str.lower()
        df_price = df_price[['date', 'open', 'high', 'low', 'close', 'volume', 'return']]
        
        ## 2. 시가총액 등 데이터
        df_caps = get_market_cap(start, end, symbol)
        df_caps.rename(columns={'시가총액': 'cap', '거래대금': 'trading_value', '상장주식수': 'num_shares'}, inplace=True)
        df_caps.index.name = 'date'
        df_caps.reset_index(inplace=True)
        df_caps = df_caps[['date', 'cap', 'trading_value', 'num_shares']]

        ## 3. 병합
        return pd.merge(df_price, df_caps, how='inner', on='date')


    ### Deprecated
    # @L
    # def get_daily_kr_price(self):
    #     """KOSPI 일데이터 가져오기
    #     """
    #     ## 1. 한국거래소에서 종목코드 받아오기
    #     df_stock_info = self.save_codes()
    #
    #     ## 2. 주가 받아오기
    #     self.save_stock_daily(df_stock_info)
    #
    #
    # @L
    # def save_codes(self):
    #     """
    #     [https://ai-creator.tistory.com/51](https://ai-creator.tistory.com/51) 참조
    #     해당 링크는 한국거래소에서 상장법인목록을 엑셀로 다운로드하는 링크입니다.
    #     다운로드와 동시에 Pandas에 excel 파일이 load가 되는 구조입니다.
    #
    #     :return: 상장법인 코드 데이터프레임
    #     :rtype: :class:`pandas.DataFrame`
    #     """
    #     stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    #     stock_code.sort_values(['상장일'], ascending=True)
    #     stock_code = stock_code[['회사명', '종목코드']]
    #     stock_code = stock_code.rename(columns={'회사명': 'name', '종목코드': 'code'})
    #     stock_code.code = stock_code.code.map('{:06d}'.format)
    #     return stock_code
    #
    # @L
    # def save_stock_daily(self, df_stock_info):
    #     """
    #     Naver finance에서 주가 데이터 받아오기
    #
    #     :param :class:`pandas.DataFrame` df_stock_info: 종목이름과 종목코드
    #     :return: 종목들의 주가
    #     :rtype: :class:`pandas.DataFrame`
    #     """
    #     with ProgressBar():
    #         tasks = [delayed(self.get_stock_daily_code)(code) for code in df_stock_info.code]
    #         data = pd.concat(compute(*tasks, scheduler='processes'), ignore_index=True)
    #
    #     data.dropna(inplace=True)
    #     data = data.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})
    #     data['volume'] = data['volume'].astype(int)
    #     data.sort_values('date', ascending=True)
    #     print(data)
    #
    #
    # def get_stock_daily_code(self, code):
    #     """``code`` 종목의 일데이터를 받아오기
    #
    #     :param str code: 종목코드
    #     :return: 종목의 일데이터
    #     :rtype: :class:`pandas.DataFrame`
    #     """
    #     data = pd.DataFrame()
    #     page = 1
    #     while True:
    #         url    = f'http://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'
    #         header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    #         html   = pd.read_html(requests.get(url,headers=header).text, header=0)
    #         data_pages = html[1].columns
    #         if str(page) not in data_pages:
    #             break
    #         data = pd.concat((data, html[0]), ignore_index=True)
    #         page += 1
    #     return data
