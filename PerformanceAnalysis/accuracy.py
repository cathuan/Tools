import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from plotly.offline import plot
from plotly import tools
from HTMLPlotter import HTMLPlt


class AccuracyAnalyzer(object):

    def __init__(self, period):
        assert isinstance(period, datetime.timedelta), \
            "period must be a datetime.timedelta. Input value is %s of the form %s" % (type(period), period)
        self.pnls = []
        self.period = period

    def on_pnl(self, date, symbol, pnl):
        assert isinstance(date, datetime.date) or isinstance(date, datetime.datetime), \
            "date must be a datetime.date or datetime.datetime object. But it's %s %s" % (type(date), date)
        assert isinstance(symbol, str)

        self.pnls.append((date, symbol, pnl))

    def _convert_records_to_dataframe(self):
        df = pd.DataFrame(self.pnls, columns=["date", "symbol", "pnl"])
        return df

    def _separate_by_date_ranges(self):
        dates = []
        pnls_grouped_by_date_range = []

        df = self._convert_records_to_dataframe()
        start_date, end_date = df["date"].min(), df["date"].max()
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date)
            df_tmp = df[(df["date"] >= current_date) & (df["date"] < current_date + self.period)]
            pnls_grouped_by_date_range.append(df_tmp["pnl"].values)            
            current_date = current_date + self.period
        
        return dates, pnls_grouped_by_date_range

    def summarize_by_accuracy(self):
        dates, pnls_grouped_by_date_range = self._separate_by_date_ranges()
        accuracies = [len([pnl for pnl in pnls if pnl > 0])*1.0/len(pnls)
                      for pnls in pnls_grouped_by_date_range]
        assert len(dates) == len(accuracies)
        plt.plot(dates, accuracies)
        plt.grid()
        plt.show()

    def summarize_by_pnl_distributions(self):
        dates, pnls_grouped_by_date_range = self._separate_by_date_ranges()
        pnls_means = np.array([np.mean([pnl for pnl in pnls if pnl > 0])
                               for pnls in pnls_grouped_by_date_range])
        pnls_stddev = np.array([np.std([pnl for pnl in pnls if pnl > 0])
                                for pnls in pnls_grouped_by_date_range])
        plt.plot(dates, pnls_means, "r")
        plt.plot(dates, pnls_means+pnls_stddev, "r--")
        plt.plot(dates, pnls_means-pnls_stddev, "r--")
        plt.grid()
        plt.show()

    def summarize(self):
        dates, pnls_grouped_by_date_range = self._separate_by_date_ranges()
        accuracies = [len([pnl for pnl in pnls if pnl > 0])*1.0/len(pnls)
                      for pnls in pnls_grouped_by_date_range]
        pnls_means = np.array([np.mean([pnl for pnl in pnls if pnl > 0])
                               for pnls in pnls_grouped_by_date_range])
        pnls_stddev = np.array([np.std([pnl for pnl in pnls if pnl > 0])
                                for pnls in pnls_grouped_by_date_range])

        fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True,
                                  subplot_titles=("Accuracy", "Pnl Distributions"),
                                  vertical_spacing=0.05)
        trace1 = dict(x=dates, y=accuracies, mode="lines+markers", name="accuracy")
        trace2 = dict(x=dates, y=pnls_means, mode="lines+markers", name="mean pnl",
                      line=dict(color="red"))
        trace3 = dict(x=dates, y=pnls_means+pnls_stddev, mode="lines+markers",
                      name="mean pnl + 1 stddev", line=dict(color="red", dash="dot"))
        trace4 = dict(x=dates, y=pnls_means-pnls_stddev, mode="lines+markers",
                      name="mean pnl - 1 stddev", line=dict(color="red", dash="dot"))

        fig.append_trace(trace1, 1, 1)
        fig.append_trace(trace2, 2, 1)
        fig.append_trace(trace3, 2, 1)
        fig.append_trace(trace4, 2, 1)

        layout = dict(title="Title",
                      yaxis1=dict(title="accuracy"),
                      yaxis2=dict(title="average pnl in $"),
                      xaxis1=dict(title="dates"))
        fig.update(layout=layout)
        plot(fig, filename="test_accuracy.html")

    def summarize_plot(self):
        dates, pnls_grouped_by_date_range = self._separate_by_date_ranges()
        accuracies = [len([pnl for pnl in pnls if pnl > 0])*1.0/len(pnls)
                      for pnls in pnls_grouped_by_date_range]
        pnls_means = np.array([np.mean([pnl for pnl in pnls if pnl > 0])
                               for pnls in pnls_grouped_by_date_range])
        pnls_stddev = np.array([np.std([pnl for pnl in pnls if pnl > 0])
                                for pnls in pnls_grouped_by_date_range])
        
        plt = HTMLPlt()
        fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True)
        axes[0].plot(dates, accuracies, "bo-", label="accuracy")
        axes[1].plot(dates, pnls_means, "go-", label="mean pnl")
        axes[1].plot(dates, pnls_means+pnls_stddev, "go--", label="mean pnl + 1 stddev")
        axes[1].plot(dates, pnls_means-pnls_stddev, "go--", label="mean pnl - 1 stddev")
        axes[0].set_title("Accuracy")
        axes[1].set_title("Pnl distribution")
        axes[0].set_xlabel("dates")
        axes[0].set_ylabel("accuracy")
        axes[1].set_ylabel("pnl in $")
        plt.show()


def example():
    period = datetime.timedelta(days=7)
    summary = AccuracyAnalyzer(period)
    with open("pnls.csv") as f:
        for line in f.readlines():
            segs = line.strip().split(",")
            date_segs = segs[0].split("-")
            date = datetime.date(int(date_segs[0]), int(date_segs[1]), int(date_segs[2]))
            symbol = segs[1]
            pnl = float(segs[5])
            summary.on_pnl(date, symbol, pnl)
    #summary.sumamrize()
    summary.summarize_plot()


if __name__ == "__main__":
    example()