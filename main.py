from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc

df = pd.read_csv('sentimentdataset.csv')

# splitting hashtags into one per row
df['Country'] = df['Country'].str.strip()
df['Hashtags'] = (df['Hashtags'].str.strip()).str.split(' ')
df = df.explode('Hashtags').reset_index(drop=True)
print(df)
app = Dash()

app.layout = html.Div(children=[
    html.H1(children='Likes/Retweets on Social Media Posts Over Time by Country or Hashtag'),

    html.Div(children='''
        Can be used to visualise trends or sentiment over time.

    '''),
    html.Div([

        html.Div([
            dcc.Dropdown(
                df['Country'].unique(),
                "USA",
                id='country-filter'
            ),
            dcc.RadioItems(
                ['Filter by country', 'Filter by hashtags'],
                'Filter by country',
                id='filter-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                df['Hashtags'].unique(),
                "#Nature",
                id='hashtag-filter'
            ),
            dcc.RadioItems(
                ['Likes', 'Retweets'],
                'Likes',
                id='yaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

])


@callback(
    Output('indicator-graphic', 'figure'),
    Input('country-filter', 'value'),
    Input('hashtag-filter', 'value'),
    Input('filter-type', 'value'),
    Input('yaxis-type', 'value')
    )
def update_graph(country_filter_name, hashtag_filter_name, filter_type, yaxis_type):
    if filter_type == "Filter by hashtags":
        dff = df[(df['Hashtags'] == hashtag_filter_name)]
    elif filter_type == "Filter by country":
        dff = df[(df['Country'] == country_filter_name)]

    print(dff[yaxis_type])

    fig = px.scatter(x=pd.to_datetime(dff['Timestamp']),
                     y=dff[yaxis_type],
                     color=dff['Sentiment'],
                     trendline="lowess",
                     trendline_scope="overall",
                     data_frame=dff,
                     custom_data=['Sentiment', 'Platform']
                     )

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_traces(hovertemplate=f'{yaxis_type}'+
        ': %{y}'+
        '<br>Date: %{x}'+
        '<br>Sentiment: %{customdata[0]}'+
        '<br>Platform: %{customdata[1]}'+
        '<extra></extra>')

    fig.update_xaxes(title="Timestamp")

    fig.update_yaxes(title=yaxis_type)

    return fig

if __name__ == '__main__':
    app.run(debug=True)