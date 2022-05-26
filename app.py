import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback
# from vars import *
import plotly.express as px
import pandas as pd
from app_secrets import *
# from tools import *
# from callbacks import *
import requests
import re
import json

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server


md2={
	'voyage_id':'Voyage ID',
	'voyage_itinerary__imp_principal_region_slave_dis__region':'Principal Region of Disembarkation *',
	'voyage_itinerary__imp_principal_region_of_slave_purchase__region':'Principal Region of Purchase *',
	'voyage_captainconnection__captain__name':'Captain\'s name',
	'voyage_crew__crew_died_complete_voyage':'Crew deaths during voyage',
	'voyage_crew__crew_first_landing':'Crew at first landing of slaves',
	'voyage_crew__crew_voyage_outset':'Crew at voyage outset',
	'voyage_dates__date_departed_africa':'Date departed Africa',
	'voyage_dates__length_middle_passage_days':'Middle passage (days)',
	'voyage_dates__imp_arrival_at_port_of_dis_yyyy':'Year arrived with captives *',
	'voyage_dates__imp_length_home_to_disembark':'Days from homeport to landing (days) *',
	'voyage_itinerary__imp_port_voyage_begin__place':'Place where voyage began *',
	'voyage_itinerary__port_of_call_before_atl_crossing__place':'Port of call before Atlantic crossing',
	'voyage_itinerary__imp_principal_place_of_slave_purchase__place':'Principal place of purchase *',
	'voyage_itinerary__first_place_slave_purchase__place':'1st place of purchase',
	'voyage_itinerary__second_place_slave_purchase__place':'2nd place of purchase',
	'voyage_itinerary__third_place_slave_purchase__place':'3rd place of purchase',
	'voyage_itinerary__imp_principal_port_slave_dis__place':'Principal place of landing *',
	'voyage_itinerary__first_landing_place__place':'1st landing place',
	'voyage_itinerary__second_landing_place__place':'2nd landing place',
	'voyage_itinerary__third_landing_place__place':'3rd landing place',
	'voyage_itinerary__place_voyage_ended__place':'Place voyage ended',
	'voyage_slaves_numbers__imp_total_num_slaves_embarked':'Total embarked *',
	'voyage_slaves_numbers__imp_total_num_slaves_disembarked':'Total disembarked *',
	'voyage_slaves_numbers__num_slaves_carried_first_port':'Arrived 1st port',
	'voyage_slaves_numbers__imp_mortality_during_voyage':'Mortality *',
	'voyage_slaves_numbers__imp_mortality_ratio':'Mortality ratio *',
	'voyage_ship__guns_mounted':'Guns mounted',
	'voyage_ship__ship_name':'Vessel name',
	'voyage_ship__rig_of_vessel__name':'Rig of vessel',
	'voyage_ship__imputed_nationality__name':'Ship nationality *',
	'voyage_ship__registered_place__place':'Ship registration place',
	'voyage_ship__registered_year':'Ship registration year',
	'voyage_ship__tonnage':'Ship tonnage',
	'voyage_ship__tonnage_mod':'Ship modern tonnage',
	'voyage_ship__vessel_construction_place__place':'Ship constructin place',
	'voyage_ship__year_of_construction':'Ship construction year',
	'voyage_outcome__outcome_owner__name':'Owner outcome',
	'voyage_outcome__vessel_captured_outcome__name':'Vessel captured outcome',
	'voyage_outcome__outcome_slaves__name':'Captives\' outcome',
	'voyage_outcome__particular_outcome__name':'Particular outcome',
	'voyage_outcome__resistance__name':'Resistance',
	'voyage_sourceconnection__source__full_ref':'Source(s)',
	'voyage_shipownerconnection__owner__name':'Owner name(s)'
}

#overwrite flatlabels w custom flatlabels enumerated above
r=requests.options(base_url+'voyage/?hierarchical=False',headers=headers)
md=json.loads(r.text)
for m in md2:
	md[m]['flatlabel']=md2[m]

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

def update_df(url,data):
	global headers
	r=requests.post(url,data=data,headers=headers)
	j=r.text
	
	try:
		results_count=r.headers['results_count']
	except:
		results_count=None
	df=pd.read_json(j)
	return df,results_count

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

if __name__ == '__main__':
    app.run_server(debug=True)  # Turn off reloader if inside Jupyter
