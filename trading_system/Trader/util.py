from common import *


## File save/load
def unite_none(df):
    """결측값을 None으로 통일

    :param :class:`pandas.DataFrame` df: 제거할 DataFrame
    :return: 제거한 DataFrame
    :rtype: :class:`pandas.DataFrame`
    """
    return df.where((pd.notnull(df)), None)
def to_feather(data, path):
    """``data`` 를 feather file로 저장

    :param DataFrame data: 저장할 데이터
    :param str path: 저장할 경로
    """
    ## 1. None값 단일화
    data = unite_none(data)

    ## 2. Serialize index
    data.reset_index(drop=True, inplace=True)

    ## 3. Save
    data.to_feather(path)

@L
def get_raw_datas(params):
    """Cache된 file 혹은 DB에서 받아오기

    :return: raw data
    :rtype: dict
    """
    ## 1. 주가, 지수, 종목정보 받아오기
    datas = {}
    for data_id in ['stock', 'index', 'info']:
        datas[data_id] = get_raw_data(data_id, params)

    ## 2. 주가, 지수 날짜 일치시키기
    common_indexs  = datas['stock'].index.unique().intersection(datas['index'].index.unique())
    datas['stock'] = datas['stock'].loc[common_indexs]
    datas['index'] = datas['index'].loc[common_indexs]

    return datas
def get_raw_data(data_id, params):
    """``data_id`` 데이터 받아오기

    :param str data_id: 데이터 종류
    :param dict params: parameter
    :return: 데이터
    :rtype: :class:`pandas.DataFrame`
    """
    ## 1. Cache or DB에서 데이터 받아오기
    table_name = 'stock_info_kr' if data_id == 'info' else f'{data_id}_daily_kr'
    file_name  = f'{table_name}.ftr'
    cache_path = join(PATH.TRAIN, file_name)
    try:
        data = pd.read_feather(cache_path)
    except:
        generate_dir(dirname(cache_path))
        data = read_sql(f"select * from {table_name}")
        to_feather(data, cache_path)

    if data_id in ['stock', 'index']:
        ## 2. 기간 선택
        data.date = pd.to_datetime(data.date)
        data = data.loc[(params['START_DATE'] <= data.date) & (data.date <= params['END_DATE'])]
        data = data.set_index(data.date).drop(columns='date')
        
        ## 3. Volume = 0인 row 제거
        if data_id == 'stock':
            data = data.loc[(data.volume > 0) & (data.trading_value > 0)]
        else:
            data = data.loc[data.volume > 0]
    return data
