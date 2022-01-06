from Engine.CollectorEngine import *
from Engine.Engine_J.util import *




class CollectorEngine_J(CollectorEngine):
    """정재용 엔진
    """
    def __init__(self, params, code_str_list):
        super().__init__(params)
        self.code_str_list = code_str_list

    def collect_data(self):
        code_str_list = ["samsung%20electronic"]
        self.set_code_str_list(code_str_list)

        print("Here!")
        data = get_raw_datas(self.params)
        print(data)
        # for code_str in self.code_str_list:
        #     url_list, subject_list = get_url_list(code_str)
