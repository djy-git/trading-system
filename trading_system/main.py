"""**`setup.py`에서 사용되는 main module**
"""
from Interface import *


parser = argparse.ArgumentParser()

## 1. 수행 작업
parser.add_argument('--CMD', type=str, default='trade')
parser.add_argument('--DEBUG', type=str2bool, default=False)


## 2. 데이터
## 2.1 전체 데이터
parser.add_argument('--TIME_UNIT', type=str, default='day')
parser.add_argument('--START_DATE', type=str, default='2020-01-01')
parser.add_argument('--END_DATE', type=str, default=datetime.now().strftime("%Y-%m-%d"))
parser.add_argument('--COUNTRY', type=str, default='kr')
parser.add_argument('--BENCHMARK', type=str, default='KOSPI200')


## 2.2 거래 데이터
parser.add_argument('--TRADE_START_DATE', type=str, default='2021-01-01')
parser.add_argument('--TRADE_END_DATE', type=str, default=datetime.now().strftime("%Y-%m-%d"))


## 3. 엔진
## 3.1 사용할 엔진
parser.add_argument('--ENGINE', type=str, default='Y')
                    # description='Options: [Y, J, L, or combining]')  # Y or J or L or YJL
## 3.2 각 엔진 세부 설정
parser.add_argument('--ALGORITHM', type=str, default='Buy samsung every day')

## 3.2.1 Y엔진
## 3.2.1.1 투자 알고리즘
parser.add_argument('--Y_ALGORITHM', type=str, default='momentum_cap_5')
parser.add_argument('--FIGSIZE', type=tuple, default=(16, 8))


## 4. 거래 설정
parser.add_argument('--TRADE_METHOD', type=str, default='backtesting')
                    # description='Options: [backtesting, fake_trading, real_trading]')
parser.add_argument('--BALANCE', type=int, default=100_000_000)


if __name__ == '__main__':
    ## 1. Get arguments
    ## TODO: `params` should be loaded from DB
    params = parser.parse_args().__dict__


    ## 2. Generate interface
    interface = Interface(params)
    interface.run()
