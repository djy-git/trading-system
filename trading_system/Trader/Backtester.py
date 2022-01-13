from Engine.Engine_Y.util import *
from Trader.Client import *


class Backtester:
    """Backtesting class

    :param dict params: Backtesting을 위한 parameters
    :ivar dict engines: 엔진 객체들
    :ivar dict raw_datas: raw 데이터
    """
    def __init__(self, params):
        self.params    = params
        self.engines   = self.load_engines()
        self.raw_datas = get_raw_datas()
        
    @L
    def run(self):
        """Backtesting 실행"""
        ## 1. 벤치마크 데이터 가져오기
        benchmark_data = self.get_benchmark_data(self.params['BENCHMARK'])

        ## 2. 투자 진행
        trading_result = self.trade(benchmark_data)
        metrics        = get_metrics(trading_result.benchmark, trading_result.net_wealth, self.params)
        metrics_ts     = get_metrics_ts(trading_result.benchmark, trading_result.net_wealth, self.params)

        ## 3. 결과 출력
        self.plot_result(trading_result, metrics, metrics_ts)

    @L
    def trade(self, benchmark_data):
        """투자 수행
        
        :param cudf.DataFrame benchmark_data: 벤치마크 데이터
        :return: 투자 결과
        :rtype: pandas.DataFrame
        """
        ## 1. 투자자의 상태를 관리하는 Status 객체 생성
        client        = Client(self.params, self.raw_datas)
        net_wealths   = [client.net_wealth]
        balances      = [client.balance]
        stock_wealths = [client.stock_wealth]
        _portfolios   = [str({})]

        ## 2. 시간에 따라 투자 진행
        for date in benchmark_data.index.to_pandas()[1:]:
            ## 2.1 각 엔진 별 포트폴리오 선택
            portfolios = self.get_portfolios(date, client)

            ## 2.2 최종 포트폴리오 선택
            final_portfolio = self.get_final_portfolio(portfolios)

            ## 2.3 투자 수행
            client.trade(final_portfolio)

            ## 2.4 결과 저장
            net_wealths.append(client.net_wealth)
            balances.append(client.balance)
            stock_wealths.append(client.stock_wealth)
            _portfolios.append(str(client.portfolio))

            ## 2.5 결과 출력
            msg  = f"{ts2str(client.updating_date)} \t 순자산: {client.net_wealth:,.0f} = {client.balance:,.0f}(잔고) + {client.stock_wealth:,.0f}(주식평가액) \t (수익률: {100 * (client.net_wealth / self.params['BALANCE'] - 1):.2f}%) \n"
            msg += f"\t\t 포트폴리오: {client.portfolio}"
            LOGGER.info(msg)

        ## 3. 평가액을 반환
        net_wealths = np.array(net_wealths)
        return pd.DataFrame({
            'net_wealth': net_wealths, 'net_wealth_return': price2return(net_wealths).values,  # why??
            'benchmark': benchmark_data.close.to_pandas(), 'benchmark_return': price2return(benchmark_data.close.to_pandas()), 'alpha': prices2alpha(net_wealths, benchmark_data.close).to_pandas(),
            'balance': balances, 'stock_wealth': stock_wealths,
            'portfolio': _portfolios
        })
    def get_benchmark_data(self, symbol):
        """벤치마크 데이터 가져오기

        :param str symbol: 벤치마크 종목
        :return: 데이터
        :rtype: cudf.DataFrame
        """
        for raw_data in self.raw_datas.values():
            if symbol in raw_data.symbol.to_string():  # 빠르지만 date format(%Y-%m-%d)이 symbol 형식과 다른 경우에만 사용가능
                ## 1. 데이터 선택
                data = raw_data[raw_data.symbol == symbol]

                ## 2. 기간 선택
                return data.loc[(str2ts(self.params['TRADE_START_DATE']) <= data.index) & (data.index <= str2ts(self.params['TRADE_END_DATE']))]
        raise ValueError(symbol)
    def load_engines(self):
        """``engine`` 으로 지정된 Engine들을 로드

        :return: 지정된 Engine들
        :rtype: dict
        """
        return {
            id: getattr(import_module(f"Engine.Engine_{id}.TraderEngine.TraderEngine"), "TraderEngine")(self.params)
            for id in self.params['ENGINE']
        }
    def get_portfolios(self, trading_date, client):
        """각 :class:`trading_system.TraderEngine` 별 취할 매매 포트폴리오 받아오기

        :param Timestamp trading_date: 거래 날짜
        :param Client client: 투자자 상태
        :return: 각 :class:`trading_system.TraderEngine` 별 취할 매매 action
        :rtype: dict
        """
        return {id: eng.get_portfolio(trading_date, client) for id, eng in self.engines.items()}
    def get_final_portfolio(self, portfolios):
        """각 엔진들의 portfolio들로부터 최종 portfolio를 생성

        :param dict portfolios: 각 Engine 별 portfolio들
        :return: 최종적으로 선택된 portfolio
        :rtype: Portfolio
        """
        if len(self.params['ENGINE']) == 1:
            return portfolios[self.params['ENGINE']]
        else:
            ## ensemble
            raise NotImplementedError

    def plot_result(self, trading_result, metrics, metrics_ts):
        """결과 출력

        :param pandas.DataFrame trading_result: 투자 결과 (시계열)
        :param pandas.DataFrame metrics: 투자 결과 평가지표
        :param pandas.DataFrame metrics_ts: 투자 결과 평가지표 (시계열)
        """
        generate_dir(PATH.RESULT)
        plot_metrics(metrics, self.params, trading_result.index)
        self.plot_result_price(trading_result, metrics_ts)
        self.plot_result_return(trading_result)
    def plot_result_price(self, trading_result, metrics_ts):
        """Price에 대한 결과 그래프를 출력
        
        :param pandas.DataFrame trading_result: 투자 결과
        :param pandas.DataFrame metrics_ts: 투자 결과 평가지표 (시계열)
        """
        bp = pd.Series(trading_result.benchmark, name=self.params['BENCHMARK'])
        tp = pd.Series(trading_result.net_wealth, name=self.params['ALGORITHM'])
        compare_prices(bp, tp, self.params, metrics_ts, trading_result.balance, trading_result.stock_wealth)
    def plot_result_return(self, trading_result):
        """
        Plot return data

        :param cudf.DataFrame trading_result: 투자 결과
        """
        br = pd.Series(trading_result.benchmark_return, name=self.params['BENCHMARK'])
        tr = pd.Series(trading_result.net_wealth_return, name=self.params['ALGORITHM'])
        compare_returns(br, tr, self.params)
