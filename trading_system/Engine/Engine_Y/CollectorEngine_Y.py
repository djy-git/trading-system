from Engine.CollectorEngine import *
from Engine.Engine_Y.util import *


class CollectorEngine_Y(CollectorEngine):
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

        :param str country: 국호
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
