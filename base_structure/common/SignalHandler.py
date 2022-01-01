from base_structure.common.LoggerFactory import *


class SignalHandler:
    """Signal을 처리하는 class
    """
    @classmethod
    def register_signal(cls, signo):
        """Signal을 처리하는 함수를 등록하는 함수

        :param int signo: 처리될 signal(주로 ``signal.SIGINT`` , ``signal.SIGTERM`` 의 형태로 입력)
        """
        signal.signal(signo, cls.handler)

    @staticmethod
    def handler(signo, frame):
        """Signal을 받으면 종료하는 함수 

        :param int signo: 처리될 signal
        :param frame: dummy parameter
        """
        LOGGER.info(f"Receive signal({signo})")
        exit(1)
