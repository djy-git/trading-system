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


class Level:
    val  = 1
    vals = defaultdict(lambda: 1)

    @classmethod
    def step_into(cls):
        cls.val += 1
    @classmethod
    def step_out(cls):
        cls.val           -= 1
        cls.vals[cls.val] += 1


def L(fn):
    def print_fn(name, args, fn):
        logs = f"> {name} "
        if len(args) > 0 and isinstance(args[0], object):
            logs = f"{logs}{fn.__module__.split('.')[-1]}."
        logs = f"{logs}{fn.__name__}()"
        LOGGER.info(logs)

    @wraps(fn)
    def log(*args, **kwargs):
        name = f"{'.'.join([str(Level.vals[l]) for l in range(1, Level.val+1)]):<15}"

        print_fn(name, args, fn)
        Level.step_into()

        with Timer(name):
            rst = fn(*args, **kwargs)

        Level.step_out()
        return rst
    return log
