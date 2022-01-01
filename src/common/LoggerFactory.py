from common.env import *


class LoggerFactory(metaclass=MetaSingleton):
    @classmethod
    def get(cls):
        if not hasattr(cls, 'logger'):
            cls.logger = cls.generate()
        return cls.logger

    @classmethod
    def generate(cls):
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
        sys.excepthook = lambda *args: logger.error('\nUncaught exception:', exc_info=args)

        return logger

    # ### Option2: print() can be used for logging
    # sys.stdout = cls.LogOut(PATH.LOG_FILE)
    # class LogOut:
    #     def __init__(self, log_path, stay_stdout=True):
    #         self.logout = open(log_path, 'w')
    #         self.outs = [self.logout, sys.stdout] if stay_stdout else [self.logout]
    #
    #     def __del__(self):
    #         self.logout.close()
    #
    #     def write(self, msg):
    #         for out in self.outs:
    #             out.write(msg)
    #
    #     def flush(self): pass



##########################################################
### CAUTION! LOGGER is declared with global variable
LOGGER = LoggerFactory.get()
##########################################################
