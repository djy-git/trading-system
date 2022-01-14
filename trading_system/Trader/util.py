from common import *


@L
def get_raw_datas(start_date=None, end_date=None):
    """Cache된 file 혹은 DB에서 받아오기

    :param str start_date: 시작 날짜
    :param str end_date: 끝 날짜
    :return: raw data
    :rtype: dict
    """
    def get_raw_data(data_id):
        """``data_id`` 데이터 받아오기

        :param str data_id: 데이터 종류
        :return: 데이터
        :rtype: :class:`cudf.DataFrame`
        """
        ## 1. Cache or DB에서 데이터 받아오기
        table_name = 'stock_info_kr' if data_id == 'info' else f'{data_id}_daily_kr'
        cache_path = join(PATH.TRAIN, f'{table_name}.ftr')
        if not isfile(cache_path):
            raw_data = cudf.from_pandas(read_sql(f"select * from {table_name}"))
            generate_dir(dirname(cache_path))
            raw_data.to_feather(cache_path)
        raw_data = cudf.read_feather(cache_path)

        if data_id in ['stock', 'index']:
            ## 2. 기간 선택
            data = raw_data.set_index(raw_data.date).drop(columns='date')

            ## 3. volume = 0인 row 제거 (trading_value 는 nan 일 수 있음)
            data = data.loc[data.volume > 0]
        elif data_id == 'info':
            data = raw_data
            for col in ('listingdate', 'update_date'):
                data[col] = pd.to_datetime(data[col].values_host)
        else:
            raise ValueError(data_id)

        return data

    ## 1. 주가, 지수, 종목정보 받아오기
    datas = {}
    for data_id in ['stock', 'index', 'info']:
        datas[data_id] = get_raw_data(data_id)

    ## 2. 주가, 지수 날짜 일치시키기
    common_indexs  = datas['stock'].index.unique().to_pandas().intersection(datas['index'].index.unique().to_pandas())
    datas['stock'] = datas['stock'].loc[common_indexs]
    datas['index'] = datas['index'].loc[common_indexs]

    if start_date is not None and end_date is not None:
        ## 3. 데이터 선택
        start_date, end_date = str2ts(start_date), str2ts(end_date)
        datas['stock'] = datas['stock'][(start_date <= datas['stock'].index) & (datas['stock'].index <= end_date)]
        datas['index'] = datas['index'][(start_date <= datas['index'].index) & (datas['index'].index <= end_date)]
        datas['info']  = datas['info'][datas['info'].listingdate.notnull() & (datas['info'].listingdate <= end_date)]
    return datas
def get_price(data, symbol, date, nearest=False):
    """주식의 가격을 가져옴

    :param cudf.Dataframe data: 주가 데이터
    :param str symbol: 주식의 종목명
    :param Timestamp date: 주식의 가격을 가져올 날짜
    :return: 주식의 가격
    :rtype: float|None
    """
    try:
        data_at_date = data.loc[date]
        return data_at_date[data_at_date.symbol == symbol].close[0]
    except:
        pass

    ## Time-consuming!
    if nearest:
        data_before_date = data.loc[data.index <= date]
        return data_before_date[data_before_date.symbol == symbol].iloc[-1].close[0]
    else:
        LOGGER.info(f"{date}에 {symbol} 값이 존재하지 않음")
        return
def select_datas(trading_date, raw_datas):
    """학습 데이터 선택

    :param str trading_date: 거래 날짜
    :param dict raw_datas: 전체 구간에 대한 데이터
    :return: 현재, 미래 구간이 제외된 학습 데이터
    :rtype: dict
    """
    ## 1. 학습 구간 추출
    datas = {}
    for data_id, data in raw_datas.items():
        if data_id in ['stock', 'index']:
            datas[data_id] = data.loc[data.index < trading_date]
        elif data_id == 'info':
            datas[data_id] = data.loc[data.listingdate.notnull() & (data.listingdate < trading_date)]
        else:
            raise ValueError(data_id)
    return datas


