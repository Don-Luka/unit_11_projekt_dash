from dash import dcc, html
import plotly.graph_objects as go

def render_tab(df):

    grouped = df[(df['total_amt']>0)].pivot_table(index='country',columns='Store_type',values='total_amt',aggfunc='sum')\
        .assign(_sum=lambda x: x['Flagship store']+x['MBR']+x['TeleShop']+x['e-Shop'])\
        .sort_values(by='_sum').round(2)

    traces = []
    for col in grouped.columns[:-1]:
        traces.append(go.Bar(x=grouped[col],y=grouped.index,orientation='h',name=col))
    data = traces
    fig = go.Figure(data=data,layout=go.Layout(barmode='stack', title='Sprzedaż według państw'))

    layout = html.Div([html.H1('Kanały sprzedaży',style={'text-align':'center'}),

                        html.Div([html.Div([dcc.Graph(id='pie-store-type-countries',figure=fig)],style={'width':'50%'}),
                        html.Div([dcc.RadioItems(id='store_radio',
                                    options=[{'label':store_type,'value':store_type} for store_type in df['Store_type'].unique()],
                                    value=df['Store_type'].unique()[0]),
                                    dcc.Graph(id='pie-store-weekday')],style={'width':'50%'})],style={'display':'flex'}),
                                    html.Div(id='temp-out')
                        ])

    return layout
