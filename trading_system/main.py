"""**`setup.py`에서 사용되는 main module**
"""
from Interface import *

parser = argparse.ArgumentParser()
parser.add_argument('--CMD', type=str, default='collect')



if __name__ == '__main__':
    ## 1. Get arguments
    ## TODO: `params` should be loaded from DB
    params = parser.parse_args().__dict__


    ## 2. Generate interface
    interface = Interface()
    interface.run(params)