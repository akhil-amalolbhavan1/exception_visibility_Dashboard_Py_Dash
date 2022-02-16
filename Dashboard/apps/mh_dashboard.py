# Owner : Akhil A
# Version V1
# Created on :

from dash_core_components.Graph import Graph
from dash_html_components.Div import Div
from numpy.core.fromnumeric import size
import pandas as pd
import plotly.express as px
import numpy as np
#import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from dash_extensions.enrich import ServersideOutput, Trigger
import plotly.graph_objs as go
import dash_table
import plotly.express as px
from datetime import datetime as dt,timedelta
import os
import dash_bootstrap_components as dbc

from plotly.graph_objs import bar
from dashboard import app

mhdf = pd.read_csv(os.getcwd() +'/Dashboard/data/mh_full_data.csv', low_memory=False)
# mhdf['month_year'] = ['-'.join(i) for i in zip(mhdf["month"].map(str),mhdf["year"].map(str))]
mhdf['month_year'] = pd.to_datetime(mhdf['scanned_date']).dt.month_name().str.slice(stop=3)+"-"+mhdf["year"].map(str)
mhdf.zone = mhdf.zone.fillna('NA')
# mhdf['month_year'] = pd.to_datetime(mhdf['month_year']).dt.date.astype(str)


color_code = ['crimson','darkgreen','darkorange','blue','red', 'maroon', 'teal', 'darkblue', 'magenta','yellow','lightgreen']
# print(mhdf.columns)
overall_pivot = pd.DataFrame(pd.pivot_table(mhdf, index=['month_year'], values=['exception_log_timestamp'], aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})
zone_pivot = pd.DataFrame(pd.pivot_table(mhdf, index=['month_year','zone'], values=['exception_log_timestamp'], fill_value='NA', aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})
zone_hub_pivot = pd.DataFrame(pd.pivot_table(mhdf, index=['month_year','zone','hub_name'], values=['exception_log_timestamp'], fill_value='NA', aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})
# print(zone_pivot)


# def func_load_data(mhdf):
#     mhdf['month_year'] = pd.to_datetime(mhdf['month_year']).dt.month_name().str.slice(stop=3)+"-"+mhdf["year"].map(str)
#     mhdf.zone = mhdf.zone.fillna('NA')
#     mhdf['month_year'] = pd.to_datetime(mhdf['month_year']).dt.date.astype(str)
#     overall_pivot = pd.DataFrame(pd.pivot_table(mhdf, index=['month_year'], values=['exception_log_timestamp'], aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})
#     zone_pivot = pd.DataFrame(pd.pivot_table(mhdf, index=['month_year','zone'], values=['exception_log_timestamp'], fill_value='NA', aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})
#     zone_hub_pivot = pd.DataFrame(pd.pivot_table(mhdf, index=['month_year','zone','hub_name'], values=['exception_log_timestamp'], fill_value='NA', aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})
#     cat_order = ['Jan-2021','Feb-2021','Mar-2021','Apr-2021','May-2021','Jun-2021','Jul-2021','Aug-2021','Sep-2021','Oct-2021','Nov-2021','Dec-2021','Jan-2022','Feb-2022','Mar-2022','Apr-2022','May-2022','Jun-2022',
#             'Jul-2022','Aug-2022','Sep-2022','Oct-2022','Nov-2022','Dec-2022','Jan-2023','Feb-2023','Mar-2023','Apr-2023','May-2023','Jun-2023','Jul-2023','Aug-2023','Sep-2023','Oct-2023','Nov-2023','Dec-2023']
#     df_sorter = pd.DataFrame(data ={ 'month_year': cat_order,
#                                 'priority':[1,	2,	3,	4,	5,	6,	7,	8,	9,	10,	11,	12,	13,	14,	15,	16,	17,	18,	19,	20,	21,	22,	23,	24,	25,	26,	27,	28,	29,	30,	31,	32,	33,	34,	35,	36]})
#     overall_pivot = pd.merge(overall_pivot,df_sorter,on='month_year', how='left').sort_values(by='priority')
#     zone_hub_pivot = pd.merge(zone_hub_pivot,df_sorter,on='month_year', how='left').sort_values(by='priority')
#     return overall_pivot, zone_pivot, zone_hub_pivot



