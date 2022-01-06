from Engine.BaseTraderEngine import *
from Engine.Engine_J.CollectorEngine_J import *
from Engine.Engine_J.util import *

class TraderEngine(BaseTraderEngine):
    """정재용 엔진
    """
    def __init__(self, params):
        super().__init__(params)
        self.data_collector = CollectorEngine_J(params)

    def get_portfolio(self):
        Data_X, Data_Y = self.data_collector.get_predict_Data()
        Data_X = torch.tensor(Data_X)


        model = Get_model(PATH)
        ans = model.predict(Data_X)

        return

    def Train_model(self, PATH):
        Data_X, Data_Y = self.data_collector.get_train_data()
        Data_X = torch.tensor(Data_X)
        Data_Y = torch.tensor(Data_Y)
        Data_Y = Data_Y.type(torch.LongTensor)

        train_dataloader = make_data_set(Data_X, Data_Y)
        model = train_model(train_dataloader)
        torch.save(model, PATH)
        return

    def Get_model(self, PATH):
        model = torch.load(PATH)
        model.eval()
        return model

