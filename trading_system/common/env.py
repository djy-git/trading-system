"""**최하위 environment module**

1. 일반적으로 사용되는 package와 함수, class가 정의되어 있음
2. 이 module에서 project 내 다른 module, package를 import하면 안 됨 (최하위 module)
"""

### Internal packages
import sys
import os
from os.path import join, isdir, isfile, exists, basename, dirname, split, abspath
import shutil
from time import time, sleep
from datetime import datetime, timedelta
from pytz import timezone
from itertools import product
from functools import wraps
from collections import defaultdict
from copy import deepcopy as copy
import argparse
from contextlib import ContextDecorator
from tqdm import tqdm
import joblib
import json
import re
import logging
import signal
import configparser


### External packages
import numpy as np
import pandas as pd
from tabulate import tabulate
from numba import njit, cuda
from dask import delayed, compute
from dask.distributed import Client
from switch import Switch
from parse import parse, search
import pymysql


## Plotting packages
import seaborn as sns
import matplotlib.pyplot as plt
import cv2
import PIL
from PIL import Image


### Matplotlib options
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.rc('font', family='DejaVu Sans')
plt.rc('axes', unicode_minus=False)  # Remove warning (Glyps 8722)


### Set options
np.set_printoptions(suppress=True, precision=6, edgeitems=20, linewidth=1000)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.width', 1000)


### PATH
class PATH:
    """Directory, file들에 대한 경로가 저장된 class

    :cvar str ROOT: Project의 root directory의 경로
    :cvar str SRC: Source code가 포함된 directory의 경로
    :cvar str INPUT: Input data가 포함된 directory의 경로
    :cvar str OUTPUT: Output data가 포함된 directory의 경로
    :cvar str TRAIN: Train data가 포함된 directory의 경로
    :cvar str Test: Test data가 포함된 directory의 경로
    :cvar str CKPT: Checkpoint가 포함된 directory의 경로
    :cvar str RESULT: 결과가 포함된 directory의 경로
    :cvar str LOG: Log가 포함된 directory의 경로
    :cvar str LOG_FILE: Log file의 경로
    :cvar str INI_FILE: 비공개 ini file의 경로
    """
    ROOT     = abspath(dirname(os.getcwd()))
    SRC      = join(ROOT, 'trading_system')
    INPUT    = join(ROOT, 'input')
    OUTPUT   = join(ROOT, 'output')
    TRAIN    = join(INPUT, 'train')
    TEST     = join(INPUT, 'test')
    CKPT     = join(SRC, 'ckpt')
    RESULT   = join(ROOT, 'result')
    LOG      = join(ROOT, 'log')
    LOG_FILE = join(LOG, f"{datetime.now(timezone('Asia/Seoul')).strftime('%y-%m-%d_%H-%M-%S')}.log")
    INI_FILE = join(SRC, 'common', 'account.ini')

    @classmethod
    def clean(cls):
        """``OUTPUT`` , ``CKPT`` , ``RESULT`` , ``LOG`` directory를 제거
        """
        for path in [cls.OUTPUT, cls.CKPT, cls.RESULT, cls.LOG]:
            remove_dir(path)


### Utility functions
## lambda functions
list_all   = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path))]
list_dirs  = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path)) if isdir(join(path, name))]
list_files = lambda path: [(join(path, name), name) for name in sorted(os.listdir(path)) if isfile(join(path, name))]


## Convertor
def str2bool(s):
    if isinstance(s, bool):
        return s
    if s.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif s.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
dt2str = lambda dt: dt.strftime('%Y-%m-%d')
str2dt = lambda s: pd.to_datetime(s).date()
def ini2dict(path, section):
    config = configparser.ConfigParser()
    config.read(path)
    return dict(config[section])


## Manage directory
def generate_dir(path):
    if not isdir(path):
        os.makedirs(path)
def remove_dir(path):
    if isdir(path):
        shutil.rmtree(path)


### Singleton superclass
class MetaSingleton(type):
    """Singleton pattern을 위한 superclass

    :cvar dict _instances: 독립적인 객체들
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
