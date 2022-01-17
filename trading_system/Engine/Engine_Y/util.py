from Trader.util import *
import pandas_datareader.data as web
import FinanceDataReader as fdr
import pykrx.stock as kstock


## Silent mode
logging.getLogger('numexpr').setLevel(logging.WARNING)


## Get information
def get_markets(country):
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
def get_indexs(country):
    """``country`` 국가의 지수 가져오기

    :param str country: 국호
    """
    ## TODO: DB에서 가져오기
    if country == 'kr':
        names = ['KOSPI', 'KOSDAQ', 'KOSPI50', 'KOSPI100', 'KRX100', 'KOSPI200']
        symbols = ['KS11', 'KQ11', 'KS50', 'KS100', 'KRX100', 'KS200']
    elif country == 'us':
        names = ['DowJones', 'NASDAQ', 'SP500', 'SP500_VIX']
        symbols = ['DJI', 'IXIC', 'US500', 'VIX']
    else:
        raise ValueError(country)
    return names, symbols


## Download data
def download_price(symbol, start, end):
    """주가 일데이터 받아오기
    FinanceDataReader, YahooFinance에서 데이터를 가져온다

    :param str symbol: 종목코드
    :param str start: 시작일
    :param str end: 종료일
    :return: 주가 일데이터
    :rtype: pandas.DataFrame
    """
    ## 1. 주가 데이터
    df_price = fdr.DataReader(symbol, start=start, end=end)
    if len(df_price) == 0:  # TODO: check (지수의 경우 에러 발생 가능)
        df_price = web.DataReader(f"^{symbol}", 'yahoo', start=start, end=end)
        df_price['Change'] = df_price['Close'].pct_change()
    assert len(df_price) > 0, f"df_price of {symbol}({symbol2name(symbol)}) is empty"

    df_price = df_price.astype(np.float32)
    df_price.columns = df_price.columns.str.lower()
    df_price.rename(columns={'change': 'return'}, inplace=True)
    df_price.reset_index(inplace=True)
    df_price.columns = df_price.columns.str.lower()
    df_price = df_price[['date', 'open', 'high', 'low', 'close', 'volume', 'return']]


    ## 2. 시가총액 등 데이터 (TODO: us)
    LOGGER.setLevel(logging.WARNING)  # kstock.get_market_cap() logs error with info()
    df_caps = kstock.get_market_cap(start, end, symbol)
    name = symbol2name(symbol)
    LOGGER.setLevel(logging.INFO)
    if len(df_caps) == 0:
        LOGGER.info(f"\ndf_caps of {symbol}({name}) is empty")  # ETF 종목은 없음
        df_caps = pd.DataFrame({'시가총액': None, '거래대금': None, '상장주식수': None}, index=df_price.date)
    df_caps.index.name = 'date'
    df_caps.rename(columns={'시가총액': 'cap', '거래대금': 'trading_value', '상장주식수': 'num_shares'}, inplace=True)
    df_caps.reset_index(inplace=True)
    df_caps = df_caps[['date', 'cap', 'trading_value', 'num_shares']]

    ## 3. 병합
    df_merge = pd.merge(df_price, df_caps, how='inner', on='date')

    ## 4. return: nan row 제거
    df_merge.dropna(subset=['return'], inplace=True)

    ## 5. 종목코드 추가
    df_merge['symbol'] = symbol

    return df_merge
def download_stock_info(market):
    """주식 정보 받아오기

    :param str market: 시장
    :return: 주식 정보
    :rtype: pandas.DataFrame
    """
    df_info = fdr.StockListing(market)
    assert len(df_info) > 0, "df_info is empty"

    df_info = df_info.astype(str)
    df_info.columns = df_info.columns.str.lower()
    df_info['update_date'] = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))
    return df_info
