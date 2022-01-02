from Engine.Engine import *


class Engine_Y(Engine):
    """윤동진 엔진
    """
    def __init__(self, params):
        super().__init__(params)

    def collect_data(self):
        pass

    def insert_into_db(self, data):
        ## 1. Connection을 각 함수에서 받아와야 process 병렬처리가 가능
        self.conn = self.get_connection()

        pass

    def get_action(self):
        return np.array([0, 0, 0, 0, 0])
