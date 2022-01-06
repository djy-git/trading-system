from Engine.BaseCollectorEngine import *
from Engine.Engine_J.util import *




class CollectorEngine_Y(BaseCollectorEngine):
    """정재용 엔진
    """
    def __init__(self, params, code_str_list):
        super().__init__(params)
        self.code_str_list = code_str_list

    def collect_data(self):
        for code_str in self.code_str_list:
            url_list, subject_list = get_url_list(code_str)

'''
test 구간
'''

code_str_list = ["samsung%20electronic"]

test_Obj = BaseCollectorEngine_Y(None, code_str_list)
test_Obj.collect_data()
'''
test 구간 해제
'''