def plot_metrics(metrics, params, dates=None):
    """평가지표를 그래프로 표현

    :param pandas.DataFame metrics: 평가지표들
    :param dict params: parameters
    :param pandas.Index dates: 투자 기간
    """
    ## 1. Prepare data
    metrics = metrics.reset_index()

    ## 2. Plot
    fig, axes = plt.subplots(4, 3, figsize=params['FIGSIZE'])

    ## 2.1 Sharpe ratio
    sns.barplot(x='index', y='sharpe ratio', data=metrics, ax=axes[0, 0])
    sns.barplot(x='index', y='mean return', data=metrics, ax=axes[0, 1])
    sns.barplot(x='index', y='std return', data=metrics, ax=axes[0, 2])
    for ax in axes[0]:
        ax.xaxis.tick_top()

    ## 2.2 VWR
    sns.barplot(x='index', y='VWR', data=metrics, ax=axes[1, 0])
    sns.barplot(x='index', y='CAGR', data=metrics, ax=axes[1, 1])
    sns.barplot(x='index', y='variability', data=metrics, ax=axes[1, 2])

    ## 2.3 Information ratio
    sns.barplot(x='index', y='information ratio', data=metrics, ax=axes[2, 0])
    sns.barplot(x='index', y='mean excess return', data=metrics, ax=axes[2, 1])
    sns.barplot(x='index', y='std excess return', data=metrics, ax=axes[2, 2])

    ## 2.4 Maximum Drawdown
    sns.barplot(x='index', y='MDD', data=metrics, ax=axes[3, 0])
    axes[3, 1].axis('off')
    axes[3, 2].axis('off')

    ## 3. Options
    ## 3.1 x-axis
    for r in range(len(axes)):
        for c in range(len(axes[r])):
            ax = axes[r, c]
            if r > 0:
                ax.set_xticklabels([])
            try:
                ax.bar_label(ax.containers[0], label_type='center', fmt='%.3f')
            except:  # axis off
                pass
            ax.xaxis.tick_top()
            ax.set_xlabel(None)
            ax.set_axisbelow(True)
            ax.grid()


    ## 4. Show
    if dates is None:
        title = f"{metrics['index'][0]} vs {metrics['index'][1]}"
    else:
        title = f"{metrics['index'][0]} vs {metrics['index'][1]} ({ts2str(dates[0])} ~ {ts2str(dates[-1])})"
    fig.suptitle(title, fontsize=20, fontweight='bold')
    fig.tight_layout()
    generate_dir(PATH.RESULT)
    fig.savefig(join(PATH.RESULT, f"[metric] {title}.png"))
    fig.show()
    plt.close(fig)
def compare_prices(p1, p2, params, balances=None, stock_wealths=None):
    """
    Plot price data

    :param pd.Series p1: 비교값 1 (benchmark)
    :param pd.Series p2: 비교값 2 (algorithm)
    :param dict params: Parameters
    :param Sequence balances: 잔고, default=None
    :param Sequence stock_wealths: 주식 평가액, default=None
    """
    ## 1. Plot line plot
    ## 1.1 Generate figure and axes
    fig = plt.figure(figsize=params['FIGSIZE'])
    gs = GridSpec(3, 1, height_ratios=[2, 1, 1])
    ax_p1, ax_r, ax_c = fig.add_subplot(gs[0]), fig.add_subplot(gs[1]), fig.add_subplot(gs[2])
    plot_prices(p2, p1, params, ax_p1, fig)
    plot_ratio(prices2alpha(p2, p1), params, ax_r, fig)
    if balances is not None:
        plot_composition(p1.index, balances, stock_wealths, params, ax_c, fig)

    ## 2. Show
    title = f"{p1.name} vs {p2.name} ({ts2str(p1.index[0])} ~ {ts2str(p1.index[-1])})"
    fig.suptitle(title, fontsize=20, fontweight='bold')
    fig.tight_layout()
    generate_dir(PATH.RESULT)
    fig.savefig(join(PATH.RESULT, f"[price] {title}.png"))
    fig.show()
    plt.close(fig)
def compare_returns(r1, r2, params):
    """
    Plot return data

    :param pd.Series r1: 비교값 1 (benchmark)
    :param pd.Series r2: 비교값 2 (algorithm)
    :param dict params: Parameters
    """
    ## 1. Prepare data
    data = pd.DataFrame()
    for name, r in zip((r1.name, r2.name), (r1, r2)):
        data[name] = r
    min_global = np.min([r1, r2])
    max_global = np.max([r1, r2])
    max_abs    = np.max([abs(min_global), abs(max_global)])

    ## 2. Plot distribution of return
    fig, ax = plt.subplots(figsize=params['FIGSIZE'])
    ax.axvline(0, color='k', linestyle='--')
    sns.histplot(data, bins=100, kde=True, stat='probability', ax=ax)

    ## 3. Options
    ## 3.1 xlim
    ax.set_xlim(-max_abs, max_abs)
    ax.set_xticks(np.linspace(-max_abs, max_abs, 11))
    ax.set_xlabel('return', fontsize=15, fontweight='bold')
    ax.set_ylabel('probability density function', fontsize=15, fontweight='bold')

    ## 3.2 grid
    ax.grid()

    ## 4. Show
    title = f"{r1.name} vs {r2.name} ({ts2str(r1.index[0])} ~ {ts2str(r1.index[-1])})"
    fig.suptitle(title, fontsize=20, fontweight='bold')
    fig.tight_layout()
    generate_dir(PATH.RESULT)
    fig.savefig(join(PATH.RESULT, f"[return] {title}.png"))
    fig.show()
    plt.close(fig)


