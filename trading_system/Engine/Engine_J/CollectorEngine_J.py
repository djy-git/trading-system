from Engine.BaseCollectorEngine import *
from Engine.Engine_J.util import *




class CollectorEngine_J(BaseCollectorEngine):
    """정재용 엔진
    """
    def __init__(self, params):
        super().__init__(params)
        self.code_str_list =None
        self.code_list = None
        self.code_list, self.code_str_list = get_code_code_str()

    def collect_data(self):
        Data_X = np.array([])
        Data_Y = np.array([])

        self.code_list, self.code_str_list = get_code_code_str()
        for code_ind in range(len(self.code_str_list)):
            code_str = self.code_str_list[code_ind]
            code = self.code_list[code_ind]

            url_list, subject_list = get_url_list(code_str)

            totken_txts = [get_tokenize(subject) for subject in subject_list]

            totken_embeddings = [get_embedding_token(totken_txt) for totken_txt in totken_txts]
            totken_embeddings = match_sent_size(totken_embeddings)

            labels = get_label(code, len(subject_list))
            labels = np.array(labels)
            if len(Data_X) == 0:
                Data_X = totken_embeddings
                Data_Y = labels
            else:
                Data_X = np.append(Data_X, totken_embeddings, axis=0)
                Data_Y = np.append(Data_Y, labels, axis=0)

        np.save("", Data_X)
        np.save("", Data_Y)
        return

    def get_train_data(self):
        pass

    def get_predict_Data(self):
        pass

