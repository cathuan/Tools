import pandas as pd
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
fig["layout"].update(height=600, width=600, title="test graph with two subplots")
div = plot(fig, output_type="div")

df = pd.DataFrame(np.arange(1000).reshape(50, 20))
summary_table_1 = df.describe()
for column in summary_table_1.columns:
    summary_table_1[column] = summary_table_1[column].apply(lambda v: "%.2f" % v)
# use bootstrap styling
summary_table_1 = summary_table_1.to_html().replace('<table border="1" class="dataframe">',
                                                    '<table class="table table-striped">')

summary_table_2 = df.to_html().replace('<table border="1" class="dataframe">',
                                       '<table class="table table-striped">')

style = '''
<style>
    body{ margin:0 100; background:whitesmoke; }

    tr {
    width: 100%;
    display: inline-table;
    table-layout: fixed;
    }

    table{
     height:300px;              // <-- Select the height of the table
     display: -moz-groupbox;    // Firefox Bad Effect
     table-layout: fixed;
     width: 100%
    }
    tbody{
      overflow-y: scroll;
      height: 200px;            //  <-- Select the height of the body
      width: 100%;
      position: absolute;
    }
</style>
'''
html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        ''' + style + '''
    </head>
    <body>
        <h2>2014 technology and CPG stock prices</h1>
        <h3>Section 1: Apple Inc. (AAPL) stock in 2014</h2>
        ''' + div + '''
        <p>Apple stock price rose steadily through 2014.</p>
        <h3>Reference table: stock tickers</h3>
        <div class="span3", style="overflow:auto">
            ''' + summary_table_1 + '''
        </div>
        <h3>Summary table: 2014 stock statistics</h3>
        <div class="span3", style="overflow:auto">
            ''' + summary_table_2 + '''
        </div>
    </body>
</html>'''

print html_string
