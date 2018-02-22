# XXX: This program depends on plotly external package
# Anyone wants to run this program need to download it from pypi and build to local Python path

from __future__ import print_function
from plotly.offline import plot
# from plotly.graph_objs import Scatter  # Line, Maker from here as well
from plotly import tools
import matplotlib.pyplot as plt

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
                       include_plotlyjs=False  # the js script plotly.js is included in html_template via cdn. It's pretty big.
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


def example():
    html_plotter = HTMLPlotter("test html interactive plots")
    date1 = datetime.date(2014, 1, 1)
    total_num = 1000

    fig, axes = plt.subplots(nrows=3, sharex=True)

    x = [date1 + datetime.timedelta(days=n) for n in range(total_num)]
    y = np.random.normal(0, 0.01, total_num).cumsum()
    axes[0].plot(x,y,"ro-")
    x = [date1 + datetime.timedelta(days=n) for n in range(total_num)]
    y = np.random.normal(0, 0.01, total_num).cumsum()
    axes[0].plot(x,y,"b")
    axes[0].set_title("graph 1")

    x = [date1 + datetime.timedelta(days=n) for n in range(total_num)]
    y = np.random.normal(0, 0.01, total_num).cumsum()
    axes[1].plot(x,y,"g--")
    axes[1].set_title("User used this")

    x = [date1 + datetime.timedelta(days=n) for n in range(total_num)]
    y = np.random.normal(0, 0.01, total_num).cumsum()
    axes[2].plot(x, y, "g^", markersize=15)
    axes[0].grid()
    axes[1].grid()
    axes[2].grid()

    html_plotter.add_matplotlib_fig(fig, "very very long")

    fig, axes = plt.subplots(nrows=3, sharex=True)

    x = [date1 + datetime.timedelta(days=n) for n in range(total_num)]
    y = np.random.normal(0, 0.01, total_num).cumsum()
    axes[0].plot(x,y,"ro-")
    x = [date1 + datetime.timedelta(days=n) for n in range(total_num)]
    y = np.random.normal(0, 0.01, total_num).cumsum()
    axes[0].plot(x,y,"b")
    axes[0].set_title("graph 1")

    x = [date1 + datetime.timedelta(days=n) for n in range(total_num)]
    y = np.random.normal(0, 0.01, total_num).cumsum()
    axes[1].plot(x,y,"g--")

    x = [date1 + datetime.timedelta(days=n) for n in range(total_num)]
    y = np.random.normal(0, 0.01, total_num).cumsum()
    axes[2].plot(x, y, "g^", markersize=15)
    axes[0].grid()
    axes[1].grid()
    axes[2].grid()

    html_plotter.add_matplotlib_fig(fig, "test")

    f = open("test3.html", "w")
    print(html_plotter.generate_html(), file=f)
    f.close()


if __name__ == "__main__":

    example()
