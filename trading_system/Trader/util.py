from common import *


def plot_metrics(metrics, title, params):
    """평가지표를 그래프로 표현

    :param pd.DataFame metrics: 평가지표들
    :param str title: title
    :param dict params: parameters
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
    fig.suptitle(title, fontsize=20, fontweight='bold')
    fig.tight_layout()
    generate_dir(PATH.RESULT)
    fig.savefig(join(PATH.RESULT, f"{title}_metric.png"))
    fig.show()
    plt.close(fig)
def plot_result_price(trading_result, params):
    bp = pd.Series(trading_result.benchmark, name=params['BENCHMARK'])
    tp = pd.Series(trading_result.net_wealth, name=params['ALGORITHM'])
    compare_prices(bp, tp, params, trading_result.balance, trading_result.stock_wealth)

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
    if balances is not None:
        gs = GridSpec(3, 1, height_ratios=[2, 1, 1])
        ax_p1, ax_r, ax_c = fig.add_subplot(gs[0]), fig.add_subplot(gs[1]), fig.add_subplot(gs[2])
        plot_prices(p2, p1, params, ax_p1, fig)
        plot_ratio(prices2alpha(p2, p1), params, ax_r, fig)
        plot_composition(p1.index, balances, stock_wealths, params, ax_c, fig)
    else:
        gs = GridSpec(2, 1, height_ratios=[2, 1])
        ax_p1, ax_r = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
        plot_prices(p2, p1, params, ax_p1, fig)
        plot_ratio(prices2alpha(p2, p1), params, ax_r, fig)


    ## 2. Show
    title = f"{p2.name} vs {p1.name} ({dt2str(p1.index[0])} ~ {dt2str(p1.index[-1])})"
    fig.suptitle(title, fontsize=20, fontweight='bold')
    fig.tight_layout()
    generate_dir(PATH.RESULT)
    fig.savefig(join(PATH.RESULT, f"{title}_price.png"))
    fig.show()
    plt.close(fig)
def plot_result_return(trading_result, title, params):
    """
    Plot return data

    :param pd.DataFrame trading_result: 투자 결과
    :param str title: title
    :param dict params: Parameters
    """
    ## 1. Prepare data
    br, tr = trading_result.benchmark_return, trading_result['return']
    tr.iloc[0] = 0  # nan 처리

    data = pd.DataFrame()
    for label, d in zip((params['BENCHMARK'], params['ALGORITHM']), (br, tr)):
        data[label] = d
    min_global = np.min([br, tr])
    max_global = np.max([br, tr])
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
    fig.suptitle(title, fontsize=20, fontweight='bold')
    fig.tight_layout()
    generate_dir(PATH.RESULT)
    fig.savefig(join(PATH.RESULT, f"{title}_return.png"))
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
        ax.axhline(1, color='k', linestyle='--')
        sns.lineplot(data=norm_p, ax=ax, linewidth=2, label=norm_p.name, **plot_params)
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
        yticks = np.linspace(ymin, ymax, 10)
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
        ax.set_xlim(norm_p.index[0], norm_p.index[-1])
        ax.set_xmargin(0.05)
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
    ax.axhline(1, color='k', linestyle='--')
    sns.lineplot(data=ratios, ax=ax, linewidth=2, label='ratio')


    ## 3. Options
    ymin, ymax = np.min(ratios), np.max(ratios)

    ## 3.1 y-axis
    yticks = np.linspace(ymin, ymax, 10)
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
    ax.set_xlim(ratios.index[0], ratios.index[-1])
    ax.set_xmargin(0.05)
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
    ax.set_xlim(dates[0], dates[-1])
    ax.set_xmargin(0.05)
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
