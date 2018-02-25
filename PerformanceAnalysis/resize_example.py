from plotly import tools
import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

if __name__ == "__main__":
    trace0 = go.Scatter(
        x=[1, 2],
        y=[1, 2]
    )
    trace1 = go.Scatter(
        x=[1, 2],
        y=[1, 2]
    )
    trace2 = go.Scatter(
        x=[1, 2, 3],
        y=[2, 1, 2]
    )

    df = pd.DataFrame(np.arange(300).reshape(100,3))
    df.columns = ["a", "b", "c"]

    table_trace0 = go.Table(header=dict(values=df.columns.tolist()),
                            cells=dict(values=[df[col].tolist() for col in df.columns]),
                            domain=dict(x=[0, 0.45], y=[0,0.65]))

    df = pd.DataFrame(np.arange(20).reshape(5,4))
    df.columns = ["1", "2", "3", "4"]
    table_trace1 = go.Table(header=dict(values=df.columns.tolist()),
                            cells=dict(values=[df[col].tolist() for col in df.columns]),
                            domain=dict(x=[0, 0.45], y=[0.75,1.0]))

    #fig = tools.make_subplots(rows=2, cols=2, specs=[[{}, {}], [{'colspan': 2}, None]],
    #                          subplot_titles=('First Subplot','Second Subplot', 'Third Subplot'))
    fig = tools.make_subplots(rows=2, cols=2, specs=[[{"rowspan":2}, {}], [None, {}]])

    fig.append_trace(trace1, 1, 2)
    fig.append_trace(trace2, 2, 2)
    fig['layout'].update(showlegend=False, title='Specs with Subplot Title')

    data = fig["data"]
    data.append(table_trace0)
    data.append(table_trace1)
    layout = fig["layout"]
    fig = dict(data=data, layout=layout)
    py.plot(fig)