""".. note:: **편의를 위해** ``LOGGER`` **가 전역 변수로 정의되어 있으므로 사용에 주의가 필요**
"""

from common.env import *


class LoggerFactory(metaclass=MetaSingleton):
    """Singleton Logger를 생성하는 class
    
    ``LOGGER`` 사용법
    ::

        try:
            LOGGER.info("Hello, world!")
            4 / 0
        except Exception as e:
            LOGGER.exception(e)
    """
    @classmethod
    def get(cls):
        """기존의 생성된 Logger를 반환하거나 새로운 Logger를 생성하여 반환

        :return: 저장된 Logger
        :rtype: :class:`logging.Logger`
        """
        if not hasattr(cls, 'logger'):
            cls.logger = cls.generate()
        return cls.logger

    @classmethod
    def generate(cls):
        """
        새로운 Logger를 생성

        :return: 생성된 Logger
        :rtype: :class:`logging.Logger`
        """
        def excepthook(*args):
            logger.error('\nUncaught exception:', exc_info=args)
            exit(1)

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
        sys.excepthook = excepthook

        return logger

    # ## Option2: print() can be used for logging
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
## CAUTION! LOGGER is declared with global variable
LOGGER = LoggerFactory.get()
##########################################################
