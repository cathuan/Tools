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
import datetime
from collections import namedtuple
import numpy as np
from HTMLPlotter import HTMLPlotter


class InterdayPnlSummary(object):

    PnlRecord = namedtuple("PnlRecord", ["date", "symbol", "pnl", "abs_delta", "delta", "side"])

    def __init__(self):
        self.exchange_rates = {"yen": 0.01, "usd": 1, "aud": 1}
        self.pnl_records = []

    def on_pnl(self, date, symbol, pnl, abs_delta, unit_of_currency, side):
        assert isinstance(date, datetime.date), "date must be a datetime.date object. But it's %s" % type(date)
        assert isinstance(symbol, str)
        assert unit_of_currency in ["yen", "usd", "aud", "krw", "twd", "nzd"]
        assert side in ["B", "S"]
        assert abs_delta >= 0

        exchange_rate = self.exchange_rates[unit_of_currency]
        pnl = pnl * exchange_rate
        abs_delta = abs_delta * exchange_rate
        sign = 1 if side == "B" else -1
        delta = abs_delta * sign
        self.pnl_records.append(self.PnlRecord(date, symbol, pnl, abs_delta, delta, side))

    def get_pnl_dataframe(self):
        dates = [record.date for record in self.pnl_records]
        symbols = [record.symbol for record in self.pnl_records]
        pnls = [record.pnl for record in self.pnl_records]
        deltas = [record.delta for record in self.pnl_records]
        abs_deltas = [record.abs_delta for record in self.pnl_records]
        sides = [record.side for record in self.pnl_records]
        df = pd.DataFrame(np.array([dates, symbols, pnls, deltas, abs_deltas, sides]).transpose())
        df.columns = ["date", "symbol", "pnl", "delta", "abs_delta", "side"]
        for col in ["pnl", "delta", "abs_delta"]:
            df[col] = df[col].apply(float)
        df = df.set_index(["date", "symbol"])
        return df

    def get_daily_pnls_series(self):
        """Return a pandas dataframe with index "date" and values 'pnl on the date'
        """
        df = self.get_pnl_dataframe()
        s_daily_pnls = df.reset_index().groupby("date")["pnl"].sum()
        return s_daily_pnls

    def get_daily_deltas_series(self):
        """Return a pandas dataframe with index "date" and values 'delta on the date'
        """
        df = self.get_pnl_dataframe()
        s_daily_deltas = df.reset_index().groupby("date")["delta"].sum()
        return s_daily_deltas

    def get_daily_abs_deltas_series(self):
        """Return a pandas dataframe with index "date" and values 'abs delta on the date'
        """
        df = self.get_pnl_dataframe()
        s_daily_abs_deltas = df.reset_index().groupby("date")["abs_delta"].sum()
        return s_daily_abs_deltas

    def get_drawdowns_series(self):
        drawdowns = []
        drawdown = 0
        s_daily_pnls = self.get_daily_pnls_series()
        for pnl in s_daily_pnls.values:
            drawdown += pnl
            if drawdown >= 0:
                drawdown = 0
            drawdowns.append(drawdown)
        df_drawdowns = pd.DataFrame(drawdowns)
        df_drawdowns.index = s_daily_pnls.index
        df_drawdowns.columns = ["drawdown"]
        s_drawdowns = df_drawdowns["drawdown"]
        return s_drawdowns

    def get_daily_trades_series(self):

        df = self.get_pnl_dataframe()
        s_daily_trades = df.reset_index().groupby("date")["pnl"].count()
        return s_daily_trades

    def get_pnl_by_symbols_series(self):
        df = self.get_pnl_dataframe()
        s_pnl_by_symbols = df.reset_index().groupby("symbol")["pnl"].sum()
        return s_pnl_by_symbols

    def get_trades_by_symbol_series(self):

        df = self.get_pnl_dataframe()
        s_trades_by_symbol = df.reset_index().groupby("symbol")["pnl"].count()
        return s_trades_by_symbol

    def summarize_daily_pnl(self):
        # daily pnls
        s_daily_pnls = self.get_daily_pnls_series()
        daily_pnl_mean = s_daily_pnls.mean()
        daily_pnl_stddev = s_daily_pnls.std()
        k2_statistics, normal_test_p_value = scipy.stats.mstats.normaltest(s_daily_pnls)
        print "Daily Pnl Summary: daily pnl mean: $%.2f" % daily_pnl_mean
        print "Daily Pnl Summary: daily pnl stddev: $%.2f" % daily_pnl_stddev
        print "Daily Pnl Summary: daily pnl sharpe ratio: %.2f" % (daily_pnl_mean * 1.0 / daily_pnl_stddev)
        print "Daily Pnl Summary: daily pnl max win: $%.2f" % s_daily_pnls.max()
        print "Daily Pnl Summary: daily pnl max loss: $%.2f" % s_daily_pnls.min()
        print "Daily Pnl Summary: daily pnl normal test p-value: %.4f" % normal_test_p_value

    def summarize_daily_pnl_in_bps(self):
        # daily pnl in bps
        s_daily_pnls = self.get_daily_pnls_series()
        s_daily_abs_deltas = self.get_daily_abs_deltas_series()
        s_daily_bps = s_daily_pnls * 10000.0 / s_daily_abs_deltas
        daily_bps_mean = s_daily_bps.mean()
        daily_bps_stddev = s_daily_bps.std()
        k2_statistics, normal_test_p_value = scipy.stats.mstats.normaltest(s_daily_bps)
        print "Daily Pnl in bps Summary: daily pnl in bps mean: %.2f" % daily_bps_mean
        print "Daily Pnl in bps Summary: daily pnl in bps stddev: %.2f" % daily_bps_stddev
        print "Daily Pnl in bps Summary: daily pnl in bps normal test p-value: %.4f" % normal_test_p_value

    def summarize_daily_abs_delta(self):
        s_daily_abs_delta = self.get_daily_abs_deltas_series()
        daily_abs_delta_mean = s_daily_abs_delta.mean()
        print "Daily abs delta Summary: daily abs delta mean: $%d" % daily_abs_delta_mean
        print "Daily abs delta Summary: max daily abs delta: $%d" % s_daily_abs_delta.max()
        print "Daily abs delta Summary: min daily abs delta: $%d" % s_daily_abs_delta.min()

    def summarize_daily_delta(self):
        s_daily_delta = self.get_daily_deltas_series()
        daily_delta_mean = s_daily_delta.mean()
        print "Daily delta Summary: daily delta mean: $%d" % daily_delta_mean
        print "Daily delta Summary: max daily delta: $%d" % s_daily_delta.max()
        print "Daily delta Summary: min daily delta: $%d" % s_daily_delta.min()

    def summarize_daily_trades(self):
        s_daily_trades = self.get_daily_trades_series()
        print "Daily count Summary: daily count mean: %.1f" % s_daily_trades.mean()
        print "Daily count Summary: max daily count: %d" % s_daily_trades.max()
        print "Daily count Summary: min daily count: %d" % s_daily_trades.min()

    def summarize_pnl_by_symbols(self):

        s_pnl_by_symbols = self.get_pnl_by_symbols_series()
        print "Pnl Summary by Symbols: max pnl $%d in symbol %s" % (s_pnl_by_symbols.max(), s_pnl_by_symbols.idxmax())
        print "Pnl Summary by Symbols: min pnl $%d in symbol %s" % (s_pnl_by_symbols.min(), s_pnl_by_symbols.idxmin())

    def summarize_trades_by_symbols(self):
        s_trades_by_symbol = self.get_trades_by_symbol_series()
        print "Trades Summary by Symbols: max symbol count: %d" % s_trades_by_symbol.max()
        print "Trades Summary by Symbols: min symbol count: %d" % s_trades_by_symbol.min()

    def summarize_drawdown(self):
        s_drawdowns = self.get_drawdowns_series()
        print "Drawdown Summary: max drawdown: $%.2f" % s_drawdowns.min()

    def summarize(self):
        self.summarize_daily_pnl()
        self.summarize_daily_trades()
        self.summarize_daily_pnl_in_bps()
        self.summarize_daily_delta()
        self.summarize_daily_abs_delta()
        self.summarize_drawdown()
        self.summarize_pnl_by_symbols()
        self.summarize_trades_by_symbols()

    def plot(self):

        s_daily_pnls = self.get_daily_pnls_series()
        s_drawdowns = self.get_drawdowns_series()
        s_daily_deltas = self.get_daily_deltas_series()
        s_daily_abs_deltas = self.get_daily_abs_deltas_series()

        fig, axes = plt.subplots(nrows=4, sharex=True)

        axes[0].plot(s_daily_pnls.index, s_daily_pnls.cumsum())
        axes[0].set_title("pnl curve")
        axes[0].set_ylabel("pnl in $")

        axes[1].fill_between(s_daily_pnls.index, 0, s_drawdowns, color="r")
        axes[1].set_title("drawdown")
        axes[1].set_ylabel("drawdown in $")

        axes[2].plot(s_daily_deltas.index, s_daily_deltas)
        axes[2].set_title("daily delta")
        axes[2].set_ylabel("delta in $")

        axes[3].plot(s_daily_abs_deltas.index, s_daily_abs_deltas)
        axes[3].set_title("daily abs delta")
        axes[3].set_ylabel("abs delta in $")

        axes[0].grid()
        axes[1].grid()
        axes[2].grid()
        axes[3].grid()
        plt.show()

    def get_html_plot(self, html_filename):
        s_daily_pnls = self.get_daily_pnls_series()
        s_drawdowns = self.get_drawdowns_series()
        s_daily_deltas = self.get_daily_deltas_series()
        s_daily_abs_deltas = self.get_daily_abs_deltas_series()

        plotter = HTMLPlotter("pnl summary graphs")
        plotter.plot(s_daily_pnls.index, s_daily_pnls.cumsum().values, "pnl", "daily_pnl", "green", "daily_pnl")
        plotter.plot(s_drawdowns.index, s_drawdowns.values, "pnl", "drawdown", "red", "drawdown", kind="drawdown")
        plotter.plot(s_daily_deltas.index, s_daily_deltas.values, "pnl", "daily_delta", "blue", "daily_delta")
        plotter.plot(s_daily_abs_deltas.index, s_daily_abs_deltas.values, "pnl", "daily_abs_delta", "blue", "daily_abs_delta")
        plotter.plot(s_daily_pnls.index, s_daily_pnls.cumsum().values, "pnl2", "daily_pnl", "green", "daily_pnl")
        plotter.plot(s_daily_pnls.index, s_daily_pnls.cumsum().values, "act", "daily_pnl", "green", "daily_pnl")

        f = open(html_filename, "w")
        print >> f, plotter.generate_html()
        f.close()


if __name__ == "__main__":

    summary = InterdayPnlSummary()
    with open("pnls.csv") as f:
        for line in f.readlines():
            segs = line.strip().split(",")
            date_segs = segs[0].split("-")
            date = datetime.date(int(date_segs[0]), int(date_segs[1]), int(date_segs[2]))
            symbol = segs[1]
            side = "B" if segs[4] == "1" else "S"
            pnl = float(segs[5])
            abs_delta = abs(float(segs[7]))
            summary.on_pnl(date, symbol, pnl, abs_delta, "usd", side)
    summary.get_html_plot("summary.html")
