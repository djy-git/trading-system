from common import *
import matplotlib.dates as mdates


def plot_result(benchmark_data, trading_result, params):
    """
    Plot price data

    :param pd.DataFrame benchmark_data: 벤치마크 데이터
    :param dict trading_result: 투자 결과
    """
    ## 0. Prepare data
    benchmark_name = benchmark_data.symbol.unique()[0]
    bp = benchmark_data.close
    tp = trading_result['net_wealth'].close

    norm_bp = bp / bp.iloc[0]
    norm_tp = tp / tp.iloc[0]

    ## 1. Plot lineplot
    ## 1.1 Generate figure and axes
    gs = GridSpec(2, 1, height_ratios=[2, 1])
    fig = plt.figure(figsize=params['FIGSIZE'])
    ax_b, ax_a = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])  # b(enchmark), a(lpha)
    ax_t = ax_b.twinx()  # t(rading algorithm)

    ## 1.2 Plot benchmark vs trading algorithm
    sns.lineplot(data=norm_bp, ax=ax_b, linewidth=2, label=benchmark_name, color='k')
    sns.lineplot(data=norm_tp, ax=ax_b, linewidth=2, label='Trading algorithm')
    ax_b.axhline(norm_bp[0], color='k', linestyle='--')

    sns.lineplot(data=norm_tp/norm_bp, ax=ax_a, linewidth=2, label='Alpha')
    ax_a.axhline(1, color='k', linestyle='--')


    ## 2. Options
    ## 2.1 yticks
    ymin, ymax = min(norm_bp.min(), norm_tp.min()), max(norm_bp.max(), norm_tp.max())
    for ax, p, norm_p, name in zip((ax_b, ax_t), (bp, tp), (norm_bp, norm_tp), ('benchmark', 'net wealth')):
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
    ax_a.set_ylabel("Alpha (trading / benchmark)", fontsize=15, fontweight='bold')


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
    title = f"Trading algorithm vs {benchmark_name} ({dt2str(benchmark_data.index[0])} ~ {dt2str(benchmark_data.index[-1])})"
    fig.suptitle(title, fontsize=20, fontweight='bold')

    ## 2.7 tight layout
    fig.tight_layout()


    ## 3. Show
    fig.show()
    plt.close(fig)
