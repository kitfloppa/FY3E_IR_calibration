import os
import fy3
import json
import configparser
import plotly.express as px

from dash import Dash, html, dcc, callback, Output, Input


def get_world_map(data):
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
                    showocean=True, oceancolor='LightBlue')
    
    fig.update_traces(line_color='red', line_width=2)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

def draw_sat_image(data):
    fig = px.imshow(data.dn_data_b6.data, binary_string=True)

    fig.update_layout(
        margin={"t": 0, "b": 0, "r": 0, "l": 0, "pad": 0})
    
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

app.layout = html.Div(children=[
    html.Div(children=[dcc.Graph(id='world_map', figure=get_world_map(data))],
             style={'border': 'solid', 'width': '33%', 'display': 'inline-block'}),
    html.Div(children=[dcc.Graph(id='sat_image', figure=draw_sat_image(data))],
             style={'width': '33%', 'display': 'inline-block'})         
], style={"display": "inline"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)