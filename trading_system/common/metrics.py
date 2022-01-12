from common import *

## 연율화 지수
ANNUALIZATION_FACTOR = 252


def get_ratio(returns):
    """
    Compute ratio (Sharpe ratio, Information ratio, etc)

    :param Sequence returns: 수익률
    :return: ratio 관련값
    :rtype: dict
    """
    mean, std = np.mean(returns), np.std(returns, ddof=1)
    ratio     = np.sqrt(ANNUALIZATION_FACTOR) * mean / std
    return dict(ratio=ratio, mean=mean, std=std)
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
def get_VWR(prices, MAV=0.5, TAU=2):
    """
    Compute Variability Weighted Return (VWR)

    :param pd.Series prices: 가격
    :param float MAV: Maximum Acceptable Variability
    :param float TAU: 가격변동성
    :return: VWR 관련값
    :rtype: dict
    """
    ### 0. Alias
    T = len(prices)

    ### 1. Compound Annual Growth (CAG)
    mean_log_return = np.log(prices[-1] / prices[0]) / (T - 1)
    CAGR = np.exp(mean_log_return * ANNUALIZATION_FACTOR) - 1
    norm_return = CAGR * 100

    ### 2. Ideal spreads_val
    ideal_preds_val = [prices[0] * np.exp(mean_log_return * idx_time) for idx_time in range(T)]

    ### 3. Difference between ideal and real
    diff = [prices[idx_time] / ideal_preds_val[idx_time] - 1 for idx_time in range(T)]

    ### 4. Variability
    variability = np.std(diff, ddof=1)

    if variability < MAV:
        if norm_return > 0:
            return dict(VWR=norm_return * (1 - (variability / MAV) ** TAU), CAGR=CAGR,
                        variability=variability)
        else:
            return dict(VWR=norm_return * (variability / MAV) ** TAU, CAGR=CAGR,
                        variability=variability)
    else:
        return dict(VWR=0, CAGR=CAGR, variability=variability)
