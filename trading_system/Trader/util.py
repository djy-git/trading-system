from common import *


def plot_result_price(benchmark_data, trading_result, title, params):
    """
    Plot price data

    :param pd.DataFrame benchmark_data: 벤치마크 데이터
    :param dict trading_result: 투자 결과
    :param str title: title
    :param dict params: Parameters
    """
    ## 0. Prepare data
    bp, br = benchmark_data['close'], benchmark_data['return']
    tp, tr = trading_result['net_wealth']['close'], trading_result['net_wealth']['return']

    norm_bp = bp / bp.iloc[0]
    norm_tp = tp / tp.iloc[0]

    ## 1. Plot lineplot
    ## 1.1 Generate figure and axes
    gs = GridSpec(2, 1, height_ratios=[2, 1])
    fig = plt.figure(figsize=params['FIGSIZE'])
    ax_b, ax_a = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])  # b(enchmark), a(lpha)
    ax_t = ax_b.twinx()  # t(rading algorithm)

    ## 1.2 Plot benchmark vs trading algorithm
    for label, data, p, r in zip((params['BENCHMARK'], "Trading algorithm"), (norm_bp, norm_tp), (bp, tp), (br, tr)):
        options = {'color': 'k'} if data is norm_bp else {}
        sns.lineplot(data=data, ax=ax_b, linewidth=2, label=label, **options)
    ax_b.axhline(norm_bp[0], color='k', linestyle='--')
    sns.lineplot(data=norm_tp/norm_bp, ax=ax_a, linewidth=2, label='Alpha')
    ax_a.axhline(1, color='k', linestyle='--')


    ## 2. Options
    ## 2.1 yticks
    ymin, ymax = min(norm_bp.min(), norm_tp.min()), max(norm_bp.max(), norm_tp.max())
    for ax, p, norm_p, name in zip((ax_b, ax_t), (bp, tp), (norm_bp, norm_tp), (params['BENCHMARK'], 'net wealth')):
        yticks = np.linspace(ymin, ymax, 10)
        yticks = sorted(np.append(yticks, norm_p[0]))
        if params['COUNTRY'] == 'kr':
            yticklabels = [f"{p[0]*ytick:,.0f}({ytick-1:.2f})" for ytick in yticks]
        else:
            yticklabels = [f"{p[0]*ytick:,.2f}({ytick-1:.2f})" for ytick in yticks]
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.set_ylim(ymin, ymax)

        ## 2.2 ylabel
        ax.set_ylabel(f"{name} (return)", fontsize=15, fontweight='bold')
    ax_a.set_ylabel(f"Alpha (algorithm / {params['BENCHMARK']})", fontsize=10, fontweight='bold')

    for ax in (ax_a, ax_b):
        ## 2.3 xticks
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
        ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[3, 5, 7, 9, 11]))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
        ax.set_xlabel(None)

        ## 2.4 grid
        ax.grid(True, linewidth=1)
        ax.grid(True, 'minor', linewidth=0.2)

        ## 2.5 legend
        ax.legend(loc='upper left', fontsize='x-large')
    fig.autofmt_xdate(which='both')

    ## 2.6 title
    fig.suptitle(title, fontsize=20, fontweight='bold')


    ## 3. Show
    fig.tight_layout()
    fig.savefig(join(PATH.RESULT, f"{title}_price.png"))
    fig.show()
    plt.close(fig)
def plot_result_return(benchmark_data, trading_result, title, params):
    """
    Plot return data

    :param pd.DataFrame benchmark_data: 벤치마크 데이터
    :param dict trading_result: 투자 결과
    :param str title: title
    :param dict params: Parameters
    """
    ## 1. Prepare data
    br, tr = benchmark_data['return'], trading_result['net_wealth']['return']
    tr.iloc[0] = 0  # nan 처리

    data = pd.DataFrame()
    for label, d in zip((params['BENCHMARK'], "Trading algorithm"), (br, tr)):
        data[label] = d
    min_global = np.min([br, tr])
    max_global = np.max([br, tr])
    max_abs    = np.max([abs(min_global), abs(max_global)])

    ## 2. Plot distribution of return
    fig, ax = plt.subplots(figsize=np.array(params['FIGSIZE'])//2)
    ax.axvline(0, color='k', linestyle='--')
    sns.histplot(data, bins=100, kde=True, stat='probability', ax=ax)

    ## 3. Options
    ## 3.1 xlim
    ax.set_xlim(-max_abs, max_abs)
    ax.set_xticks(np.linspace(-max_abs, max_abs, 11))
    ax.set_xlabel('return', fontsize=15, fontweight='bold')
    ax.set_ylabel('probabiliby density', fontsize=15, fontweight='bold')

    ## 3.2 grid
    ax.grid()

    ## 3.3 Title
    fig.suptitle(title, fontsize=20, fontweight='bold')

    ## 4. Show
    fig.tight_layout()
    fig.savefig(join(PATH.RESULT, f"{title}_return.png"))
    fig.show()
    plt.close(fig)

def plot_metrics(metrics, title, params):
    """평가지표를 그래프로 표현
    
    :param pd.DataFame metrics: 평가지표들
    :param str title: title
    :param dict params: parameters
    """
    ## 1. Prepare data
    metrics = metrics.reset_index()

    ## 2. Plot
    fig, axes = plt.subplots(4, 3, figsize=np.array(params['FIGSIZE'])//2)

    ## 2.1 Sharpe ratio
    sns.barplot(x='index', y='sharpe_ratio', data=metrics, ax=axes[0, 0])
    sns.barplot(x='index', y='mean_return', data=metrics, ax=axes[0, 1])
    sns.barplot(x='index', y='std_return', data=metrics, ax=axes[0, 2])
    for ax in axes[0]:
        ax.xaxis.tick_top()

    ## 2.2 VWR
    sns.barplot(x='index', y='VWR', data=metrics, ax=axes[1, 0])
    sns.barplot(x='index', y='CAGR', data=metrics, ax=axes[1, 1])
    sns.barplot(x='index', y='variability', data=metrics, ax=axes[1, 2])

    ## 2.3 Information ratio
    sns.barplot(x='index', y='information_ratio', data=metrics, ax=axes[2, 0])
    sns.barplot(x='index', y='mean_excess_return', data=metrics, ax=axes[2, 1])
    sns.barplot(x='index', y='std_excess_return', data=metrics, ax=axes[2, 2])

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

    ## 3.2 Title
    fig.suptitle(title, fontsize=20, fontweight='bold')


    ## 4. Show
    fig.tight_layout()
    fig.savefig(join(PATH.RESULT, f"{title}_metric.png"))
    fig.show()
    plt.close(fig)