def plot_prices(p1, p2=None, params=None, ax=None, fig=None):
    """Plot prices

    :param pd.Series p1: 비교값 1
    :param pd.Series p2: 비교값 2
    :param dict params: parameters
    :param matplotlib.figure.Figure fig: figure, default=None
    """
    def plot_price(norm_p, ax, plot_params):
        sns.lineplot(data=norm_p, ax=ax, linewidth=2, label=norm_p.name, **plot_params)
        ax.axhline(1, color='k', linestyle='--')
    ## 1. Prepare data
    if ax is None and fig is None:
        new_fig = True
        fig, ax = plt.subplots(figsize=params['FIGSIZE'])
    else:
        new_fig = False
    ps      = [p1, p2]             if p2 is not None else [p1]
    norm_ps = [p1/p1[0], p2/p2[0]] if p2 is not None else [p1/p1[0]]
    axes    = [ax, ax.twinx()]     if p2 is not None else [ax]
    options = [{}, {'color': 'k'}] if p2 is not None else [{}]


    ## 2. Plot
    for norm_p, option in zip(norm_ps, options):
        plot_price(norm_p, axes[0], option)


    ## 3. Options
    ymin, ymax = np.min(norm_ps), np.max(norm_ps)
    for ax, norm_p, p in zip(axes, norm_ps, ps):
        ## 3.1 y-axis
        yticks = np.linspace(ymin, ymax, params['NYTICK'])
        yticks = sorted(np.append(yticks, norm_p[0]))
        if params['COUNTRY'] == 'kr':
            yticklabels = [f"{p[0]*ytick:,.0f}({ytick-1:.2f})" for ytick in yticks]
        else:
            yticklabels = [f"{p[0]*ytick:,.2f}({ytick-1:.2f})" for ytick in yticks]
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.set_ylim(ymin, ymax)
        ax.set_ylabel(f"{norm_p.name} (return)", fontsize=15, fontweight='bold')

        ## 3.2 x-axis
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
        ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[3, 5, 7, 9, 11]))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
        # ax.set_xlim(norm_p.index[0].strftime("%Y-%m-01"), norm_p.index[-1])
        ax.set_xlabel(None)  # date is 명백

        ## 3.3 grid
        ax.grid(True, linewidth=1)
        ax.grid(True, 'minor', linewidth=0.2)

    ## 3.4 legend
    axes[0].legend(loc='lower left', fontsize='x-large')

    ## 3.5 Adjust x-axis
    fig.autofmt_xdate(which='both')

    ## 4. Show if new figure
    if new_fig:
        fig.tight_layout()
        fig.show()
        plt.close(fig)
def plot_ratio(ratios, params, ax=None, fig=None):
    """Plot ratio
    """
    ## 1. Prepare data
    if ax is None and fig is None:
        new_fig = True
        fig, ax = plt.subplots(figsize=params['FIGSIZE'])
    else:
        new_fig = False


    ## 2. Plot
    sns.lineplot(data=ratios, ax=ax, linewidth=2, label='ratio')
    ax.axhline(1, color='k', linestyle='--')


    ## 3. Options
    ymin, ymax = np.min(ratios), np.max(ratios)

    ## 3.1 y-axis
    yticks = np.linspace(ymin, ymax, params['NYTICK'])
    yticks = sorted(np.append(yticks, ratios[0]))
    yticklabels = [f"{ytick:.3f}" for ytick in yticks]
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_ylim(ymin, ymax)
    ax.set_ylabel('ratio', fontsize=15, fontweight='bold')

    ## 3.2 x-axis
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[3, 5, 7, 9, 11]))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
    # ax.set_xlim(ratios.index[0].strftime("%Y-%m-01"), ratios.index[-1])
    ax.set_xlabel(None)  # date is 명백

    ## 3.3 grid
    ax.grid(True, linewidth=1)
    ax.grid(True, 'minor', linewidth=0.2)

    ## 3.4 legend
    ax.legend(loc='lower left', fontsize='x-large')

    ## 3.5 Adjust x-axis
    fig.autofmt_xdate(which='both')

    ## 4. Show if new figure
    if new_fig:
        fig.tight_layout()
        fig.show()
        plt.close(fig)
def plot_composition(dates, balances, stock_wealths, params, ax=None, fig=None):
    """Plot ratio
    """
    ## 1. Prepare data
    if ax is None and fig is None:
        new_fig = True
        fig, ax = plt.subplots(figsize=params['FIGSIZE'])
    else:
        new_fig = False


    ## 2. Plot
    ax.stackplot(dates, balances, stock_wealths, labels=['balance', 'stock wealth'])

    ## 3. Options
    ## 3.1 y-axis
    ax.set_ylabel("composition", fontsize=15, fontweight='bold')

    ## 3.2 x-axis
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[3, 5, 7, 9, 11]))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
    ax.set_xlabel(None)  # date is 명백

    ## 3.3 grid
    ax.grid(True, linewidth=1)
    ax.grid(True, 'minor', linewidth=0.2)

    ## 3.4 legend
    ax.legend(loc='lower left', fontsize='x-large')

    ## 3.5 Adjust x-axis
    fig.autofmt_xdate(which='both')

    ## 4. Show if new figure
    if new_fig:
        fig.tight_layout()
        fig.show()
        plt.close(fig)
