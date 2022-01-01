from common.util import *

parser = argparse.ArgumentParser()
parser.add_argument('--option', type=str2bool, default=False)


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
    F()