cat_order = ['Jan-2021','Feb-2021','Mar-2021','Apr-2021','May-2021','Jun-2021','Jul-2021','Aug-2021','Sep-2021','Oct-2021','Nov-2021','Dec-2021','Jan-2022','Feb-2022','Mar-2022','Apr-2022','May-2022','Jun-2022',
            'Jul-2022','Aug-2022','Sep-2022','Oct-2022','Nov-2022','Dec-2022','Jan-2023','Feb-2023','Mar-2023','Apr-2023','May-2023','Jun-2023','Jul-2023','Aug-2023','Sep-2023','Oct-2023','Nov-2023','Dec-2023']
df_sorter = pd.DataFrame(data ={ 'month_year': cat_order,
                                'priority':[1,	2,	3,	4,	5,	6,	7,	8,	9,	10,	11,	12,	13,	14,	15,	16,	17,	18,	19,	20,	21,	22,	23,	24,	25,	26,	27,	28,	29,	30,	31,	32,	33,	34,	35,	36]})

date_column_name = ''
overall_pivot.month_year = overall_pivot.month_year.astype('category')
overall_pivot.month_year.cat.set_categories(cat_order, inplace=True)
overall_pivot = pd.merge(overall_pivot,df_sorter,on='month_year', how='left').sort_values(by='priority')
zone_hub_pivot = pd.merge(zone_hub_pivot,df_sorter,on='month_year', how='left').sort_values(by='priority')
# print(overall_pivot)
dd_mh_name = mhdf.hub_name.unique().tolist()
dd_mh_name.append('All')
dd_mh_name.remove(np.nan)

dd_date_agg_values = ['Day Wise','Week Wise', 'Month Wise']

# print(dd_mh_name)

# print(overall_pivot)
# def layout(mhdf): 
#     global overall_pivot, zone_pivot, zone_hub_pivot
#     overall_pivot, zone_pivot, zone_hub_pivot = func_load_data(mhdf)
#     print(mhdf)
#     dd_mh_name = mhdf.hub_name.unique().tolist()
#     dd_mh_name.append('All')
#     dd_mh_name.remove(np.nan)
def get_layout(df):
    global mhdf
    mhdf = df
    mhdf['month_year'] = pd.to_datetime(mhdf['scanned_date']).dt.month_name().str.slice(stop=3)+"-"+mhdf["year"].map(str)
    mhdf.zone = mhdf.zone.fillna('NA')
    # layout = html.Div([dcc.Store(id='full_data', data=mhdf.to_json(date_format='iso', orient='split')),
    #             html.Div(id="onload"),
    layout = html.Div([html.H1('MH Dashboard', style={'textAlign':'center', 'width':'100%', 'display':'inline-block'}),
            html.Div([
                html.Div([
                    html.Label(['Choose the x axis for date'], style={'color':'black','width':'100%','textAlign':'left'}),
                                dcc.Dropdown(id='dd_date_agg',
                                        options = [{'label':name, 'value':name} for name in dd_date_agg_values],
                                        value = 'Month Wise', multi=False #multi=True,clearable=False,
                                        )],style={'width':'30%','align':'right', 'margin': '0 auto'}),
                html.Br(),
                    dcc.Graph(id='overall_trend',
                    figure = go.Figure())
            ]),
            html.Div([
                    dcc.Graph(id = 'zone_trend',
                    figure = go.Figure(),
                                    style={'width':'100%', 'display':'inline-block'}
                                    )
            ], style={'oveflow':'hidden'}),
            html.Div([
                dcc.Graph(id='hubwise_bubble',
                figure = go.Figure(),
            #     figure = px.scatter(zone_hub_pivot, 
            #                         x='month_year', 
            #                         y="orphan_count", 
            #                         color="hub_name", 
            #                         facet_col='zone',
            #                         size="orphan_count", size_max=50, 
            #                         template= {'layout':{'paper_bgcolor':'#ffffe6', 'plot_bgcolor':'#aebfd0', 'showlegend':False,
            #                                             'xaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1, 'fixedrange':True},
            #                                             'yaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1, 'fixedrange':True},
            #                                                 }},
            #  title="Zone-Hub wise MoM Exceptions",
            #  labels={"month_year":"Months",
            #         "orphan_count":"Exceptions Generated",
            #         "hub_name":'Hubs'} # customize label,
            
            #             )
                        )
            ]),
            html.Div([
                html.Div([
                    html.Label(['Choose Hub Name to see Hub wise details'], style={'color':'white','width':'50%','textAlign':'center'}),
                                dcc.Dropdown(id='dd_mhname',
                                        options = [{'label':name, 'value':name} for name in dd_mh_name],
                                        value = 'All', multi=False #multi=True,clearable=False,
                                        )],style={'width':'30%','align':'center', 'margin': '0 auto'}),
                html.Br(),
                html.Div([
                    dcc.Graph(id = 'exception_type_trend',
                                            # figure = go.Figure(),
                                            figure=go.Figure(), 
                                                        style={'width':'100%', 'display':'inline-block', 'border-style':'solid', 'border-color':'#405972', 'backgroundColor':'#33475b'}),
                    
                ])
            ], style={'background-color':'#33475b'})
            ])
    return layout


