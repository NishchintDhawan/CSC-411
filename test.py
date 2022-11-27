from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import os
import glob

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)


df_2022 = pd.DataFrame({
    "Place": ["Downtown","James Bay", "Harris Green" , "Victoria West", "Rock Bay"],
    "Amt": [95199.71, 31933.15503, 84278.61205, 54624.10574, 66599.85236],
    "Exits": [0, 1, 0, 5, 1],
    "SizeVal" : [1, 2, 1, 6, 2]
})

fig = px.scatter(df_2022, x="Place", y="Amt", size="SizeVal",height=700, hover_name='Place', labels={
                     "Place": "Neighborhood",
                     "Amt": "Amount in CAD",
                     "Exits": "Emergency Exits"
                 },
                  custom_data=['Place', 'Amt', 'Exits']
                 )

fig.update_layout(
    yaxis_range = [ 0, 100000 ],
    width=700, title=dict(
        text='<b>Year 2022</b>',
        x=0.128,
        y=0.945,
        font=dict(
            family="Arial",
            size=14,
            color='#000000'
        ))
)
fig.update_xaxes(tickfont = dict(size=13), titlefont=dict(size=13))
fig.update_yaxes(tickfont = dict(size=13), range=[0, 150000], titlefont=dict(size=13))

fig.update_traces(hovertemplate='%{x} <br> <br> Emergency Blocks: <b> %{customdata[2]} </b>')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    html.Div(['Property tax for various regions of City of Victoria'], style={'marginTop': '2%', 'width': '100%', 'marginLeft': '35%', 'fontSize': '16px'}),
    html.Div([
        html.Div([
            dcc.Graph(
            id='example-graph',
            figure=fig, 
            style={'display': 'inline-block', 'width': '20%'}),
        ], style={'width': '50%', 'display': 'inline-block', 'paddingLeft': '60px'}),
        html.Div([
            html.Div(id='text-title', style={'display': 'inline-block', 'marginLeft': '10%', 'display': 'inline-block', 'marginLeft': '14%', 'fontSize': '16px', 'fontWeight': '600'}),
            dcc.Graph(id='res-time-series', style={'width':'85%', 'marginTop': '5%'}),
            dcc.Graph(id='bus-time-series', style={'width':'85%'}),
        ], style={'display': 'inline-block', 'width': '20%', 'paddingBottom' : '20px', 'marginTop': '70px'}),
        html.Div([
        dcc.Graph(id='lightind-time-series', style={'width': '85%', 'marginTop': '7%'}),
        dcc.Graph(id='type-bar', style={'width': '86%', 'marginLeft':'2%'}),
        ], style={'display': 'inline-block', 'width': '20%', 'paddingBottom' : '56px', 'marginTop': '95px'}),
    ], style={'display': 'flex'})
])



@app.callback(
    Output('text-title', 'children'),
    Input('example-graph', 'hoverData'),
    #inputs required for the values to be filtered by. Can use a different dataframe for that.
)
def update_title_text(hoverData):
    val = 'Downtown'
    if hoverData != None:
        val = hoverData['points'][0]['x']
    return val

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
    fig = px.scatter(df, x="year", y="amt",height=300, hover_name='type', labels={
                     "year": "Year",
                     "amt": "Amount in CAD",
                 })
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False, dtick=2, tickfont = dict(size=10), titlefont=dict(size=10))
    fig.update_yaxes(type='linear', range=[0, 8000], dtick=2000, tickfont = dict(size=10), titlefont=dict(size=10))
    fig.update_layout(height=250, margin={'l': 20, 'b': 30, 'r': 10, 't': 20}, title=dict(
        text='Residential',
        x=0.60,
        y=0.97,
        font=dict(
            family="Arial",
            size=12,
            color='#000000'
        )))
    fig.update_traces(hovertemplate='Year: %{x} <br> Amount: <b> %{y} </b>')
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
    fig = px.scatter(df, x="year", y="amt",height=300, hover_name='type', labels={
                     "year": "Year",
                     "amt": "Amount in CAD",
                 })
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False, dtick=2, tickfont = dict(size=10), titlefont=dict(size=10), title_font_color="green")
    fig.update_yaxes(type='linear', range = [0, 50000], dtick=20000, tickfont = dict(size=10), titlefont=dict(size=10), title_font_color="green")
    fig.update_layout(height=250, margin={'l': 20, 'b': 30, 'r': 10, 't': 30},title=dict(
        text='Business',
        x=0.60,
        y=0.93,
        font=dict(
            family="Arial",
            size=13,
            color='#000000'
        )))
    fig.update_traces(hovertemplate='Year: %{x} <br> Amount: <b> %{y} </b>')
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
    fig = px.scatter(df, x="year", y="amt",height=200, hover_name='type', labels={
                     "year": "Year",
                     "amt": "Amount in CAD",
                 },)
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False, dtick=2, tickfont = dict(size=10), titlefont=dict(size=10), title_font_color="green")
    fig.update_yaxes(type='linear', range = [0, 350000], dtick=50000, tickfont = dict(size=10), titlefont=dict(size=10), title_font_color="green")
    fig.update_layout(height=255, margin={'l': 20, 'b': 50, 'r': 10, 't': 10}, title=dict(
        text='<b>Light Industry</b>',
        x=0.60,
        y=0.98,
        font=dict(
            family="Arial",
            size=12,
            color='#000000'
        )))
    fig.update_traces(hovertemplate='Year: %{x} <br> Amount: <b> %{y} </b>')
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
    fig = px.bar(df, x="year", y="amt",height=240, labels={
                     "year": "Year",
                     "amt": "Amount in CAD",
                 })
    fig.update_xaxes(showgrid=False, tickfont = dict(size=10), titlefont=dict(size=10), title_font_color="green")
    fig.update_yaxes(range=[50000, 400000], dtick=50000, tickfont = dict(size=10), titlefont=dict(size=10), title_font_color="green")
    fig.update_layout(margin={'l': 30, 'r': 20, 'b': 0, 't': 20}, title=dict(
        text='Bar Chart',
        x=0.55,
        y=0.97,
        font=dict(
            family="Arial",
            size=12,
            color='#000000'
        )))
    fig.update_traces(hovertemplate='Year: %{x} <br> Amount: <b> %{y} </b>')
    return fig    
    
    


if __name__ == '__main__':
    app.run_server(debug=True)
