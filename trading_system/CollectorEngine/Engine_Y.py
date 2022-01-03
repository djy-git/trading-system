from CollectorEngine.Engine import *
import FinanceDataReader as fdr
logging.getLogger('numexpr').setLevel(logging.WARNING)


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
        # TODO: country = 'NYSE'
        for market in ['KRX']:
            self.save_daily(market)


    @L
    def save_daily(self, market):
        """주가와 지수 데이터 저장하기
        """
        self.save_price_info(market, 'stock')
        self.save_price_info(market, 'index')


    @L
    def save_price_info(self, market, data_id):
        """
        [FinanceDataReader](https://financedata.github.io/posts/finance-data-reader-users-guide.html) 참고
        """
        def task(symbol, start=None, end=None):
            try: return fdr.DataReader(symbol, start=start, end=end)
            except: return pd.DataFrame()


        if data_id == 'stock':
            ## 1. ``market`` 상장된 종목들의 일데이터를 가져오기
            df_info = fdr.StockListing(market)
            df_info.columns = map(lambda x: x.lower(), df_info.columns)
            symbols = df_info.symbol
        else:
            ## 2. 지수 일데이터를 가져오기
            if market == 'KRX':
                symbols = ['KS11', 'KQ11', 'KS50', 'KS100', 'KRX100', 'KS200']
            else:
                raise ValueError(market)

        with ProgressBar():
            tasks = [delayed(task)(symbol) for symbol in symbols]
            data  = pd.concat(compute(*tasks, scheduler='processes'))
        data.reset_index(inplace=True)
        data.columns = map(lambda x: x.lower(), data.columns)

        ## TODO: Check if nans exist

        ## 3. DB에 저장
        self.insert_into_db(data, market, data_id)


    @L
    def insert_into_db(self, data, market, data_id):
        """https://blog.naver.com/scyan2011/221963557539 참고
        """
        raise NotImplementedError

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