# @app.callback(ServersideOutput("store", "data"), Trigger("onload", "children"))
# def query_df():
#     print('Entered here')
#     mhdf = pd.read_csv(os.getcwd() +'/Dashboard/data/mh_full_data.csv', low_memory=False)
#     return mhdf


@app.callback(
    [Output('exception_type_trend','figure')],
    [Input('dd_mhname','value'),
    Input('dd_date_agg','value'),]
    )
def update_exception_graph(dd_mhname_value,dd_date_agg_value, ):
    column_name = ''
    tickformat = ''
    xaxis_name =''
    # print(data_val)
    # mhdf = pd.read_json(data_val, orient='split')
    # print(mhdf)
    # dd_date_agg_value = date_column_name
    # print('inside dd mhname')
    # print(dd_date_agg_value)
    if dd_date_agg_value=='Day Wise':
        tickformat = '%Y-%b-%d'
        xaxis_name = 'Scanned Date'
        column_name = 'scanned_date'
    elif dd_date_agg_value == 'Week Wise':
        column_name = 'weeknum'
        xaxis_name = 'Week'
    else:
        column_name = 'month_year'
        tickformat = '%Y-%b'
        xaxis_name = 'Months'
    if dd_mhname_value=='All':
        exception_type_pivot = generate_pivots(mhdf, column_name)
    else:
        exception_type_pivot = generate_pivots(mhdf[mhdf.hub_name==dd_mhname_value], column_name)
    # print(column_name)
    # print(exception_type_pivot)
    if exception_type_pivot.empty:
        exception_type_fig = func_exception_type_fig(pd.DataFrame(columns=['exception_type','orphan_count']), column_name, tickformat, xaxis_name)
    else:
        exception_type_fig = func_exception_type_fig(exception_type_pivot, column_name, tickformat, xaxis_name)
        # excp_data, excp_column = fun_datatable_column_data(exception_type_pivot)
    
    return [exception_type_fig]

@app.callback([Output('overall_trend','figure'),
                Output('zone_trend','figure'),
                Output('hubwise_bubble', 'figure'),
                # Output('exception_type_trend','figure')
                ],
                [Input('dd_date_agg','value')]
        )
