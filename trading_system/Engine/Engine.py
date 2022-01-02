from common.util import *


class Engine(metaclass=ABCMeta):
    """Engine class(superclass)
    :class:`Engine_Y`, :class:`Engine_J`, :class:`Engine_L` 이 상속받아야 하는 class
    ``PATH.INI_FILE`` 에 저장된 정보를 기반으로 연결된 DB connection을 연결

    :param dict params: Parameter
    """
    def __init__(self, params):
        self.params = params

    def get_connection(self):
        """``PATH.INI_FILE`` 을 기반으로 연결된 DB connection을 반환
        :return: DB connection
        """
        return DBHandler(ini2dict(PATH.INI_FILE, 'DB')).get_connection()

    @abstractmethod
    def collect_data(self):
        """데이터를 수집
        """
        pass

    @abstractmethod
    def insert_into_db(self, data):
        """데이터를 DB에 삽입

        :param dict data: 삽입할 데이터
        """
        pass

    @abstractmethod
    def get_action(self):
        """다음 시점에 취해야 할 매매 action을 반환
        """
        pass
