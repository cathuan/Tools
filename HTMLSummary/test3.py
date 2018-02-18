# This program depends on plotly external package
# Anyone wants to run this program need to download it from pypi and build to local Python path

from __future__ import print_function
import numpy as np
from plotly.offline import plot
from plotly.graph_objs import Scatter, Line
import datetime
from collections import defaultdict


class HTMLPlotter(object):

    html_template = ["""
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
            <title>oec2003</title>
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
            </script>
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

    def __init__(self):
        self.graphs = defaultdict(lambda: defaultdict(lambda: []))

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

    def get_ordered_subplot_names(self, graph_name):
        """Determine the order of subplots in each graph
        """
        return self.graphs[graph_name]

    def generate_html(self):
        """Generate html code of the graphs with selections
        """

        divs = ''
        for graph_index, graph_name in enumerate(sorted(self.graphs)):
            graph_divs = ''
            for subplot_name in self.get_ordered_subplot_names(graph_name):
                data = self.graphs[graph_name][subplot_name]
                layout = dict(title=subplot_name, height=500, width=1000)
                fig = dict(data=data, layout=layout)
                div = plot(fig, output_type="div")
                graph_divs += div
            divs += '<div class="start-hide" id="graph%s">' % graph_index + graph_divs + '</div>'

        options = ''
        for graph_index, graph_name in enumerate(sorted(self.graphs)):
            option = '<option value="%s">%s</option>' % (graph_index, graph_name)
            options += option

        return self.html_template[0] + options + self.html_template[1] + divs + self.html_template[2]


def example():
    html_plotter = HTMLPlotter()
    date1 = datetime.date(2014, 1, 1)

    print("graph1 pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "pnl", "blue", "net pnl")

    print("graph1 pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "very long very long very long name", "position", "red", "abs delta")

    print("graph1 pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "test", "pnl", "green", "gross pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "test", "pnl", "blue", "net pnl")

    print("graph1 pnl")
    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "test", "position", "blue", "delta")
    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "test", "position", "red", "abs delta")

    print("HTML")
    f = open("test3.html", "w")
    print(html_plotter.generate_html(), file=f)
    f.close()


if __name__ == "__main__":

    example()
