from common import *
import matplotlib.dates as mdates


def plot_result(benchmark_data, trading_result):
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
    fig, ax_left = plt.subplots(figsize=(20, 10))
    ax_right = ax_left.twinx()

    ## 1.2 Plot benchmark vs trading algorithm
    sns.lineplot(data=norm_bp, ax=ax_left, linewidth=2, label=benchmark_name, color='k')
    sns.lineplot(data=norm_tp, ax=ax_left, linewidth=2, label='Trading algorithm')
    ax_left.axhline(norm_bp[0], color='k', linestyle='--')


    ## 2. Options
    ## 2.1 xticks (common)
    ax_left.xaxis.set_major_locator(mdates.YearLocator())
    ax_left.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
    ax_left.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[3, 5, 7, 9, 11]))
    ax_left.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
    fig.autofmt_xdate(which='both')
    ax_left.set_xlabel(None)

    ymin, ymax = min(norm_bp.min(), norm_tp.min()), max(norm_bp.max(), norm_tp.max())
    for ax, p, norm_p, name in zip((ax_left, ax_right), (bp, tp), (norm_bp, norm_tp), ('benchmark', 'net wealth')):
        ## 2.2 yticks
        yticks = np.linspace(ymin, ymax, 10)
        yticks = sorted(np.append(yticks, norm_p[0]))
        yticklabels = [f"{p[0]*ytick:,.2f}({ytick-1:.2f})" for ytick in yticks]
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.set_ylim(ymin, ymax)

        ## 2.3 grid
        ax.grid(True, linewidth=1)
        ax.grid(True, 'minor', linewidth=0.2)

        ## 2.4 ylabel
        ax.set_ylabel(f"{name} (return)")

    ## 2.5 legend
    ax_left.legend(loc='upper left', fontsize='x-large')

    ## 2.6 title
    title = f"Trading vs {benchmark_name} ({dt2str(benchmark_data.index[0])} ~ {dt2str(benchmark_data.index[-1])})"
    plt.title(title, fontsize=20, fontweight='bold')

    ## 2.7 tight layout
    fig.tight_layout()


    ## 3. Show
    fig.show()
    plt.close(fig)
