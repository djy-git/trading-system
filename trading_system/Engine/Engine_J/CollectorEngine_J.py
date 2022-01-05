from Engine.CollectorEngine import *
from Engine.Engine_J.util import *


for code_str in code_str_list:
    url_list, subject_list = get_url_list(code_str)
class CollectorEngine_Y(CollectorEngine):
    """정재용 엔진
    """
    def __init__(self, params, code_str_list):
        super().__init__(params)
        self.code_str_list = code_str_list

    def collect_data(self):
        pass