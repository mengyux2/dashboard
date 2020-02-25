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

color_list = px.colors.qualitative.G10
imo_list_100 = [9082063,
 8316601,
 9286243,
 9586320,
 9150298,
 9088732,
 9557226,
 9586863,
 9290701,
 9438391,
 9357468,
 9357456,
 9357420,
 9533347,
 9438377,
 8706090,
 9621182,
 9357444,
 9111591,
 9164445,
 9605839,
 9169067,
 9626924,
 9573995,
 9339454,
 9650494,
 9004712,
 9438389,
 9412957,
 9551375,
 9291080,
 9712199,
 9594444,
 9584205,
 9576739,
 9374349,
 9831775,
 9228215,
 9611503,
 9122899,
 9408267,
 9129689,
 9151333,
 9316995,
 9310769,
 9611498,
 9040443,
 9556844,
 9199842,
 9201061,
 9282948,
 9486257,
 9001485,
 9487433,
 9512202,
 9146003,
 9571428,
 9152246,
 9418779,
 9549566,
 9666649,
 9302906,
 9329411,
 9433559,
 9249300,
 9441881,
 9321005,
 9573957,
 9495363,
 9530979,
 9732802,
 9605047,
 9605841,
 9433896,
 9403841,
 9528184,
 9347853,
 9621170,
 9597977,
 9615066,
 9485033,
 9565118,
 9412969,
 9273014,
 9288344,
 9584293,
 9604419,
 9152480,
 9626948,
 9189770,
 9588249,
 9253193,
 9408293,
 9189861,
 9174488,
 9293105,
 9284489,
 9557240,
 9718179,
 9316191]

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
        children='Vessel Owner Score Plot 2 week data(left) and 1 week data(right)',
        style={
            'textAlign': 'left',
            'color': colors['text']}
    ),

    html.Div([
        dcc.Dropdown(
            id='dropdown1',
            options=[{'label': i, 'value': i} for i in imo_list_100],
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

            style={'width':'600','height':'500'}
        ),
        style={'display':'inline-block'}
    ),

    html.Div(
        dcc.Graph(
            id='graph_2week',

            style={'width':'600','height':'500'}
        ),
        style={'display':'inline-block'}
    ),


    ],
style={'width': '100%', 'display': 'inline-block'}
)


#callback to update graph
@app.callback(
    Output(component_id='graph_2week', component_property='figure'), 
    [Input(component_id='dropdown1',component_property='value')]
)

def update_graph_2week(value):
    data = df_2week[df_2week['imo'] ==value]
    traces = []
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
                'color': color_list[idx],
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
                'color': color_list[idx],
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