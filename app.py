import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px


df_2week = pd.read_csv('owner_test.csv')
df_1week = pd.read_csv("owner_test_1week.csv")
df_2and1week = pd.read_csv("owner_test_2week.csv")

#color_list = px.colors.qualitative.Dark24

fileName = 'asia_imo_list.txt'
good_pattern_fileName = 'common_imo_list_pattern.txt'
imo_list_300 = [int(line.rstrip('\n')) for line in open(fileName)]

#app = dash.Dash()
app = dash.Dash(__name__)
server = app.server
colors = {
    'background': '#111111',
    'text': '#000000'
}

#function to generate perfromance table from pandas dataframe
def generate_table(dataframe, max_rows=1000000):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app.layout = html.Div([
    html.H1(
        children='Vessel Owner Score Plots',
        style={
            'textAlign': 'left',
            'color': colors['text']}
    ),

    html.Div(children='''
        plot1: weekly call using 1 week data. \b
        plot2: biweekly call using 2 weeks data. \b
        plot3: weekly call using 2 weeks data. \b
    '''),

    html.Div([
        dcc.Dropdown(
            id='dropdown1',
            options=[{'label': i, 'value': i} for i in imo_list_300],
            value='10',
            style={'width': '49%', 'display': 'inline-block'}
        ),
    ],
    style={'width': '49%', 'display': 'inline-block'}
    ),

    html.Div(id='tablecontainer'),
    
    html.Div(
        dcc.Graph(
            id='graph_1week',

            style={'width':'550','height':'450'}
        ),
        style={'display':'inline-block'}
    ),

    html.Div(
        dcc.Graph(
            id='graph_2week',

            style={'width':'550','height':'450'}
        ),
        style={'display':'inline-block'}
    ),

    html.Div(
        dcc.Graph(
            id='graph_2and1week',

            style={'width':'550','height':'450'}
        ),
        style={'display':'inline-block'}
    ),


    ],
style={'width': '100%', 'display': 'inline-block'}
)

def match_color(df_2week,df_1week,df_2and1week,value):
    color_list = px.colors.qualitative.Dark24+px.colors.qualitative.Light24
    color_map = {}
    data_2week = df_2week[df_2week['imo'] == value]
    data_1week = df_1week[df_1week['imo'] == value]
    data_2and1week = df_2and1week[df_2and1week['imo'] == value]
    email_list = list(set(data_2week.email.unique().tolist()+data_1week.email.unique().tolist()+data_2and1week.email.unique().tolist()))
    for idx,email in enumerate(email_list):
        color_map[email] = color_list[idx]
    return color_map


#callback to update graph
@app.callback(
    Output(component_id='graph_2week', component_property='figure'), 
    [Input(component_id='dropdown1',component_property='value')]
)

def update_graph_2week(value):
    data = df_2week[df_2week['imo'] ==value]
    traces = []
    color_map = match_color(df_2week,df_1week,df_2and1week,value)
    for idx, i in enumerate(data.email.unique()):
        df_by_email = data[data['email'] == i]
        traces.append(dict(
            x=df_by_email['creation_date'].values.tolist(),
            y=df_by_email['score'].values.tolist(),
            text=df_by_email['email'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'color': color_map[i],
                'line': {'width': 0.3, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'datetime', 'title': 'email creation date'
                   },
            yaxis={'title': 'TFIDF score', 'range': [0, 1.3]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
    		}

#callback to update graph
@app.callback(
    Output(component_id='graph_1week', component_property='figure'), 
    #[Input('dropdown1', 'value')]
    [Input(component_id='dropdown1',component_property='value')]
)

def update_graph_1week(value):
    data = df_1week[df_1week['imo'] ==value]
    traces = []
    color_map = match_color(df_2week,df_1week,df_2and1week,value)
    for idx, i in enumerate(data.email.unique()):
        df_by_email = data[data['email'] == i]
        traces.append(dict(
            x=df_by_email['creation_date'].values.tolist(),
            y=df_by_email['score'].values.tolist(),
            text=df_by_email['email'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'color': color_map[i],
                'line': {'width': 0.3, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'datetime', 'title': 'email creation date'
                   },
            yaxis={'title': 'TFIDF score', 'range': [0, 1.3]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
            }
    
#callback to update graph
@app.callback(
    Output(component_id='graph_2and1week', component_property='figure'), 
    #[Input('dropdown1', 'value')]
    [Input(component_id='dropdown1',component_property='value')]
)

def update_graph_2and1week(value):
    data = df_2and1week[df_2and1week['imo'] ==value]
    traces = []
    color_map = match_color(df_2week,df_1week,df_2and1week,value)
    for idx, i in enumerate(data.email.unique()):
        df_by_email = data[data['email'] == i]
        traces.append(dict(
            x=df_by_email['creation_date'].values.tolist(),
            y=df_by_email['score'].values.tolist(),
            text=df_by_email['email'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'color': color_map[i],
                'line': {'width': 0.3, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'datetime', 'title': 'email creation date'
                   },
            yaxis={'title': 'TFIDF score', 'range': [0, 1.3]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
            }


if __name__ == '__main__':
    app.run_server(debug=False)