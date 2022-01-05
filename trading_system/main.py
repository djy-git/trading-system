"""**`setup.py`에서 사용되는 main module**
"""
from Interface import *


parser = argparse.ArgumentParser()
parser.add_argument('--CMD', type=str, default='collect')
parser.add_argument('--ENGINE', type=str, default='Y')
                    # description='Options: [Y, J, L, or combining]')  # Y or J or L or YJL

# parser.add_argument('--START_DATE', type=str, default='2000-01-01')
# parser.add_argument('--END_DATE', type=str, default=datetime.now().strftime("%Y-%m-%d"))
parser.add_argument('--START_DATE', type=str, default='2022-01-05')
parser.add_argument('--END_DATE', type=str, default=datetime.now().strftime("%Y-%m-%d"))

parser.add_argument('--INVEST_METHOD', type=str, default='backtracking')
                    # description='Options: [backtracking, fake_trading, real_trading]')

parser.add_argument('--TIME_UNIT', type=str, default='day')
parser.add_argument('--INVEST_STRATEGY_Y', type=str, default='momentum_cap_5')
parser.add_argument('--DEBUG', type=str2bool, default=False)



if __name__ == '__main__':
    ## 1. Get arguments
    ## TODO: `params` should be loaded from DB
    params = parser.parse_args().__dict__


    ## 2. Generate interface
    interface = Interface(params)
    interface.run()
