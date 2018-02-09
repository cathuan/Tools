"""
We assume
- the index is ["date", "symbol"]
- the params columns are with level 0 index "Parameters"
- the pnl column is with level 0 index "Pnl"
- the delta column is with level 0 index "Delta"
"""
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats


def get_daily_pnls(df):
    """Return a pandas dataframe with index "date" and values 'pnl on the date'
    """
    s_daily_pnls = df["Pnl"].reset_index().groupby("date")["pnl"].sum()
    return s_daily_pnls


def get_daily_deltas(df):
    """Return a pandas dataframe with index "date" and values 'delta on the date'
    """
    s_daily_deltas = df["Delta"].reset_index().groupby("date")["delta"].sum()
    return s_daily_deltas


def get_daily_abs_deltas(df):
    """Return a pandas dataframe with index "date" and values 'abs delta on the date'
    """
    s_abs_deltas = df["Delta"]["delta"].apply(abs)
    s_abs_deltas.index = df.index
    s_daily_abs_deltas = s_abs_deltas.reset_index().groupby("date").sum()["delta"]
    return s_daily_abs_deltas


def get_drawdowns(df):
    df_daily_pnls = get_daily_pnls(df)
    drawdowns = []
    drawdown = 0
    for pnl in df_daily_pnls.values:
        drawdown += pnl
        if drawdown >= 0:
            drawdown = 0
        drawdowns.append(drawdown)
    df_drawdowns = pd.DataFrame(drawdowns)
    df_drawdowns.index = df_daily_pnls.index
    df_drawdowns.columns = ["drawdown"]
    return df_drawdowns["drawdown"]


def plot_fill_between(ax, series):
    ax.fill_between(series.index, 0, series, color="r")


# summary 1
def summarize_daily_pnl(df):
    # daily pnls
    s_daily_pnls = get_daily_pnls(df)
    daily_pnl_mean = s_daily_pnls.mean()
    daily_pnl_stddev = s_daily_pnls.std()
    k2_statistics, normal_test_p_value = scipy.stats.mstats.normaltest(s_daily_pnls)
    print "Daily Pnl Summary: daily pnl mean: $%.2f" % daily_pnl_mean
    print "Daily Pnl Summary: daily pnl stddev: $%.2f" % daily_pnl_stddev
    print "Daily Pnl Summary: daily pnl sharpe ratio: %.2f" % (daily_pnl_mean * 1.0 / daily_pnl_stddev)
    print "Daily Pnl Summary: daily pnl max win: $%.2f" % s_daily_pnls.max()
    print "Daily Pnl Summary: daily pnl max loss: $%.2f" % s_daily_pnls.min()
    print "Daily Pnl Summary: daily pnl normal test p-value: %.4f" % normal_test_p_value

    s_daily_pnls.to_frame().hist(bins=range(-500, 500, 10))
    plt.savefig("daily_pnl_histogram.png")


# summary 2
def summarize_daily_pnl_in_bps(df):
    # daily pnl in bps
    s_daily_pnls = get_daily_pnls(df)
    s_daily_abs_deltas = get_daily_abs_deltas(df)
    s_daily_bps = s_daily_pnls * 10000.0 / s_daily_abs_deltas
    daily_bps_mean = s_daily_bps.mean()
    daily_bps_stddev = s_daily_bps.std()
    k2_statistics, normal_test_p_value = scipy.stats.mstats.normaltest(s_daily_bps)
    print "Daily Pnl in bps Summary: daily pnl in bps mean: %.2f" % daily_bps_mean
    print "Daily Pnl in bps Summary: daily pnl in bps stddev: %.2f" % daily_bps_stddev
    print "Daily Pnl in bps Summary: daily pnl in bps normal test p-value: %.4f" % normal_test_p_value

    s_daily_bps.to_frame().hist(bins=range(-50, 50))
    plt.savefig("daily_bps_histogram.png")


# summary 3
def summarize_daily_abs_delta(df):
    s_daily_abs_delta = get_daily_abs_deltas(df)
    daily_abs_delta_mean = s_daily_abs_delta.mean()
    print "Daily abs delta Summary: daily abs delta mean: $%d" % daily_abs_delta_mean
    print "Daily abs delta Summary: max daily abs delta: $%d" % s_daily_abs_delta.max()
    print "Daily abs delta Summary: min daily abs delta: $%d" % s_daily_abs_delta.min()


# summary 4
def summarize_daily_delta(df):
    s_daily_delta = get_daily_deltas(df)
    daily_delta_mean = s_daily_delta.mean()
    print "Daily delta Summary: daily delta mean: $%d" % daily_delta_mean
    print "Daily delta Summary: max daily delta: $%d" % s_daily_delta.max()
    print "Daily delta Summary: min daily delta: $%d" % s_daily_delta.min()


# summary 5
def summarize_drawdown(df):
    s_drawdown = get_drawdowns(df)
    print "Drawdown Summary: max drawdown: $%.2f" % s_drawdown.min()

    plot_fill_between(plt, s_drawdown)
    plt.savefig("drawdown.png")


def plot(df):

    df_daily_pnls = get_daily_pnls(df)
    df_drawdowns = get_drawdowns(df_daily_pnls)
    df_daily_deltas = get_daily_deltas(df)
    df_daily_abs_deltas = get_daily_abs_deltas(df)

    fig, axes = plt.subplots(nrows=4, sharex=True)

    df_daily_pnls.cumsum().plot(ax=axes[0])
    axes[0].set_title("pnl curve")
    axes[0].set_ylabel("pnl in $")

    plot_fill_between(axes[1], df_drawdowns["drawdown"])
    axes[1].set_title("drawdown")
    axes[1].set_ylabel("drawdown in $")

    df_daily_deltas.plot(ax=axes[2])
    axes[2].set_title("daily delta")
    axes[2].set_ylabel("delta in $")

    df_daily_abs_deltas.plot(ax=axes[3])
    axes[3].set_title("daily abs delta")
    axes[3].set_ylabel("abs delta in $")

    plt.show()


if __name__ == "__main__":

    df = pd.read_csv("pnls.csv", header=[0, 1], index_col=[0, 1])
    summarize_daily_pnl(df)
    summarize_daily_pnl_in_bps(df)
    summarize_daily_delta(df)
    summarize_daily_abs_delta(df)
    summarize_drawdown(df)
