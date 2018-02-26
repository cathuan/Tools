from __future__ import print_function
from plotly.offline import plot
from plotly import tools

from collections import defaultdict
from HTMLPlotter import HTMLPlt
import numpy as np


html_template = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
        <title>{title}</title>

        <!-- Used to hide and update the selected plotsets from dropdown menu -->
        <script language="JavaScript" type="text/JavaScript">
            function show(targetid) {{
                if (document.getElementById) {{
                    var i = 0;
                    var el;
                    while (el = document.getElementById("plotset" + i)) {{
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

        <!-- Required to interact with the plotsets -->
        <!-- Latest compiled and minified plotly.js JavaScript -->
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <!-- OR use a specific plotly.js release (e.g. version 1.5.0) -->
        <!-- <script src="https://cdn.plot.ly/plotly-1.5.0.min.js"></script> -->

        <style type="text/css">
            .hide{{display:none;}}
            .default{{display:block;}}
        </style>
    </head>
    <body>
        <center>
            Choose the plotset you want:
            <td width="100%" align="right">
                <select onchange="show(parseInt(this.value));">{dropdown_options}</select>
            </td>
        </center>
        <center>{graph_divs}</center>
    </body>
</html>
"""

class WebpagePlotter(object):

    def __init__(self, page_title="default page name"):
        self.page_title = page_title
        self.subplot_divs = defaultdict(lambda: [])
        self.plotset_orders = []

    def _get_drop_menu_html(self):
        dropdown_options = ''
        for plotset_index, plotset_name in enumerate(self.plotset_orders):
            option = '<option value="%s">%s</option>' % (plotset_index, plotset_name)
            dropdown_options += option
        return dropdown_options

    def _get_graphs_html(self):

        divs = ''
        for plotset_index, plotset_name in enumerate(self.plotset_orders):
            # We will show only one set of graphs each time. The default one is the first one
            # we start to plot. This one will be set with class "default".
            # Other graphs are originally hiden. The class will be "start-hide"
            for div in self.subplot_divs[plotset_name]:
                if plotset_index == 0:
                    divs += '<div class="default" id="plotset%s">' % plotset_index + div + '</div>'
                else:
                    divs += '<div class="start-hide" id="plotset%s">' % plotset_index + div + '</div>'
        return divs

    def add_subplot(self, plotset_name, subplot_div):
        self.subplot_divs[plotset_name].append(subplot_div)
        if plotset_name not in self.plotset_orders:
            self.plotset_orders.append(plotset_name)

    def output_html(self, html_filename):
        """output webpage of the graphs with selections
        """

        dropdown_options = self._get_drop_menu_html()
        graph_divs = self._get_graphs_html()

        # HTML template has 3 formats
        # title: title of the graph
        # dropdown_options: divs and selections used to determine the dropdown menus
        # graph_divs: divs containing js for graphs. Generally it contains the values used to plot
        html = html_template.format(title=self.page_title, dropdown_options=dropdown_options,
                                    graph_divs=graph_divs)
        with open(html_filename, "w") as f:
            print(html, file=f)


def example():
    page = WebpagePlotter("plot test page")
    plt = HTMLPlt()

    _, axes = plt.subplots(nrows=2, ncols=2, sharex=True)
    x = range(1000)
    y = np.random.normal(0,0.01,1000).cumsum()
    axes[0][0].plot(x, y, "r--", label="pnl")
    y = np.random.normal(0,0.01,1000).cumsum()
    axes[1][0].plot(x, y, "b", label="user")
    y = np.random.normal(0,0.01,1000).cumsum()
    axes[0][1].plot(x, y, "k", label="outrage")
    y = np.random.normal(0,0.01,1000).cumsum()
    axes[1][1].plot(x, y, "m", label="test")
    axes[0][0].set_title("[0][0] title")
    axes[0][1].set_title("[0][1] title")
    axes[1][1].set_title("Blue curve used to show something")
    axes[0][0].set_xlabel("test x-axis")
    axes[0][0].set_ylabel("test y-axis")
    plt.title("Graph 1")

    page.add_subplot("test test test page", plt.subplot_to_html_div())

    _, axes = plt.subplots(nrows=2, ncols=2, sharex=True)
    x = range(1000)
    y = np.random.normal(0,0.01,1000).cumsum()
    axes[0][0].plot(x, y, "y--", label="pnl")
    y = np.random.normal(0,0.01,1000).cumsum()
    axes[1][0].plot(x, y, "m", label="user")
    y = np.random.normal(0,0.01,1000).cumsum()
    axes[0][1].plot(x, y, "k-.", label="outrage")
    y = np.random.normal(0,0.01,1000).cumsum()
    axes[1][1].plot(x, y, "co--", label="test")
    axes[0][0].set_title("[0][0] title")
    axes[0][1].set_title("[0][1] title")
    axes[0][0].set_xlabel("test x-axis")
    axes[0][0].set_ylabel("test y-axis")

    page.add_subplot("copy and paste result", plt.subplot_to_html_div())
    
    page.output_html("test_page.html")


if __name__ == "__main__":

    example()