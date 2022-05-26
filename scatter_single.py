import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback
from vars import *
import requests
import re
import plotly.express as px
from app_secrets import *
from tools import *
from callbacks import *

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

scatter_plot_x_vars=[
	'voyage_dates__imp_arrival_at_port_of_dis_yyyy',
	'voyage_dates__imp_length_home_to_disembark',
	'voyage_dates__length_middle_passage_days',
	'voyage_crew__crew_voyage_outset',
	'voyage_crew__crew_first_landing',
	'voyage_slaves_numbers__imp_total_num_slaves_embarked',
	'voyage_slaves_numbers__imp_total_num_slaves_disembarked'
	]

scatter_plot_y_vars=[
	'voyage_slaves_numbers__imp_total_num_slaves_embarked',
	'voyage_slaves_numbers__imp_total_num_slaves_disembarked',
	'voyage_slaves_numbers__percentage_female',
	'voyage_slaves_numbers__percentage_male',
	'voyage_slaves_numbers__percentage_child',
	'voyage_slaves_numbers__percentage_men_among_embarked_slaves',
	'voyage_slaves_numbers__percentage_women_among_embarked_slaves',
	'voyage_slaves_numbers__imp_mortality_ratio',
	'voyage_slaves_numbers__imp_jamaican_cash_price',
	'voyage_slaves_numbers__percentage_boys_among_embarked_slaves',
	'voyage_slaves_numbers__percentage_girls_among_embarked_slaves',
	'voyage_ship__tonnage_mod',
	'voyage_crew__crew_voyage_outset',
	'voyage_crew__crew_first_landing'
]

scatter_plot_factors=[
	'voyage_ship__imputed_nationality__name',
	'voyage_itinerary__imp_principal_region_of_slave_purchase__region',
	'voyage_itinerary__imp_broad_region_of_slave_purchase__broad_region',
	'voyage_itinerary__imp_broad_region_slave_dis__broad_region'
]

app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label('X variable'),
                    dcc.Dropdown(
                        id='scatter_x_var',
                        options=[{'label':md[i]['flatlabel'],'value':i} for i in scatter_plot_x_vars],
                        value=scatter_plot_x_vars[0],
                        multi=False
                    )
                ]),
                width=4,xs=12,sm=12,md=12,lg=6
            ),
            dbc.Col(
                html.Div([
                    html.Label('Y variable'),
                    dcc.Dropdown(
                        id='scatter_y_var',
                        options=[{'label':md[i]['flatlabel'],'value':i} for i in scatter_plot_y_vars],
                        value=scatter_plot_y_vars[0],
                        multi=False
                    )
                ]),
                width=4,xs=12,sm=12,md=12,lg=6
            ),

            dbc.Col(
                html.Div([
                    html.Label('Factor'),
                    dcc.Dropdown(
                        id='scatter_factor',
                        options=[{'label':md[i]['flatlabel'],'value':i} for i in scatter_plot_factors],
                        value=scatter_plot_factors[0],
                        multi=False
                    )
                ]),
                width=4,xs=12,sm=12,md=12,lg=6
            )
        ]),
        dbc.Row([
            html.Div([
                html.Label('Totals/Sums or Averages'),
                dcc.RadioItems(
                    id='scatter_agg_mode',
                    options=[{'label': i, 'value': i} for i in ['Totals/Sums','Averages']],
                    value='Totals/Sums',
                    labelStyle={'display': 'inline'}
                )
            ])
        ]),
        # dbc.Row(
        #     dcc.Graph(id="bar-graph")
        # )
        dcc.Graph(id="bar-graph")
    ]
)

@callback(
    Output('bar-graph', 'figure'),
    Input('scatter_x_var', 'value'),
    Input('scatter_y_var', 'value'),
    Input('scatter_factor', 'value'),
    Input('scatter_agg_mode', 'value')
)
def update_bar_graph(x_var, y_var, factor, agg_mode):
    global md

    data={
        'selected_fields':[x_var, y_var, factor],
        'cachename':['voyage_xyscatter']
    }

    print(data)

    df, results_count=update_df(base_url+'voyage/caches', data=data)


    yvarlabel=md[y_var]['flatlabel']
    xvarlabel=md[x_var]['flatlabel']


    colors=df[factor].unique()
    for color in colors:
        df2=df[df[factor]==color]
        trace_name=color
    
    if agg_mode=='Averages':
        df2=df.groupby([x_var, factor]).mean()
        df2=df2.reset_index()

    elif agg_mode=='Totals/Sums':
        df2=df.groupby([x_var, factor]).sum()
        df2=df2.reset_index()

    fig = px.scatter(df2, x=x_var, y=y_var, color=factor,
        labels={
            y_var:yvarlabel,
			x_var:xvarlabel
            }
        )


    del df

    return fig

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