def update_figure_dateagg(dd_date_agg_value):
    # print(dd_date_agg_value)
    global date_column_name 
    date_column_name = dd_date_agg_value
    column_name = ''
    tickformat = ''
    xaxis_name =''
    if dd_date_agg_value=='Day Wise':
        tickformat = '%Y-%b-%d'
        column_name = 'scanned_date'
        xaxis_name = 'Scanned Date'
    elif dd_date_agg_value == 'Week Wise':
        column_name = 'weeknum'
        xaxis_name = 'Week'
    else:
        column_name = 'month_year'
        tickformat = '%Y-%b'
        xaxis_name = 'Months'
    # print(column_name) 
    overall_pivot, zone_pivot, zone_hub_pivot  = func_generate_pivots(mhdf, column_name)
    
    # print(overall_pivot)
    overall_exception_trend_fig = func_generate_overal_trend_figure(overall_pivot, column_name,tickformat,xaxis_name)
    zone_trend_fig = func_generate_zone_trend_figure(zone_pivot, column_name, xaxis_name)
    zone_hub_fig = func_generate_zone_hub_bubble_fig(zone_hub_pivot, column_name, xaxis_name)
    # update_exception_graph('All')
    return [overall_exception_trend_fig, zone_trend_fig, zone_hub_fig]

def func_generate_pivots(df, date_agg_column):
    overall_pivot = pd.DataFrame(pd.pivot_table(df, index=[date_agg_column], values=['exception_log_timestamp'], aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})
    zone_pivot = pd.DataFrame(pd.pivot_table(df, index=[date_agg_column,'zone'], values=['exception_log_timestamp'], fill_value='NA', aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})
    zone_hub_pivot = pd.DataFrame(pd.pivot_table(df, index=[date_agg_column,'zone','hub_name'], values=['exception_log_timestamp'], fill_value='NA', aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})
    # exception_type_pivot = pd.DataFrame(pd.pivot_table(df, index=[date_agg_column,'exception_type'], values=['exception_log_timestamp'], aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})

    if date_agg_column=='month_year':
        overall_pivot = pd.merge(overall_pivot,df_sorter,on='month_year', how='left').sort_values(by='priority')
        zone_hub_pivot = pd.merge(zone_hub_pivot,df_sorter,on='month_year', how='left').sort_values(by='priority')
        
    return overall_pivot, zone_pivot, zone_hub_pivot

def generate_pivots(df, date_agg):
    # print('insdie exception pivot')
    # print(date_agg)
    exception_type_pivot = pd.DataFrame(pd.pivot_table(df, index=[date_agg,'exception_type'], values=['exception_log_timestamp'], aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})
    if date_agg=='month_year':
        exception_type_pivot = pd.merge(exception_type_pivot,df_sorter,on='month_year', how='left').sort_values(by='priority')
    # hub_pivot = pd.DataFrame(pd.pivot_table(df, index=['month_year','exception_type'], values=['exception_log_timestamp'], aggfunc=len)).reset_index().rename(columns={'exception_log_timestamp': 'orphan_count'})
    return exception_type_pivot

def func_generate_overal_trend_figure(df, date_agg, tickformat, xasisname):
    figure = go.Figure({
                    'data':[go.Scatter(x=df[date_agg],
                                        y=df.orphan_count,
                                        line = dict(color='firebrick', width=2),
                                        # xperiod='M7',
                                        mode='markers+lines')],
                    'layout':{'title':'Overall Excpetions generation Trend',
                                # 'xaxis':{'title':'Business Units'},
                                'yaxis':{'title':'Exceptions Generated'},
                                'paper_bgcolor':'#ffffe6',
                                'plot_bgcolor':'#aebfd0',
                                'font':dict(
                                    family="sans serif",
                                    size=14,
                                    color="black"
                                ),
                                'xaxis' : dict(
                                        tickformat = tickformat, # hide dates with no values
                                        title=xasisname,
                                        # tickmode = 'array',
                                        # ticklabelmode="period", dtick="M1",
                                        # showgrid=False,
                                        nticks =7,
                                        ticktext = df[date_agg],
                                        tickvals = df[date_agg].unique(),
                                        # tick0 = 1.0,
                                        tickangle = 35)
                                }
                        })
    return figure

