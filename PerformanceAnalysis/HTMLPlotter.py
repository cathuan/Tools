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

    def __init__(self):
        self.fig_configs = None
        self._title = None
        self.axes = []

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

    def show(self):
        subtitles = []
        for row in range(self.fig_configs["nrows"]):
            for col in range(self.fig_configs["ncols"]):
                subtitles.append(self.axes[row][col].subtitle)
        p_fig = tools.make_subplots(rows=self.fig_configs["nrows"], cols=self.fig_configs["ncols"],
                                    shared_xaxes=self.fig_configs["sharex"],
                                    shared_yaxes=self.fig_configs["sharey"],
                                    subplot_titles=tuple(subtitles))
        for row in range(self.fig_configs["nrows"]):
            for col in range(self.fig_configs["ncols"]):
                self.axes[row][col].populate_graph(p_fig)

        if self._title is not None:
            p_fig["layout"].update(title=self._title)

        plot(p_fig, filename="tmp_test.html")
        self.fig_configs = None  # clean buffer
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

    def plot(self, *args, **kwargs):
        m_fig = plt.figure()
        plt.plot(*args, **kwargs)
        p_fig = tools.mpl_to_plotly(m_fig)
        trace = p_fig["data"][0]
        trace = self._update_linestyle(m_fig, trace)
        self.traces.append(trace)

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


class HTMLPlotter_(object):

    html_template = """
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
            <title>{title}</title>

            <!-- Used to hide and update the selected graphs from dropdown menu -->
            <script language="JavaScript" type="text/JavaScript">
                function show(targetid) {{
                    if (document.getElementById) {{
                        var i = 0;
                        var el;
                        while (el = document.getElementById("graph" + i)) {{
                            if (i == targetid) {{
                                el.style.display = "block";
                            }}
                            else {{
                                el.style.display = "none";
                            }}
                            i++;
                        }}
                    }}
                }}
            </script>

            <!-- Required to interact with the graphs -->
            <!-- Latest compiled and minified plotly.js JavaScript -->
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <!-- OR use a specific plotly.js release (e.g. version 1.5.0) -->
            <!-- <script src="https://cdn.plot.ly/plotly-1.5.0.min.js"></script> -->

            <style type="text/css">
                .start-hide{{display:none;}}
                .default{{display:block;}}
            </style>
        </head>
        <body>
            <center>
                Choose the graph you want:
                <td width="100%" align="right">
                    <select onchange="show(parseInt(this.value));">{dropdown_options}</select>
                </td>
            </center>
            <center>{graph_divs}</center>
        </body>
    </html>
    """

    def __init__(self, title):
        self.title = title
        self.graphs = defaultdict(lambda: [])
        self.graph_orders = []
        self.fig = None
    def subplots(self, nrows=1, ncols=1, sharex=False, sharey=False):
        p_fig = tools.make_subplots(rows=nrows, cols=ncols, shared_xaxes=sharex, shared_yaxes=sharey)
        p_fig["layout"].update(showlegend=True)
        return p_fig

    def show(self):
        plot(self.fig, filename="tmp_test.html")

    def add_matplotlib_fig(self, fig, graph_name):
        if graph_name not in self.graph_orders:
            self.graph_orders.append(graph_name)

        plotly_fig = tools.mpl_to_plotly(fig)

        for i in range(len(plotly_fig.data)-1):
            data = plotly_fig.data[i]
            data.xaxis = plotly_fig.data[-1].xaxis
        self.graphs[graph_name] = plotly_fig

    def _get_drop_menu_html(self):
        dropdown_options = ''
        for graph_index, graph_name in enumerate(self.graph_orders):
            option = '<option value="%s">%s</option>' % (graph_index, graph_name)
            dropdown_options += option
        return dropdown_options

    def _get_graphs_html(self):
        divs = ''
        for graph_index, graph_name in enumerate(self.graph_orders):
            fig = self.graphs[graph_name]
            fig["layout"].update(height=1000, width=1000)
            div = plot(fig,
                       output_type="div",  # output div html strings instead of a full html file
                       include_plotlyjs=False  # the js script plotly.js is included in html_template via cdn.
                       )
            div = str(div)  # unicode to str

            # We will show only one set of graphs each time. The default one is the first one we start to plot.
            # This one will be set with class "default".
            # Other graphs are originally hiden. The class will be "start-hide"
            if graph_index == 0:
                divs += '<div class="default" id="graph%s">' % graph_index + div + '</div>'
            else:
                divs += '<div class="start-hide" id="graph%s">' % graph_index + div + '</div>'
        return divs

    def generate_html(self):
        """Generate html code of the graphs with selections
        """

        dropdown_options = self._get_drop_menu_html()
        graph_divs = self._get_graphs_html()

        # HTML template has 3 formats
        # title: title of the graph
        # dropdown_options: divs and selections used to determine the dropdown menus
        # graph_divs: divs containing js for graphs. Generally it contains the values used to plot
        return self.html_template.format(title=self.title, dropdown_options=dropdown_options, graph_divs=graph_divs)


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