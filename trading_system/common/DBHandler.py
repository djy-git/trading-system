from trading_system.common.LoggerFactory import *


class DBHandler:
    """Singleton pattern을 통해 하나의 connection을 유지하는 class

    :param dict db_info: DB 접속 계정에 대한 정보
    :cvar list db_infos: DB 접속 계정에 대한 정보 리스트
    :cvar list instances: ``db_infos`` 에 해당하는 인스턴스 리스트
    :cvar list conns: ``db_infos`` 에 해당하는 connection 리스트
    """
    db_infos  = []
    instances = []
    conns     = []

    def __new__(cls, db_info):
        """객체 생성 시, __init__() 이전에 호출**
        :param dict db_info: DB 정보
        :return: DBHandler 객체 (singleton)
        :rtype: object
        """
        ids = {'user', 'password', 'host', 'port', 'db'}
        assert ids.issubset(set(db_info)), f"{set(db_info)} should include {ids}"

        if db_info in cls.db_infos:
            instance = cls.instances[cls.db_infos.index(db_info)]
        else:
            instance = super().__new__(cls)  # generate new instance
            cls.db_infos.append(db_info)
            cls.instances.append(instance)
        return instance
    def __init__(self, db_info):
        self.db_info  = db_info
        self.db_info['port'] = int(self.db_info['port'])  # port should be int
        self.idx_info = self.db_infos.index(db_info)
    def __del__(self):
        """객체 소멸 시, 관리하고 있던 connection들을 모두 해제**
        """
        for conn in self.conns:
            conn.close()

    def get_connection(self):
        """``self.db_info`` 를 기반으로 하는 connection을 반환

        :return: 저장된 connection
        :rtype: :class:`mysql.connector.connection.MySQLConnection`
        """
        conn_desc = f"{self.db_info['user']}@{self.db_info['host']}:{self.db_info['port']} - DB: {self.db_info['db']}"
        if self.idx_info == len(self.conns):
            try:
                self.conns.append(pymysql.connect(**self.db_info))
                LOGGER.info(f"[New connection succeeded] {conn_desc}")
            except:
                LOGGER.exception(f"[Connection failed] {conn_desc}")
                exit()
        else:
            LOGGER.info(f"[Load existing connection] {conn_desc}")
        return self.conns[self.idx_info]
