from common.env import *


class SignalHandler:
    @classmethod
    def register_signal(cls, signo):
        signal.signal(signo, cls.handler)

    @staticmethod
    def handler(signo, frame):
        LOGGER.info(f"Receive signal({signo})")
        exit(1)
