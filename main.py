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

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                df['Hashtags'].unique(),
                "#Nature",
                id='xaxis-column'
            ),
            dcc.RadioItems(
                ['Filter by hashtags', 'Filter by country'],
                'Filter by hashtags',
                id='filter-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                df['Country'].unique(),
                "USA",
                id='yaxis-column'
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
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('filter-type', 'value'),
    Input('yaxis-type', 'value')
    )
def update_graph(xaxis_column_name, yaxis_column_name, filter_type, yaxis_type):
    if filter_type == "Filter by hashtags":
        dff = df[(df['Hashtags'] == xaxis_column_name)]
    elif filter_type == "Filter by country":
        dff = df[(df['Country'] == yaxis_column_name)]

    print(dff[yaxis_type])

    fig = px.scatter(x=pd.to_datetime(dff['Timestamp']),
                     y=dff[yaxis_type],
                     hover_name=dff['Sentiment'],
                     color=dff['Sentiment'],
                     trendline="lowess",
                     trendline_scope="overall"
                     )

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig

if __name__ == '__main__':
    app.run(debug=True)