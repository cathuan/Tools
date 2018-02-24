# XXX: This program depends on plotly external package
# Anyone wants to run this program need to download it from pypi and build to local Python path

from __future__ import print_function
from plotly.offline import plot
from plotly import tools
import matplotlib.pyplot as plt

import datetime
import numpy as np
from collections import defaultdict


# TODO: to_html()
class HTMLPlt(object):

    def __init__(self, height_per_plot=500, width_per_plot=800):
        self.fig_configs = None
        self._title = None
        self.axes = []
        self.height_per_plot = height_per_plot
        self.width_per_plot = width_per_plot

    # ===================================
    # Methods mimic the API of matplotlib
    # ===================================
    def subplots(self, nrows=1, ncols=1, sharex=False, sharey=False):
        assert self.fig_configs is None
        assert len(self.axes) == 0

        self.fig_configs = dict(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey)
        if nrows == 1:
            for col in range(ncols):
                axes = HTMLPlotter(1, col+1)
                self.axes.append(axes)
        elif ncols == 1:
            for row in range(nrows):
                axes = HTMLPlotter(row+1, 1)
                self.axes.append(axes)
        else:
            for row in range(nrows):
                self.axes.append([])
                for col in range(ncols):
                    axes = HTMLPlotter(row+1, col+1)
                    self.axes[row].append(axes)
        
        return self.fig_configs, self.axes
        
    def plot(self, *args, **kwargs):
        _, axes = self.subplots(nrows=1, ncols=1)
        axes[0].plot(*args, **kwargs)

    def title(self, title):
        self._title = title

    def legend(self):
        pass  # automatically the legend is on.

    def grid(self):
        pass  # automatically the grid is on. Actually I think it should be on all the time..

    def xlabel(self, xlabel):
        self.axes[0].set_xlabel(xlabel)

    def ylabel(self, ylabel):
        self.axes[0].set_ylabel(ylabel)

    def xlim(self, xmin, xmax):
        self.axes[0].set_xlim(xmin, xmax)

    def ylim(self, ymin, ymax):
        self.axes[0].set_ylim(ymin, ymax)

    # ==============
    # Output methods
    # ==============
    def show(self):
        p_fig = self._draw()

        plot(p_fig, filename="tmp_test.html")
        self._clean_graphs()

    def subplot_to_html_div(self):
        p_fig = self._draw()
        p_fig["layout"].update(height=self.fig_configs["nrows"]*self.height_per_plot,
                               width=self.fig_configs["ncols"]*self.width_per_plot)

        div = plot(p_fig, output_type="div", include_plotlyjs=False)
        div = str(div)  # unicode to str

        self._clean_graphs()
        return div

    # ===========================
    # Methods used to draw graphs
    # ===========================
    def _draw(self):
        p_fig = self._layout_fig()
        p_fig = self._draw_each_graphs(p_fig)
        return p_fig

    def _layout_fig(self):
        # have to record all the subtitles first, because it will be very hard to change subtitle
        # after the p_fig has been constructed
        subtitles = []
        if self.fig_configs["nrows"] == 1:
            for col in range(self.fig_configs["ncols"]):
                subtitles.append(self.axes[col].subtitle)
        elif self.fig_configs["ncols"] == 1:
            for row in range(self.fig_configs["nrows"]):
                subtitles.append(self.axes[row].subtitle)
        else:
            for row in range(self.fig_configs["nrows"]):
                for col in range(self.fig_configs["ncols"]):
                    subtitles.append(self.axes[row][col].subtitle)

        # construct p_fig
        p_fig = tools.make_subplots(rows=self.fig_configs["nrows"], cols=self.fig_configs["ncols"],
                                    shared_xaxes=self.fig_configs["sharex"],
                                    shared_yaxes=self.fig_configs["sharey"],
                                    subplot_titles=tuple(subtitles))

        # add title to the whole subgraph
        if self._title is not None:
            p_fig["layout"].update(title=self._title)

        return p_fig

    def _draw_each_graphs(self, p_fig):
        if self.fig_configs["nrows"] == 1:
            for col in range(self.fig_configs["ncols"]):
                p_fig = self.axes[col].populate_graph(p_fig)
        elif self.fig_configs["ncols"] == 1:
            for row in range(self.fig_configs["nrows"]):
                p_fig = self.axes[row].populate_graph(p_fig)
        else:
            for row in range(self.fig_configs["nrows"]):
                for col in range(self.fig_configs["ncols"]):
                    p_fig = self.axes[row][col].populate_graph(p_fig)
        return p_fig

    def _clean_graphs(self):
        self.fig_configs = None
        self._title = None
        self.axes = []


