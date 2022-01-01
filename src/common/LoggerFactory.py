from common.env import *


class LoggerFactory(MetaSingleton):
    @classmethod
    def get(cls):
        if not hasattr(cls, 'logger'):
            cls.logger = cls.generate()
        return cls.logger

    @staticmethod
    def generate():
        generate_dir(PATH.LOG)

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        file_handler   = logging.FileHandler(filename=PATH.LOG_FILE)

        stream_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)

        ## Instead, use common.Timer.L.print_fn() for log format
        # LOG_FORMAT = "[%(asctime)s] %(filename)s - %(funcName)s() | %(levelname)s | %(message)s"
        # formatter  = logging.Formatter(LOG_FORMAT, "%Y-%m-%d %H:%M:%S")
        # stream_handler.setFormatter(formatter)
        # file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        return logger


##########################################################
### CAUTION! LOGGER is declared with global variable
LOGGER = LoggerFactory.get()
##########################################################


### Simple logger using print()
# class Logger:
#     class LogOut:
#         def __init__(self, log_path, stay_stdout=True):
#             self.logout = open(log_path, 'w')
#             self.outs   = [self.logout, sys.stdout] if stay_stdout else [self.logout]
#         def __del__(self):
#             self.logout.close()
#         def write(self, msg):
#             for out in self.outs:
#                 out.write(msg)
#         def flush(self): pass
#
#     ## Level log
#     level     = 1
#     level_val = defaultdict(lambda: 1)
#
#
#
#     def __init__(self, log_dir_path):
#         generate_dir(log_dir_path)
#
#         ## Append log file output to stdout
#         log_path   = join(log_dir_path, f"{datetime.now(timezone('Asia/Seoul')).strftime('%y-%m-%d_%H-%M-%S')}.log")
#         sys.stdout = self.LogOut(log_path)
