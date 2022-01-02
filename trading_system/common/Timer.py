from trading_system.common.LoggerFactory import *


class Timer(ContextDecorator):
    """수행시간을 측정하는 class

    함수의 수행 시간을 측정하기 위해 2가지 방법을 사용할 수 있다.
    
    1. Context manager
    ::

        with Timer("fn()"):
            fn()

    2. Decorator
    ::

        @Timer("fn()")
        def fn():
            # do something
        fn()

    :param str name: 측정할 작업의 이름, default: 'untitled'
    :param bool verbose: 작업 시간을 출력할지 여부, default: `True`
    """
    def __init__(self, name='untitled', verbose=True):
        self.name    = name
        self.verbose = verbose
    def __enter__(self):
        self.start_time = time()
        return self
    def __exit__(self, *exc):
        elapsed_time = time() - self.start_time
        if elapsed_time > 1 or self.verbose:
            LOGGER.info(f"* {self.name} [{elapsed_time:.2f}s]")  # ({elapsed_time/60:.2f}m)
        return False
