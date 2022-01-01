from common.util import *

@L
def F():
    LOGGER.info("Hello, world!")
    DB_INFO = ini2dict(PATH.INI_FILE, 'DB')
    DBHandler(DB_INFO).get_connection()

if __name__ == '__main__':
    F()
