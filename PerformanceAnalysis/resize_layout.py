from __future__ import print_function
from plotly.offline import plot
from plotly import tools
import plotly.graph_objs as go

import numpy as np
import pandas as pd


def get_all_axes(layout):
    xs = {}
    ys = {}
    for key, value in layout.items():
        if key.startswith("xaxis"):
            xs[key] = value
        if key.startswith("yaxis"):
            ys[key] = value
    return xs, ys


def resize_axis(axis_name, layout, fig_min, fig_max):
    assert fig_min < fig_max
    axis_size_min = layout[axis_name]["domain"][0]
    axis_size_max = layout[axis_name]["domain"][1]
    ratio = fig_max - fig_min

    new_axis_size_min = axis_size_min * ratio + fig_min
    new_axis_size_max = axis_size_max * ratio + fig_min
    layout[axis_name]["domain"] = [new_axis_size_min, new_axis_size_max]
    return layout


def relocate_position(axis_name, layout, oppo_min, oppo_max):
    assert oppo_min < oppo_max
    # determine where the labels of ticks will be printed
    if "position" in layout[axis_name]:
        ratio = oppo_max - oppo_min
        position = layout[axis_name]["position"]
        new_position = position * ratio + oppo_min
        layout[axis_name].update(position=new_position)
    return layout
    

def resize_layout(layout, x_min=0.0, x_max=1.0, y_min=0.0, y_max=1.0):
    xs, ys = get_all_axes(layout)
    for xaxis in xs:
        layout = resize_axis(xaxis, layout, x_min, x_max)
        layout = relocate_position(xaxis, layout, y_min, y_max)
    for yaxis in ys:
        layout = resize_axis(yaxis, layout, y_min, y_max)
        layout = relocate_position(yaxis, layout, x_min, x_max)
    
    # change the place of text, usually subtitles
    if "annotations" in layout:
        for annotation in layout["annotations"]:
            if "text" in annotation:
                x_pos = annotation["x"]
                y_pos = annotation["y"]
                new_x_pos = x_min + (x_max - x_min) * x_pos
                new_y_pos = y_min + (y_max - y_min) * y_pos
                annotation.update(x=new_x_pos)
                annotation.update(y=new_y_pos)

    return layout


def get_table_trace(df, x_min=0.0, x_max=1.0, y_min=0.0, y_max=1.0):
    table_trace = go.Table(header=dict(values=df.columns.tolist(),
                                       fill=dict(color="grey"),
                                       line=dict(color="#506784"),
                                       font=dict(color="white", size=14)),
                           cells=dict(values=[df[col].tolist() for col in df.columns],
                                      line=dict(color="#506784")),
                           domain=dict(x=[x_min, x_max], y=[y_min, y_max]))
    return table_trace


if __name__ == "__main__":

    df = pd.DataFrame(np.arange(300).reshape(100,3))
    df.columns = ["a", "b", "c"]
    table_trace0 = get_table_trace(df, 0, 0.45, 0, 0.65)

    df = pd.DataFrame(np.arange(20).reshape(5,4))
    df.columns = ["1", "2", "3", "4"]
    table_trace1 = get_table_trace(df, 0, 0.45, 0.75, 1.0)

    fig = tools.make_subplots(rows=3, cols=2, shared_xaxes=True)
    trace = go.Scatter(x=range(100), y=np.random.normal(0,0.1,100).cumsum())
    fig.append_trace(trace, 1, 1)
    trace = go.Scatter(x=range(100), y=np.random.normal(0,0.1,100).cumsum())
    fig.append_trace(trace, 2, 1)
    trace = go.Scatter(x=range(100), y=np.random.normal(0,0.1,100).cumsum())
    fig.append_trace(trace, 3, 1)
    trace = go.Scatter(x=range(100), y=np.random.normal(0,0.1,100).cumsum())
    fig.append_trace(trace, 1, 2)
    trace = go.Scatter(x=range(100), y=np.random.normal(0,0.1,100).cumsum())
    fig.append_trace(trace, 2, 2)
    trace = go.Scatter(x=range(100), y=np.random.normal(0,0.1,100).cumsum())
    fig.append_trace(trace, 3, 2)

    layout = fig["layout"]
    layout = resize_layout(layout, x_min=0.5, x_max=1.0)
    layout["xaxis1"].update(title="test x axis")
    layout["yaxis1"].update(title="test y axis")

    fig["data"].append(table_trace0)
    fig["data"].append(table_trace1)
    plot(fig)
    assert False
