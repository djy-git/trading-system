from common.LoggerFactory import *


class DBHandler:
    db_infos  = []
    instances = []
    conns     = []

    def __new__(cls, db_info):
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
        self.idx_info = self.db_infos.index(db_info)
    def __del__(self):
        for conn in self.conns:
            conn.close()

    def get_connection(self):
        if self.idx_info == len(self.conns):
            try:
                conn = pymysql.connect(**self.db_info)
                self.conns.append(conn)
                LOGGER.info(f"[New connection succeeded] {self.db_info['user']}@{self.db_info['host']}:{self.db_info['port']} DB: {self.db_info['db']}")
            except Exception as e:
                LOGGER.exception(f"[Connection failed] {self.db_info['user']}@{self.db_info['host']}:{self.db_info['port']} DB: {self.db_info['db']}")
                exit()
        else:
            LOGGER.info(f"[Load existing connection] {self.db_info['user']}@{self.db_info['host']}:{self.db_info['port']} DB: {self.db_info['db']}")
        return self.conns[self.idx_info]
