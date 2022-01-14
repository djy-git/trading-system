from common.util import *


def get_metrics(price_benchmark, price_algorithm, params):
    """Benchmark 데이터와 투자 결과에 대한 평가지표

    :param pd.Series price_benchmark: 벤치마크 가격
    :param pd.Series price_algorithm: 알고리즘 가격
    :param dict params: parameters
    :return: 평가지표
    :rtype: pandas.DataFrame
    """
    ## 0. Prepare data
    ps    = price_benchmark, price_algorithm
    rs    = price2return(price_benchmark), price2return(price_algorithm)
    names = [params['BENCHMARK'], params['ALGORITHM']]
    result = pd.DataFrame(index=names,
                          columns=['sharpe ratio', 'mean return', 'std return',
                                   'VWR', 'CAGR', 'variability',
                                   'MDD',
                                   'information ratio', 'mean excess return', 'std excess return'])

    ## VWR parameters
    MAV = 1.5 * get_VWR(ps[0].values)[2]
    TAU = 2

    for name, p, r in zip(names, ps, rs):
        ## 1. Sharpe ratio
        sr_info = get_ratio(r.values)
        result.loc[name]['sharpe ratio'] = sr_info[0]
        result.loc[name]['mean return']  = sr_info[1]
        result.loc[name]['std return']   = sr_info[2]

        ## 2. VWR
        vwr_info = get_VWR(p.values, MAV=MAV, TAU=TAU)
        result.loc[name]['VWR']         = vwr_info[0]
        result.loc[name]['CAGR']        = vwr_info[1]
        result.loc[name]['variability'] = vwr_info[2]

        ## 3. Maximum DrawDown
        result.loc[name]['MDD'] = get_MDD(p.values)

        ## 4. Information Ratio
        if name == params['ALGORITHM']:
            ir_info = get_ratio((rs[1] - rs[0]).values)
            result.loc[name]['information ratio']  = ir_info[0]
            result.loc[name]['mean excess return'] = ir_info[1]
            result.loc[name]['std excess return']  = ir_info[2]

    return result

@njit
def get_ratio(returns):
    """
    Compute ratio (Sharpe ratio, Information ratio, etc)

    :param numpy.ndArray returns: 수익률
    :return: ratio, mean, std
    :rtype: tuple
    """
    mean, std = np.mean(returns), np.std(returns)
    ratio     = np.sqrt(ANNUALIZATION_FACTOR) * mean / std
    return ratio, mean, std
@njit
def get_MDD(prices):
    """
    Compute Maximum Drawdown

    :param Sequence prices: 가격
    :return: Maximum Drawdown
    :rtype: float
    """
    max_price = prices[0]
    max_drawdown = 0
    for price in prices:
        if price > max_price:
            max_price = price
        drawdown = (max_price - price) / max_price
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    return max_drawdown
@njit
def get_VWR(prices, MAV=0.5, TAU=2):
    """
    Compute Variability Weighted Return (VWR)
    참고) https://www.crystalbull.com/sharpe-ratio-better-with-log-returns

    :param pd.Series prices: 가격
    :param float MAV: Maximum Acceptable Variability
    :param float TAU: 가격변동성
    :return: VWR, CAGR, variability
    :rtype: tuple
    """
    ### 0. Alias
    T = len(prices)

    ### 1. Compound Annual Growth (CAG)
    mean_log_return = np.log(prices[-1] / prices[0]) / (T - 1)
    CAGR = np.exp(mean_log_return * ANNUALIZATION_FACTOR) - 1
    norm_return = CAGR * 100

    ### 2. Ideal spreads_val
    ideal_preds_val = np.array([prices[0] * np.exp(mean_log_return * idx_time) for idx_time in range(T)])

    ### 3. Difference between ideal and real
    diff = np.array([prices[idx_time] / ideal_preds_val[idx_time] - 1 for idx_time in range(T)])

    ### 4. Variability
    variability = np.std(diff)

    if variability < MAV:
        if norm_return > 0:
            return norm_return * (1 - (variability / MAV) ** TAU), CAGR, variability
            # return dict(VWR=norm_return * (1 - (variability / MAV) ** TAU), CAGR=CAGR,
            #             variability=variability)
        else:
            return norm_return * (variability / MAV) ** TAU, CAGR, variability
            # return dict(VWR=norm_return * (variability / MAV) ** TAU, CAGR=CAGR,
            #             variability=variability)
    else:
        return 0, CAGR, variability
        # return dict(VWR=0, CAGR=CAGR, variability=variability)
