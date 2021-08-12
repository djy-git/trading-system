### util.py ###################################
# Commonly used functions, classes are defined in here
###############################################


from env import *
from config import *


### lambda functions
tprint         = lambda dic: print(tabulate(dic, headers='keys', tablefmt='psql'))  # print 'dic' with fancy 'psql' form
list_only_dir  = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path)) if isdir(join(path, name))]
list_only_file = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path)) if not isfile(join(path, name))]
