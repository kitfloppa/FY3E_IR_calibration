from __future__ import annotations

import os
import sys

here_path = os.path.dirname(__file__)
sys.path.append(os.path.join(here_path, '..'))

import fy3
import numpy as np
import configparser
import plotly.express as px

from fy3.dn_data import DnData
from plotly.graph_objects import Figure
from plotly.subplots import make_subplots
from contents import html_data_sector_analytics
from dash import Dash, html, dcc, callback, Output, Input


def get_world_map(data: np.array) -> Figure:
    max_x, max_y = data.dn_data_b6.shape

    fig = px.line_geo(lat=[data.latitude.data[0, 0], 
                           data.latitude.data[max_x - 1, 0],
                           data.latitude.data[max_x - 1, max_y - 1], 
                           data.latitude.data[0, max_y - 1],
                           data.latitude.data[0, 0]],
                   
                      lon=[data.longitude.data[0, 0], 
                           data.longitude.data[max_x - 1, 0],
                           data.longitude.data[max_x - 1, max_y - 1], 
                           data.longitude.data[0, max_y - 1],
                           data.longitude.data[0, 0]])
    
    fig.update_geos(projection_type='natural earth', 
                    showland=True, landcolor='LightGreen',
                    showocean=True, oceancolor='LightBlue'
    )
    
    fig.update_traces(line_color='red', line_width=2)
    
    fig.update_layout(
        margin={'t': 0, 'b': 0, 'r': 0, 'l': 0, 'pad': 0}
    )

    return fig


def draw_sat_data(data: np.array) -> Figure:
    fig = px.imshow(data, binary_string=True)

    fig.update_layout(
        margin={'t': 0, 'b': 0, 'r': 0, 'l': 0, 'pad': 0}
    )
    
    fig.update_xaxes(color='black')
    fig.update_yaxes(color='black')
    
    return fig


def draw_sec_sat_data(data: fy3.FY3EIrDnImg, x: int, y: int) -> Figure:
    fig = make_subplots(rows=2, cols=1)
    
    data_b6 = data.dn_data_b6.get_sections().get_sector_by_index(x, y)[:, :]
    data_b7 = data.dn_data_b7.get_sections().get_sector_by_index(x, y)[:, :]

    fig.append_trace(px.imshow(data_b6, binary_string=True).data[0], row=1, col=1)
    fig.append_trace(px.imshow(data_b7, binary_string=True).data[0], row=2, col=1)

    fig.update_layout(title_text='Data sector b6 (top) and b7 (bottom)')
    
    fig.update_xaxes(color='black')
    fig.update_yaxes(color='black')
    
    return fig
    

config = configparser.ConfigParser()
config.read('file_paths.ini')

# File paths for FengYun-3E data.
FY3E_L1_GOE_DATA_LOCATION = config['FY3']['FY3E_L1_GOE_DATA_LOCATION']
FY3E_L1_IMAGE_DATA_LOCATION = config['FY3']['FY3E_L1_IMAGE_DATA_LOCATION']

fy3e_l1_geo_files_paths = [FY3E_L1_GOE_DATA_LOCATION + file_name for file_name in os.listdir(FY3E_L1_GOE_DATA_LOCATION)]
fy3e_l1_image_files_paths = [FY3E_L1_IMAGE_DATA_LOCATION + file_name for file_name in os.listdir(FY3E_L1_IMAGE_DATA_LOCATION)]

data = fy3.FY3EIrDnImg(fy3e_l1_image_files_paths[0], fy3e_l1_geo_files_paths[0])

app = Dash(__name__)
app.css.append_css({'external_url': 'assets/dashboard_style.css'})
app.server.static_folder = 'assets'

app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[dcc.Graph(id='world_map', figure=get_world_map(data))],
             id='world_map_container'),

        html.Div(children=[dcc.Graph(id='sat_image', figure=draw_sat_data(data.dn_data_b6.data))],
                id='sat_image_container'),
        
        html.Div(children=[dcc.Graph(id='get-sec-data')], id='sat_sec_image_container')
    ], id='main_information'),

    html.Div(id='offset_1', style={'height': '50px'}),
    
    dcc.Tabs(id='ir-channels-analytics-tabs', value='tab-b6', children=[
        dcc.Tab(label='b6 sector analytics', value='tab-b6'),
        dcc.Tab(label='b7 sector analytics', value='tab-b7')
    ]),

    html.Div(id='data-analytics'),

    html.Div(id='offset_2', style={'height': '50px'}),

    dcc.Tabs(id='ir-channels-relative-calibration-tabs', value='tab-b6', children=[
        dcc.Tab(label='b6 sectors relative calibration', value='tab-b6'),
        dcc.Tab(label='b7 sectors relative calibration', value='tab-b7')
    ]),

    html.Div(id='data-relative-calibration')
])


@callback(
    Output('get-sec-data', 'figure'),
    Input('sat_image', 'clickData'))
def display_click_data(clickData):
    if clickData:
        x, y = clickData['points'][0]['x'], clickData['points'][0]['y']
    else:
        x, y = 0, 0
    
    return draw_sec_sat_data(data, x, y)
    

@callback(
    Output('data-analytics', 'children'),
    Input('ir-channels-analytics-tabs', 'value'),
    Input('sat_image', 'clickData'))
def render_analytics_content(tab, clickData):
    if clickData:
        x, y = clickData['points'][0]['x'], clickData['points'][0]['y']
    else:
        x, y = 0, 0

    if tab == 'tab-b6':
        return html_data_sector_analytics(data.dn_data_b6, x, y)
    elif tab == 'tab-b7':
        return html_data_sector_analytics(data.dn_data_b7, x, y)


@callback(
    Output('data-relative-calibration', 'children'),
    Input('ir-channels-relative-calibration-tabs', 'value'),
    Input('sat_image', 'clickData'))
def render_relative_calibration_content(tab, clickData):
    if clickData:
        x, y = clickData['points'][0]['x'], clickData['points'][0]['y']
    else:
        x, y = 0, 0

    if tab == 'tab-b6':
        return html_data_sector_analytics(data.dn_data_b6, x, y)
    elif tab == 'tab-b7':
        return html_data_sector_analytics(data.dn_data_b7, x, y)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