def func_generate_zone_trend_figure(df, date_agg, xasisname):
    figure = px.bar(df, x=date_agg, y='orphan_count', color='zone', 
                            barmode='group', orientation='v', category_orders={'month_year':cat_order},
                            template= {'layout':{'paper_bgcolor':'#ffffe6', 'plot_bgcolor':'#aebfd0',
                                                'xaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,},
                                                'yaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,}
                                                }},
                            labels={'scanned_date' if xasisname=='Scanned Date' else ('weeknum' if xasisname=='Week' else 'month_year'):xasisname,
                                    'orphan_count': 'Exceptions Generated'},
                                    title="MoM Zone wise Exception generation")
    return figure

def func_generate_zone_hub_bubble_fig(df, date_agg, xasisname):
    figure = px.scatter(df, 
                                        x=date_agg, 
                                        y="orphan_count", 
                                        color="hub_name", 
                                        facet_col='zone',
                                        size="orphan_count", size_max=50, 
                                        template= {'layout':{'paper_bgcolor':'#ffffe6', 'plot_bgcolor':'#aebfd0', 'showlegend':False,
                                                            'xaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1, 'fixedrange':True},
                                                            'yaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1, 'fixedrange':True},
                                                                }},
                 title="Zone-Hub wise MoM Exceptions",
                 labels={'scanned_date' if xasisname=='Scanned Date' else ('weeknum' if xasisname=='Week' else 'month_year'):xasisname,
                        "orphan_count":"Exceptions Generated",
                        "hub_name":'Hubs'} # customize label,
                
                            )
    return figure

def func_exception_type_fig(df, date_agg, tickformat, xasisname):
    # print(df[df.exception_type=='Non-reconciled Orphans'])
    # df = df[df.exception_type=='Non-reconciled Orphans']
    figure = go.Figure({
                    'data':[go.Scatter(x=df[df.exception_type==exception_typ][date_agg].unique(),
                                        y=df[df.exception_type==exception_typ].orphan_count,
                                        line = dict(width=1.5),
                                        marker=dict(size=3.5),
                                        name = exception_typ,
                                        text = exception_typ,
                                        line_color=rc_color,
                                        # xperiod='M1',
                                        mode='markers+lines') for exception_typ, rc_color in zip(df.exception_type.unique(), color_code)],
                    'layout':{'title':'Exception Type Trend',
                    # 'plot_bgcolor':'#24A3B5',
                            'yaxis':{'title':'Exceptions Generated'},
                            'paper_bgcolor':'#33475b',
                            'plot_bgcolor':'#aebfd0',
                            'font':dict(
                                            family="sans serif",
                                            size=12,
                                            color="white"
                                        ),
                            'legend':dict(
                                    yanchor="top",
                                    y=0.99,
                                    xanchor="left",
                                    x=0.01,
                                    font=dict(size=10)
                                ),
                                
                            'xaxis' : dict(
                                        tickformat = tickformat, # hide dates with no values
                                        # title='Months',
                                        title = xasisname,
                                        tickmode = 'array',
                                        # ticklabelmode="period", dtick="M1",
                                        # showgrid=False,
                                        nticks =7,
                                        ticktext = df[date_agg].unique(),
                                        tickvals = df[date_agg].unique(),
                                        # tick0 = 1.0,
                                        tickangle = 35),
                            'margin':go.layout.Margin(
                                        l=0, #left margin
                                        r=10, #right margin
                                        b=0, #bottom margin
                                        t=50, #top margin
                                    )
                        }
                                        
                    })
    return figure