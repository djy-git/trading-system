from common.env import *
from common.LoggerFactory import *
from common.Timer import *
from common.SignalHandler import *
from common.DBHandler import *
from common.config import *


### Register SIGINT
SignalHandler.register_signal(signal.SIGINT)


### Log level
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
