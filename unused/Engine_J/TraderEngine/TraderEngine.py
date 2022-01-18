from Engine.BaseTraderEngine import *
from unused.Engine_J.CollectorEngine.CollectorEngine import *
from unused.Engine_J.util import *

class TraderEngine(BaseTraderEngine):
    """정재용 엔진
    """
    def __init__(self, params):
        super().__init__(params)
        self.data_collector = CollectorEngine(params)
    @L
    def get_portfolio(self):
        Data_X, Data_Y = self.data_collector.collect_data()
        Data_X = torch.tensor(Data_X)
        model = self.Get_model()
        ans = model(Data_X)
        return ans

    def Train_model(self, PATH='../model/'):
        Data_X, Data_Y = self.data_collector.get_train_data()
        Data_X = torch.tensor(Data_X)
        Data_Y = torch.tensor(Data_Y)
        Data_Y = Data_Y.type(torch.LongTensor)

        train_dataloader = make_data_set(Data_X, Data_Y)
        model = train_model(train_dataloader)
        torch.save(model, PATH+'model.pt')
        return

    def Get_model(self, PATH='../model/'):
        model = torch.load(PATH+'model.pt')
        model.eval()
        return model
'''
test!
'''
tmp = TraderEngine(None)
#tmp.Train_model()
print(tmp.get_portfolio())