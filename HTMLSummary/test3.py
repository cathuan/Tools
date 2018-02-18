# XXX: This program depends on plotly external package
# Anyone wants to run this program need to download it from pypi and build to local Python path

from __future__ import print_function
from plotly.offline import plot
from plotly.graph_objs import Scatter, Line
from plotly import tools

import datetime
import numpy as np
from collections import defaultdict
from bs4 import BeautifulSoup


class HTMLPlotter(object):

    html_template = ["""
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
            <title>""", """</title>
            <script language="JavaScript" type="text/JavaScript">
                function show(targetid) {
                    if (document.getElementById) {
                        var i = 0;
                        var el;
                        while (el = document.getElementById("graph" + i)) {
                            if (i == targetid) {
                                el.style.display = "block";
                            }
                            else {
                                el.style.display = "none";
                            }
                            i++;
                        }
                    }
                }
            </script>""", """
            <style type="text/css">
                .start-hide{
                    display:none;
                }
                .origin{
                    display:block;
                }
            </style>
        </head>
        <body>
            <center>
                Choose the graph you want:
                <td width="100%" align="right">
                    <select onchange="show(parseInt(this.value));">""",
                """
                    </select>
                </td>
            </center>
            <center>""",
            """
            </center>
        </body>
    </html>
    """]

    def __init__(self, title):
        self.graphs = defaultdict(lambda: defaultdict(lambda: []))
        self.title = title
        self.common_js_script_for_each_plot = None

    def plot(self, x, y, graph_name, subplot_name, color, label):
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
        self.graphs[graph_name][subplot_name].append(Scatter(x=x, y=y, line=Line(width=2, color=color), name=label))

    def _get_ordered_subplot_names(self, graph_name):
        """Determine the order of subplots in each graph
        """
        return list(set(self.graphs[graph_name].keys()))

    def _get_drop_menu_html(self):
        options = ''
        for graph_index, graph_name in enumerate(sorted(self.graphs)):
            option = '<option value="%s">%s</option>' % (graph_index, graph_name)
            options += option
        return options

    def _get_graphs_html(self):
        divs = ''
        for graph_index, graph_name in enumerate(sorted(self.graphs)):
            subplot_names = self._get_ordered_subplot_names(graph_name)
            num_subplots = len(subplot_names)
            fig = tools.make_subplots(rows=num_subplots, cols=1, subplot_titles=subplot_names,
                                      shared_xaxes=True)
            for subplot_name, data in self.graphs[graph_name].items():
                index = subplot_names.index(subplot_name) + 1  # row number starts with 1 instead of 0
                for trace in data:
                    fig.append_trace(trace, index, 1)
            fig["layout"].update(height=200*num_subplots, width=1000, title="graph_name")
            div = plot(fig, output_type="div")
            soup = BeautifulSoup(div)
            js_script, plot_script = soup.find_all("script")
            plot_div_info = str(soup.find_all("div")[1].prettify())
            if self.common_js_script_for_each_plot is None:
                self.common_js_script_for_each_plot = str(js_script.prettify())
            divs += '<div class="start-hide" id="graph%s">' % graph_index + plot_div_info + str(plot_script.prettify()) + '</div>'
        return divs

    def generate_html(self):
        """Generate html code of the graphs with selections
        """

        options = self._get_drop_menu_html()
        graphs = self._get_graphs_html()

        # HTML template is separated into 4 pieces
        # js function to choose the graph is contained in the second piece: function show
        # place title between the first and second pieces
        # place dropdown menu code between the second and third pieces
        # place graphs between the third and fourth pieces
        return self.html_template[0] + self.title + self.html_template[1] + self.common_js_script_for_each_plot + self.html_template[2] + options + self.html_template[3] + graphs + self.html_template[4]


def example():
    html_plotter = HTMLPlotter("test html interactive plots")
    date1 = datetime.date(2014, 1, 1)

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "blue", "net pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(100)]
    y = np.random.normal(0, 0.01, 100).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "red", "abs delta")

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
