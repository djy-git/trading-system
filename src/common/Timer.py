from common.LoggerFactory import *


class Timer(ContextDecorator):
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
