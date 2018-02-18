from __future__ import print_function
import numpy as np
from plotly.offline import plot
from plotly.graph_objs import Scatter, Line
import datetime
from plotly import tools
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
            <td width="100%" align="right">
                <select onchange="show(parseInt(this.value));">""",
                """
                </select>
            </td>
            <center>""",
            """
            </center>
        </body>
    </html>
    """]

    def __init__(self):
        self.graphs_in_subplots = {}
        self.plot_summary = defaultdict(lambda: set())

    def plot(self, x, y, plot_name, n_row, color, label):
        self.graphs_in_subplots[(plot_name, n_row)] = Scatter(x=x, y=y, line=Line(width=2, color=color), name=label)
        self.plot_summary[plot_name].add(n_row)

    def generate_html(self):
        graph_indices = enumerate(sorted(self.plot_summary.keys()))

        divs = ''
        for graph_index, plot_name in graph_indices:
            rows = len(self.plot_summary[plot_name])
            fig = tools.make_subplots(rows=rows, cols=1, shared_xaxes=True)
            for n_row in sorted(self.plot_summary[plot_name]):
                trace = self.graphs_in_subplots[(plot_name, n_row)]
                fig.append_trace(trace, n_row, 1)
            fig["layout"].update(height=1000, width=1000, title=plot_name)
            div = plot(fig, output_type="div")
            divs += '<div class="start-hide" id="graph%s">' % graph_index + div + '</div>'

        graph_indices = enumerate(sorted(self.plot_summary.keys()))
        options = ''
        for graph_index, plot_name in graph_indices:
            option = '<option value="%s">%s</option>' % (graph_index, plot_name)
            options += option

        return self.html_template[0] + options + self.html_template[1] + divs + self.html_template[2]


def test():
    date1 = datetime.date(2014, 1, 1)
    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    trace1 = Scatter(x=x, y=y, line=Line(width=2, color="red"), name="PnL")

    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    trace2 = Scatter(x=x, y=y, line=Line(width=2, color="blue"), name="inverse pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    trace3 = Scatter(x=x, y=y, line=Line(width=2, color="green"), name="volume")

    fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 1)
    fig.append_trace(trace3, 2, 1)
    fig["layout"].update(height=1000, width=1000, title="test graph 1 with two subplots")
    div1 = plot(fig, output_type="div")
    div2 = plot(fig, output_type="div")

    date1 = datetime.date(2014, 1, 1)
    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    trace1 = Scatter(x=x, y=y, line=Line(width=2, color="red"), name="PnL")

    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    trace2 = Scatter(x=x, y=y, line=Line(width=2, color="blue"), name="inverse pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    trace3 = Scatter(x=x, y=y, line=Line(width=2, color="green"), name="volume")

    fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 1)
    fig.append_trace(trace3, 2, 1)
    fig["layout"].update(height=1000, width=1000, title="test graph 2 with two subplots")
    div3 = plot(fig, output_type="div")
    div4 = plot(fig, output_type="div")

    html_string = """
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
            <title>oec2003</title>
            <script language="JavaScript" type="text/JavaScript">
                function show(targetid) {
                    if (document.getElementById) {
                        var i = 1;
                        var el;
                        while (el = document.getElementById("div" + i)) {
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
            <td width="100%" align="right">
                <select onchange="show(parseInt(this.value));">
                    <option selected="selected" value="1">Text 1</option>
                    <option value="2">Text 2</option>
                </select>
            </td>
            <center>
                <div class="origin" id="div1">""" + div1 + div2 + """</div>
                <div class="start-hide" id="div2">""" + div3 + div4 + """</div>
            </center>
        </body>
    </html>
    """
    f = open("test2.html", "w")
    print(html_string, file=f)
    f.close()


if __name__ == "__main__":

    html_plotter = HTMLPlotter()
    date1 = datetime.date(2014, 1, 1)

    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "graph1", 1, "green", "pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "graph1", 2, "blue", "delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "graph1", 3, "red", "volume")

    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "graph2", 1, "green", "pnl")

    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "graph2", 2, "blue", "delta")

    x = [date1 + datetime.timedelta(days=n) for n in range(10000)]
    y = np.random.normal(0, 0.01, 10000).cumsum()
    html_plotter.plot(x, y, "graph2", 3, "red", "volume")

    f = open("test3.html", "w")
    print(html_plotter.generate_html(), file=f)
    f.close()
