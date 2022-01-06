from common import *
import matplotlib.dates as mdates


def plot_price(data):
    """
    Plot price data

    :param pd.DataFrame data: 주가
    """
    ## 1. Plot lineplot
    fig, ax = plt.subplots(figsize=(10, 10))
    label = f"{data.symbol.unique()[0]} ({dt2str(data.index[0])} ~ {dt2str(data.index[-1])})"
    sns.lineplot(data=data.close, ax=ax, linewidth=2, label=label, color='k')
    ax.axhline(data.close[0], color='k', linestyle='--')

    ## 2. Options
    ## 2.1 xticks
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[3, 5, 7, 9, 11]))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
    fig.autofmt_xdate(which='both')

    ## 2.2 yticks
    yticks = np.linspace(data.close.min(), data.close.max(), 10)
    yticks = sorted(np.append(yticks, data.close[0]))
    yticklabels = [f"{ytick:.2f}({ytick/data.close[0]:.2f})" for ytick in yticks]
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)

    ## 2.3 grid
    ax.grid(True, linewidth=1)
    ax.grid(True, 'minor', linewidth=0.2)

    ## 2.4 legend
    ax.legend(loc='upper left')

    ## 2.5 xlabel
    ax.set_xlabel(None)
    ax.set_ylabel("close price (ratio)")

    ## 2.6 tight layout
    fig.tight_layout()


    ## 3. Show
    fig.show()
    plt.close(fig)
