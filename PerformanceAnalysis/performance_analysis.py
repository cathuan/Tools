"""
We assume
- the index is ["date", "symbol"]
- the params columns are with level 0 index "Parameters"
- the pnl column is with level 0 index "Pnl"
- the delta column is with level 0 index "Delta"
"""
import pandas as pd
import matplotlib.pyplot as plt


def get_daily_pnls(df):
    df_daily_pnls = df["Pnl"].reset_index().groupby("date")["pnl"].sum()
    return df_daily_pnls


def get_daily_deltas(df):

    df_daily_deltas = df["Delta"].reset_index().groupby("date")["delta"].sum()
    return df_daily_deltas


def get_daily_abs_deltas(df):
    df_abs_deltas = df["Delta"]["delta"].apply(abs)
    df_abs_deltas.index = df.index
    df_daily_abs_deltas = df_abs_deltas.reset_index().groupby("date").sum()
    return df_daily_abs_deltas


def get_drawdowns(df_daily_pnls):

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
    return df_drawdowns


def plot_fill_between(ax, series):
    ax.fill_between(series.index, 0, series, color="r")


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

    df = pd.read_csv("data.csv", header=[0,1], index_col=[0,1])
    plot(df)
