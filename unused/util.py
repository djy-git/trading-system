def get_metrics_ts(price_benchmark, price_algorithm, params):
    """Benchmark 데이터와 투자 결과에 대한 평가지표 시계열 계산

    :param pd.Series price_benchmark: 벤치마크 가격
    :param pd.Series price_algorithm: 알고리즘 가격
    :param dict params: parameters
    :return: 평가지표 시계열
    :rtype: pandas.DataFrame
    """
    ## 0. Prepare data
    ps    = price_benchmark.values, price_algorithm.values
    rs    = price2return(price_benchmark).values, price2return(price_algorithm).values
    names = [params['BENCHMARK'], params['ALGORITHM']]
    dates = price_benchmark.index

    def task(idx, date, ps, rs, names):
        if idx < 20:
            emptys = [0, 0]
            return pd.DataFrame({'name': names, 'Sharpe ratio': emptys, 'VWR': emptys, 'MDD': emptys, 'Information ratio': emptys}, index=2*[date])
        else:
            return pd.DataFrame({'name'             : names,
                                 'Sharpe ratio'     : [get_ratio(r[:idx+1])[0] for r in rs],
                                 'VWR'              : [get_VWR(p[:idx+1])[0] for p in ps],
                                 'MDD'              : [get_MDD(p[:idx+1]) for p in ps],
                                 'Information ratio': [None, get_ratio(rs[1][:idx+1] - rs[0][:idx+1])[0]]}, index=2*[date])
    tasks  = [delayed(task)(idx, date, ps, rs, names) for idx, date in enumerate(dates)]
    return pd.concat(exec_parallel(tasks, params['DEBUG']))
def plot_metrics_time_series(metrics_ts, params, ax=None, fig=None):
    """Plot metric

    :param pd.DataFrame metrics_ts: 평가지표
    :param dict params: parameters
    :param matplotlib.axes.Axes ax: ax
    :param matplotlib.figure.Figure fig: figure
    """
    pass

    fig, ax = plt.subplots(figsize=params['FIGSIZE'])
    ax2 = ax.twinx()

    sns.lineplot(data=metrics_ts[metrics_ts.name == params['BENCHMARK']]['Sharpe ratio'], ax=ax, linewidth=2, label=params['BENCHMARK'] + "(Sharpe ratio)")
    sns.lineplot(data=metrics_ts[metrics_ts.name == params['ALGORITHM']]['Sharpe ratio'], ax=ax, linewidth=2, label=params['ALGORITHM'] + "(Sharpe ratio)")

    sns.lineplot(data=metrics_ts[metrics_ts.name == params['BENCHMARK']]['VWR'], ax=ax2, linestyle='--', linewidth=2, label=params['BENCHMARK'] + "(Sharpe ratio)")
    sns.lineplot(data=metrics_ts[metrics_ts.name == params['ALGORITHM']]['VWR'], ax=ax2, linestyle='--', linewidth=2, label=params['ALGORITHM'] + "(Sharpe ratio)")

    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.grid()
    plt.tight_layout()
    plt.show()


    # def plot_price(p, ax, plot_params):
    #     ax.axhline(1, color='k', linestyle='--')
    #     sns.lineplot(data=p, ax=ax, linewidth=2, label=p.name, ci=None, **plot_params)
    #     sns.lineplot(data=p, ax=ax, linewidth=2, label=p.name, ci=None, **plot_params)
    # ## 1. Prepare data
    # if ax is None and fig is None:
    #     new_fig = True
    #     fig, ax = plt.subplots(figsize=params['FIGSIZE'])
    # else:
    #     new_fig = False
    # ps      = [metrics_ts, metrics_ts]
    # axes    = [ax, ax.twinx()]
    # options = [{}, {}]
    #
    #
    # ## 2. Plot
    # for p, option in zip(ps, options):
    #     plot_price(p, axes[0], option)
    #
    #
    # ## 3. Options
    # ymin, ymax = np.min(ps), np.max(ps)
    # for ax, p in zip(axes, ps):
    #     ## 3.1 y-axis
    #     yticks = np.linspace(ymin, ymax, params['NYTICK'])
    #     yticks = sorted(np.append(yticks, p[0]))
    #     yticklabels = [f"{ytick:.3f}" for ytick in yticks]
    #     ax.set_yticks(yticks)
    #     ax.set_yticklabels(yticklabels)
    #     ax.set_ylim(ymin, ymax)
    #     ax.set_ylabel(p.name, fontsize=15, fontweight='bold')
    #
    #     ## 3.2 x-axis
    #     ax.xaxis.set_major_locator(mdates.YearLocator())
    #     ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
    #     ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[3, 5, 7, 9, 11]))
    #     ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m'))
    #     ax.set_xlim(p.index[0], p.index[-1])
    #     ax.set_xmargin(0.05)
    #     ax.set_xlabel(None)  # date is 명백
    #
    #     ## 3.3 grid
    #     ax.grid(True, linewidth=1)
    #     ax.grid(True, 'minor', linewidth=0.2)
    #
    # ## 3.4 legend
    # axes[0].legend(loc='lower left', fontsize='x-large')
    #
    # ## 3.5 Adjust x-axis
    # fig.autofmt_xdate(which='both')
    #
    # ## 4. Show if new figure
    # if new_fig:
    #     fig.tight_layout()
    #     fig.show()
    #     plt.close(fig)