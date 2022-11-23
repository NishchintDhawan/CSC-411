from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import os
import glob

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)


df_2022 = pd.DataFrame({
    "Place": ["Downtown", "Burnside", "Victoria West", "James Bay", "Rock Bay"],
    "Amt": [29805.12, 61483.46, 66089.22, 24817.28, 84286.51],
    "Exits": [3, 1, 2, 5, 1]
})


fig = px.scatter(df_2022, x="Place", y="Amt", size="Exits",height=700, hover_name='Place')

fig.update_layout(
    yaxis_range = [ 0, 100000 ],
    width=650, 
)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    html.Div([
        dcc.Graph(
        id='example-graph',
        figure=fig, 
        style={'display': 'inline-block', 'width': '20%'}),
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0'}),
    html.Div([
        dcc.Graph(id='res-time-series'),
        dcc.Graph(id='bus-time-series'),
        dcc.Graph(id='lightind-time-series'),
    ], style={'display': 'inline-block', 'width': '20%'}),
     html.Div([
        dcc.Graph(
            id='type-bar',
            style={'display': 'inline-block', 'width': '80%'}),
    ], style={'display': 'inline-block', 'width': '30%', 'padding': '0'}),
])


@app.callback(
    Output('res-time-series', 'figure'),
    Input('example-graph', 'hoverData'),
    #inputs required for the values to be filtered by. Can use a different dataframe for that.
)
def update_res_timeseries(hoverData):
    base_df = pd.read_csv('./test.csv')
    val = 'Downtown'
    if hoverData != None:
        val = hoverData['points'][0]['x']
    dff = base_df.loc[base_df['place'] == val]
    df = dff.loc[dff['type'] == 'residential']
    fig = px.scatter(df, x="year", y="amt",height=300, hover_name='type')
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False, dtick=2)
    fig.update_yaxes(type='linear', range=[0, 8000], dtick=2000)
    fig.update_layout(height=250, margin={'l': 20, 'b': 30, 'r': 10, 't': 20}, title=dict(
        text='<b>Residential</b>',
        x=0.60,
        y=0.97,
        font=dict(
            family="Arial",
            size=12,
            color='#000000'
        )))
    return fig    

@app.callback(
    Output('bus-time-series', 'figure'),
    Input('example-graph', 'hoverData'),
    #inputs required for the values to be filtered by. Can use a different dataframe for that.
)
def update_bus_timeseries(hoverData):
    base_df = pd.read_csv('./test.csv')
    val = 'Downtown'
    if hoverData != None:
        val = hoverData['points'][0]['x']
    dff = base_df.loc[base_df['place'] == val]
    df = dff.loc[dff['type'] == 'business']
    fig = px.scatter(df, x="year", y="amt",height=300, hover_name='type')
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False, dtick=2)
    fig.update_yaxes(type='linear', range = [0, 50000], dtick=20000)
    fig.add_annotation(x=0, y=1.3, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text='Business')
    fig.update_layout(height=250, margin={'l': 20, 'b': 30, 'r': 10, 't': 20},title=dict(
        text='<b>Business</b>',
        x=0.60,
        y=0.96,
        font=dict(
            family="Arial",
            size=12,
            color='#000000'
        )))
    return fig    

@app.callback(
    Output('lightind-time-series', 'figure'),
    Input('example-graph', 'hoverData'),
    #inputs required for the values to be filtered by. Can use a different dataframe for that.
)
def update_light_timeseries(hoverData):
    base_df = pd.read_csv('./test.csv')
    val = 'Downtown'
    if hoverData != None:
        val = hoverData['points'][0]['x']
    dff = base_df.loc[base_df['place'] == val]
    df = dff.loc[dff['type'] == 'lightindustry']
    fig = px.scatter(df, x="year", y="amt",height=200, hover_name='type')
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False, dtick=2)
    fig.update_yaxes(type='linear', range = [0, 350000], dtick=50000)
    fig.update_layout(height=250, margin={'l': 20, 'b': 30, 'r': 10, 't': 35}, title=dict(
        text='<b>Light Industry</b>',
        x=0.60,
        y=0.91,
        font=dict(
            family="Arial",
            size=12,
            color='#000000'
        )))
    return fig    


@app.callback(
    Output('type-bar', 'figure'),
    Input('example-graph', 'hoverData'),
    #inputs required for the values to be filtered by. Can use a different dataframe for that.
)
def update_barchart_timeseries(hoverData):
    base_df = pd.read_csv('./test.csv')
    val = 'Downtown'
    if hoverData != None:
        val = hoverData['points'][0]['x']
    dff = base_df.loc[base_df['place'] == val]
    df = dff.loc[dff['type'] == 'lightindustry']
    fig = px.bar(df, x="year", y="amt",height=550)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(range=[50000, 400000])
    fig.update_layout(margin={'l': 120, 'r': 20, 'b': 250}, title=dict(
        text='<b>Bar Chart</b>',
        x=0.70,
        y=0.91,
        font=dict(
            family="Arial",
            size=12,
            color='#000000'
        )))
    return fig    
    
    


if __name__ == '__main__':
    app.run_server(debug=True)
