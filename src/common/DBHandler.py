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
        self.db_info['port'] = int(self.db_info['port'])  # port should be int
        self.idx_info = self.db_infos.index(db_info)
    def __del__(self):
        for conn in self.conns:
            conn.close()

    def get_connection(self):
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
