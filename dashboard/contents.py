from __future__ import annotations
from typing import Callable

import numpy as np
import plotly.express as px

from dash import html, dcc
from fy3.dn_data import DnData
from plotly.graph_objects import Figure


SENSOR_COUNT = 40


def draw_analytic_by_sensor(data: DnData, 
                            analytic_func: Callable[[np.array, np.array], Figure], 
                            x: int, y: int,
                            title: str = '') -> Figure:

    data = data.get_sections().get_sector_by_index(x, y)[:, :]
    fig = px.scatter(x=np.arange(SENSOR_COUNT), y=analytic_func(data, axis=1))

    fig.update_layout(title=title)

    return fig


def html_data_sector_analytics(data: DnData, x: int, y: int) -> html:
    content = html.Div(children=[
        html.Div(children=[
            dcc.Graph(id='get-mean-by-sensor', 
                      figure=draw_analytic_by_sensor(data, 
                                                     np.mean, 
                                                     x, y,
                                                     title='Mean by each sensor'))
        ], id='analytic-unit'),

        html.Div(children=[
            dcc.Graph(id='get-median-by-sensor',
                      figure=draw_analytic_by_sensor(data, 
                                                     np.median, 
                                                     x, y,
                                                     title='Median by each sensor'))
        ], id='analytic-unit'),

        html.Div(children=[
            dcc.Graph(id='get-std-by-sensor',
                      figure=draw_analytic_by_sensor(data, 
                                                     np.std, 
                                                     x, y,
                                                     title='Standard deviation by each sensor'))
        ], id='analytic-unit'),
    ], id='analytics')

    return content


def html_data_sector_relative_calibration(data: DnData, x: int, y: int) -> html:
    pass