class HTMLPlotter(object):

    linestyles_from_m_to_p = {"-": None, "--": "dash", ":": "dot", "-.": "dashdot"}

    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.traces = []
        self.subtitle = None
        self.x_axis = None
        self.y_axis = None
        self.x_label = None
        self.y_label = None
        self.x_lim = None
        self.y_lim = None

    # for some reason I can't extract linestyle automatically using mpl_to_plotly.
    # do it manually
    def _update_linestyle(self, m_fig, trace):

        # hiden deep in matplotlib fig..
        m_linestyle = m_fig._axstack._elements[0][1][1].lines[0]._linestyle
        p_linestyle = HTMLPlotter.linestyles_from_m_to_p[m_linestyle]
        trace["line"].update(dash=p_linestyle)
        return trace

    # record the axis of the axes
    # We record it once a trace is added into the axes
    def _update_corresponding_axis(self, p_fig):
        if self.x_axis is None:
            assert self.y_axis is None
            newly_added_trace = p_fig["data"][-1]
            xs = newly_added_trace["xaxis"]
            ys = newly_added_trace["yaxis"]
            self.x_axis = "xaxis" + xs[1:]
            self.y_axis = "yaxis" + ys[1:]

    # draw the graph on p_fig
    def populate_graph(self, p_fig):
        for trace in self.traces:
            p_fig.append_trace(trace, self.row, self.col)
        self._update_corresponding_axis(p_fig)

        if self.x_label is not None:
            p_fig["layout"][self.x_axis].update(title=self.x_label)
        if self.y_label is not None:
            p_fig["layout"][self.y_axis].update(title=self.y_label)
        if self.x_lim is not None:
            xmin, xmax = self.x_lim
            p_fig["layout"][self.x_axis].update(range=[xmin, xmax])
        if self.y_lim is not None:
            ymin, ymax = self.y_lim
            p_fig["layout"][self.y_axis].update(range=[ymin, ymax])
        return p_fig

    # ===================================
    # Methods mimic the API of matplotlib
    # ===================================
    def plot(self, *args, **kwargs):
        m_fig = plt.figure()
        plt.plot(*args, **kwargs)
        p_fig = tools.mpl_to_plotly(m_fig)
        trace = p_fig["data"][0]
        trace = self._update_linestyle(m_fig, trace)
        self.traces.append(trace)

    def set_title(self, subtitle):
        self.subtitle = subtitle
            
    def set_xlabel(self, xlabel):
        self.x_label = xlabel

    def set_ylabel(self, ylabel):
        self.y_label = ylabel

    def set_xlim(self, xmin, xmax):
        self.x_lim = (xmin, xmax)

    def set_ylim(self, ymin, ymax):
        self.y_lim = (ymin, ymax)


def example2():

    plt = HTMLPlt()
    plt.plot([1,2,3,4], [3,4,5,6], "bo--", label="test dashed curve")
    plt.plot([1,2,3,4], [5,6,1,9], "ro-.", label="test -. curve")
    plt.title("Test graph")
    plt.xlabel("x axis")
    plt.ylabel("y axis")
    plt.xlim(-2,5)
    plt.ylim(-2,11)
    plt.legend()
    plt.show()


def example():

    plt = HTMLPlt()
    fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True)
    axes[0][0].plot([1,2,3], [4,5,6], "r--", label="pnl")
    axes[1][0].plot([1,2,3], [4,5,6], "b", label="user")
    axes[0][1].plot([1,2,3], [4,5,6], "k", label="outrage")
    axes[1][1].plot([1,2,3], [4,5,6], "m", label="test")
    plt.legend()
    axes[0][0].set_title("[0][0] title")
    axes[0][1].set_title("[0][1] title")
    axes[0][0].set_xlabel("test x-axis")
    axes[0][0].set_ylabel("test y-axis")
    plt.show()


if __name__ == "__main__":
    example()