from CollectorEngine.Engine import *
from CollectorEngine.Engine_Y.util import *


class Engine_Y(Engine):
    """윤동진 엔진
    """
    def __init__(self, params):
        super().__init__(params)
        generate_dir(PATH.TRAIN)

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
        for market in get_markets(country):
            self.save_stock_data(country, market)

        ## 2. Save index price
        names, symbols = get_indexs(country)
        self.save_index_data(country, names, symbols)
    @L
    def save_stock_data(self, country, market):
        """[FinanceDataReader](https://financedata.github.io/posts/finance-data-reader-users-guide.html) 참고
        주가 일데이터 받아오고 저장하기

        :param str market: 시장
        """
        ## 1. ``market`` 상장된 종목명 가져오기
        df_info = download_stock_info(market)

        ## 2. 데이터 가져오기
        def get_price(symbol, start, end):
            try: return download_price(symbol, start=start, end=end)
            except: return pd.DataFrame()
        tasks    = [delayed(get_price)(symbol, self.params['START_DATE'], self.params['END_DATE']) for symbol in df_info.symbol]
        df_stock = pd.concat(exec_parallel(tasks, self.params['DEBUG']))
        df_stock.sort_values('date', inplace=True)

        ## 3. File로 저장
        table_info  = f"stock_info_{country}"
        table_daily = f"stock_daily_{country}"
        df_info.reset_index(drop=True).to_feather(join(PATH.TRAIN, f"{table_info}.ftr"))
        df_stock.reset_index(drop=True).to_feather(join(PATH.TRAIN, f"{table_daily}.ftr"))

        ## 4. DB에 저장
        ## 4.1 ``df_info`` 저장
        query = f"""
                replace into {table_info} (symbol, market, name, sector, industry, listingdate, settlemonth, representative, homepage, region, update_date)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        to_sql(query, df_info)

        ## 4.2 ``df_stock`` 저장
        query = f"""
                replace into {table_daily} (date, open, high, low, close, volume, `return`, `cap`, trading_value, num_shares, symbol)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        to_sql(query, df_stock)
    @L
    def save_index_data(self, country, names, symbols):
        """[FinanceDataReader](https://financedata.github.io/posts/finance-data-reader-users-guide.html) 참고
        지수 일데이터 받아오고 저장하기

        :param str country: 국호
        :param list names: 지수 이름 리스트
        :param list symbols: 종목코드 리스트
        """
        ## 1. 데이터 가져오기
        def get_data(symbol, name, start, end):
            try:
                data = download_price(symbol, start=start, end=end)
                data['symbol'] = name
                data.drop(columns=['cap', 'trading_value', 'num_shares'], inplace=True)
                return data
            except:
                return pd.DataFrame()
        tasks    = [delayed(get_data)(symbol, name, self.params['START_DATE'], self.params['END_DATE']) for symbol, name in zip(symbols, names)]
        df_index = pd.concat(exec_parallel(tasks, self.params['DEBUG']))
        df_index.sort_values('date', inplace=True)

        ## 2. File로 저장
        table_daily = f"index_daily_{country}"
        df_index.reset_index(drop=True).to_feather(join(PATH.TRAIN, f"{table_daily}.ftr"))

        ## 3. DB에 저장
        query = f"""
                replace into {table_daily} (date, open, high, low, close, volume, `return`, symbol)
                values (%s, %s, %s, %s, %s, %s, %s, %s)
                """
        to_sql(query, df_index)


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
