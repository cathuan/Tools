# XXX: This program depends on plotly external package
# Anyone wants to run this program need to download it from pypi and build to local Python path

from __future__ import print_function
from plotly.offline import plot
from plotly.graph_objs import Scatter, Line
from plotly import tools

import datetime
import numpy as np
from collections import defaultdict


class HTMLPlotter(object):

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
                    <select onchange="show(parseInt(this.value));">{dropdown_menu_html}</select>
                </td>
            </center>
            <center>{graph_divs}</center>
        </body>
    </html>
    """

    # color support for matplotlib
    colors = {"b": "blue", "r": "red", "k": "black", "g": "green", "c": "cyan", "y": "yellow", "m": "magenta",
              "w": "white"}

    def __init__(self, title):
        self.title = title
        self.graphs = defaultdict(lambda: defaultdict(lambda: []))
        self.graph_orders = []  # the order we put graphs in dropdown menu
        self.subgraph_orders = defaultdict(lambda: [])  # the order of each subgraphs in a graph

    def plot(self, x, y, graph_name, subplot_name, color, label, kind=None):
        """Main function used to generate graphs in a comparatively simple API
        input:
        =====
        x: data in x-axis
        y: data in y-axis
        graph_name: the name shown in the selector. All graphs with the same graph_name will be shown together
        subplot_name: the title of each subgraph
        color: the color of the curve
        label: the label of the curve
        """
        if graph_name not in self.graph_orders:
            self.graph_orders.append(graph_name)
        if subplot_name not in self.subgraph_orders[graph_name]:
            self.subgraph_orders[graph_name].append(subplot_name)

        # translate matplotlib color to plotly color
        if color in HTMLPlotter.colors:
            plot_color = HTMLPlotter.colors[color]
        else:
            plot_color = color

        if kind == "drawdown":
            fill = "tonexty"
            fillcolor = "red"
            self.graphs[graph_name][subplot_name].append(Scatter(x=x, y=y, line=Line(width=2, color=plot_color),
                                                                 name=label, fill=fill, fillcolor=fillcolor))
        elif kind is None:
            self.graphs[graph_name][subplot_name].append(Scatter(x=x, y=y, line=Line(width=2, color=plot_color),
                                                                 name=label))
        else:
            assert False, "kind %s is not supported" % kind

    def _get_drop_menu_html(self):
        dropdown_menu_html = ''
        for graph_index, graph_name in enumerate(self.graph_orders):
            option = '<option value="%s">%s</option>' % (graph_index, graph_name)
            dropdown_menu_html += option
        return dropdown_menu_html

    def _get_graphs_html(self):
        divs = ''
        for graph_index, graph_name in enumerate(self.graph_orders):
            subplot_names = self.subgraph_orders[graph_name]
            num_subplots = len(subplot_names)
            fig = tools.make_subplots(rows=num_subplots, cols=1, subplot_titles=subplot_names,
                                      shared_xaxes=True)
            for subplot_name, data in self.graphs[graph_name].items():
                index = subplot_names.index(subplot_name) + 1  # row number starts with 1 instead of 0
                for trace in data:
                    fig.append_trace(trace, index, 1)
            fig["layout"].update(height=300*num_subplots, width=1000, title=graph_name)
            div = plot(fig,
                       output_type="div",  # output div html strings instead of a full html file
                       include_plotlyjs=False  # the js script plotly.js is included in html_template via cdn. It's pretty big.
                       )
            div = str(div)

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

        dropdown_menu_html = self._get_drop_menu_html()
        graph_divs = self._get_graphs_html()

        # HTML template has 3 formats
        # title: title of the graph
        # dropdown_menu_html: divs and selections used to determine the dropdown menus
        # graph_divs: divs containing js for graphs. Generally it contains the values used to plot
        return self.html_template.format(title=self.title, dropdown_menu_html=dropdown_menu_html, graph_divs=graph_divs)


def example():
    html_plotter = HTMLPlotter("test html interactive plots")
    date1 = datetime.date(2014, 1, 1)

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "cyan", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "magenta", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "yellow", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "black", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "value", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "value", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "task", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "task", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "user", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "user", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "user", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "test2", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "pig", "position", "red", "abs delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "player", "position", "red", "abs delta")

    f = open("test3.html", "w")
    print(html_plotter.generate_html(), file=f)
    f.close()


if __name__ == "__main__":

    example()
