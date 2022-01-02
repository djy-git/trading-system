"""**`setup.py`에서 사용되는 main module**
"""

from trading_system.common.util import *

parser = argparse.ArgumentParser()
parser.add_argument('--CMD', type=str, default='run')


def run():
    F()
@L
def F():
    LOGGER.info("Hello, world!")
    G()
@L
def G():
    DB_INFO = ini2dict(PATH.INI_FILE, 'DB')
    DBHandler(DB_INFO).get_connection()


if __name__ == '__main__':
    args = parser.parse_args()
    with Switch(args.CMD) as case:
        if case('run'):
            run()

        if case('clean'):
            PATH.clean()

        if case.default:
            raise ValueError(f"Unknown command: {args.CMD}")
