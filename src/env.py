### env.py ####################################
# Commonly used packages are defined in here
###############################################


### Internal packages
import sys
import os
from os.path import join, isdir, isfile, exists, basename, dirname, split
import datetime
import joblib
import json
import re
from itertools import product
from time import time, sleep
from collections import defaultdict
from copy import deepcopy as copy
from tqdm import tqdm
from parse import parse, search


### External packages
import numpy as np
import pandas as pd
from tabulate import tabulate
from numba import njit, cuda
from switch import Switch
from dask import delayed, compute
from dask.distributed import Client

## Plot packages
import seaborn as sns
import matplotlib.pyplot as plt
plt.rc('font', family='DejaVu Sans')
plt.rc('axes', unicode_minus=False)

## Matplotlib error handling
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


### Set options
np.set_printoptions(suppress=True, precision=6, edgeitems=20, linewidth=1000)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.width', 1000)
