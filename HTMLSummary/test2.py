from __future__ import print_function
import numpy as np
from plotly.offline import plot
from plotly.graph_objs import Scatter, Line
import datetime
from plotly import tools


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
div2 = plot(fig, output_type="div")

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
            .size{
                height:400px;
                width:400px;
                display:none;
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
            <div class="size" id="div1">""" + div1 + """</div>
            <div class="size" id="div2">""" + div2 + """ </div>
        </center>
    </body>
</html>
"""
f = open("test2.html", "w")
print(html_string, file=f)
f.close()
