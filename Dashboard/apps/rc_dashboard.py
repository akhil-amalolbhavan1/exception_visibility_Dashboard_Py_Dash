# import dash
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
import plotly.graph_objs as go
import dash_table
import plotly.express as px
from datetime import datetime as dt,timedelta
import os
from dashboard import app


rcdf = pd.read_csv(os.getcwd() +'/Dashboard/data/rc_full_data.csv')
# print(rcdf.columns)
rcdf['scanned_date'] = pd.to_datetime(rcdf['scanned_date'])
# app= dash.Dash(__name__, meta_tags=[])
color_code = ['crimson','darkgreen','darkorange','blue','red', 'maroon', 'teal', 'darkblue', 'magenta','yellow','lightgreen']

# image_filename = 'flipkart-logo.png' # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())
overall_pivot = pd.DataFrame(pd.pivot_table(rcdf, index=['scanned_date'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
rc_pivot = pd.DataFrame(pd.pivot_table(rcdf, index=['scanned_date','rc_name'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
destination_pivot = pd.DataFrame(pd.pivot_table(rcdf, index=['final_area_rc'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
damaged_non_damaged = pd.DataFrame(pd.pivot_table(rcdf, index=['packaging_condition'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
damaged_business_unit = pd.DataFrame(pd.pivot_table(rcdf[rcdf.packaging_condition=='Product Damaged'], index=['business_unit'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
non_damaged_business_unit = pd.DataFrame(pd.pivot_table(rcdf[rcdf.packaging_condition=='Non-Damaged'], index=['business_unit'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
# non_damaged_business_unit
dd_rc_name = rc_pivot.rc_name.unique().tolist()
dd_rc_name.append('All')
# print(rc_pivot)
def get_layout(df):
    global rcdf
    rcdf = df
    rcdf['scanned_date'] = pd.to_datetime(rcdf['scanned_date'])
    layout = html.Div([
                
                html.H1('RC Dashboard', style={'textAlign':'center', 'width':'100%', 'display':'inline-block'}),
                    # html.Div([
                    #         html.Label(['Select Date Range'])
                    #     ]),
                html.Div([dcc.Interval(
                                    id='interval_component',
                                    interval=1000, # in milliseconds
                                    n_intervals=0
                                ),
                            dcc.Graph(id = 'orphan_scanned_trend_graph',
                                        figure = go.Figure({
                                                'data':[go.Scatter(x=overall_pivot['scanned_date'].unique(),
                                                                    y=overall_pivot.pivot_table(index='scanned_date',values='orphan_count',aggfunc=sum).reset_index().orphan_count,
                                                                    line = dict(color='firebrick', width=2),
                                                                    mode='markers+lines')],
                                                'layout':{'title':'Overall Orphan Receiving Trend',
                                                            # 'xaxis':{'title':'Business Units'},
                                                            'yaxis':{'title':'Orphans Recieved'},
                                                            'paper_bgcolor':'#ffffe6',
                                                            'plot_bgcolor':'#aebfd0',
                                                            'font':dict(
                                                                family="sans serif",
                                                                size=14,
                                                                color="black"
                                                            ),        
                                                            'xaxis' : dict(
                                                                    # tickformat = '%Y-%b-%d',
                                                                    title='Scanned Date',
                                                                    tickmode = 'array',
                                                                    nticks =7,
                                                                    ticktext = overall_pivot['scanned_date'].unique(),
                                                                    #tickvals = df[date_agg_val].unique(),
                                                                    # tick0 = 1.0,
                                                                    tickangle = 35)}
                                                }),
                                        style={'width':'100%', 'display':'inline-block'}),
                          
                            dcc.Graph(id = 'rc_scanned_bar_graph',
                                        figure = go.Figure({
                                                'data':[go.Scatter(x=rc_pivot[rc_pivot.rc_name==rc]['scanned_date'],
                                                                    y=rc_pivot[rc_pivot.rc_name==rc].orphan_count,
                                                                    line = dict(color='firebrick', width=2),
                                                                    name = rc,
                                                                    text = rc,
                                                                    line_color=rc_color,
                                                                    mode='markers+lines') for rc, rc_color in zip(rc_pivot.rc_name.unique(), color_code)],
                                                'layout':{'title':'RC wise Orphan Receiving Trend',
                                                            # 'xaxis':{'title':'Business Units'},
                                                            'yaxis':{'title':'Orphans Recieved'},
                                                            'paper_bgcolor':'#ffffe6',
                                                            'plot_bgcolor':'#aebfd0',
                                                            'font':dict(
                                                                family="sans serif",
                                                                size=14,
                                                                color="black"
                                                            ),
                                                        'xaxis' : dict(
                                                                    # tickformat = '%Y-%b-%d',
                                                                    title='Scanned Date',
                                                                    tickmode = 'array',
                                                                    nticks =7,
                                                                    ticktext = overall_pivot['scanned_date'].unique(),
                                                                    #tickvals = df[date_agg_val].unique(),
                                                                    # tick0 = 1.0,
                                                                    tickangle = 35)}
                                                }),
                                        style={'width':'100%', 'display':'inline-block'}),
                        html.Div([
                            html.Div([
                                html.Label(['RC Name'], style={'color':'white','width':'30%'}),
                                    dcc.Dropdown(id='dd_rcname',
                                            options = [{'label':name, 'value':name} for name in dd_rc_name],
                                            value = 'All', multi=False #multi=True,clearable=False,
                                            )],style={'width':'30%','align':'center', 'margin': '0 auto'}),
                                html.Div([], style={'height':'10px'}),
                                html.Div([
                                        html.Div([], style={'display':'inline-block', 'width':'3%'}),

                                        dcc.Graph(id = 'destination_bar_graph',
                                            figure = go.Figure(),
                                                style={'width':'45%', 'display':'inline-block', 'border-style':'solid', 'border-color':'#405972'}),
                                            
                                            html.Div([], style={'display':'inline-block', 'width':'2%'}),

                                            dcc.Graph(id = 'damaged_non_damaged_bar_graph',
                                                figure = go.Figure(),
                                                style={'width':'45%', 'display':'inline-block', 'border-style':'solid', 'border-color':'#405972'}),
                                        ]),
                                        html.Div([
                                                html.Div([], style={'display':'inline-block', 'width':'3%'}),

                                                dcc.Graph(id = 'damaged_BU_bar_id',
                                                # figure = go.Figure(),
                                                figure=go.Figure({
                                                            'data':[go.Bar(x = damaged_business_unit.business_unit,
                                                                            y= damaged_business_unit.orphan_count,
                                                                            # destination_pivot.return_id/df.return_id.sum()*100,
                                                                            # text= destination_pivot.final_area_rc.apply(lambda x:"{:,}".format(x)),
                                                                            # marker_color=['green','rgb(255,69,0)']
                                                                            marker_color=color_code
                                                                            )],
                                                            'layout':go.Layout({'title':'Damaged Business Unit Split'})
                                                            }), 
                                                            style={'width':'45%', 'display':'inline-block','border-style':'solid', 'border-color':'#405972'}),
                                                html.Div([], style={'display':'inline-block', 'width':'2%'}),
                                                
                                                dcc.Graph(id = 'non_damaged_BU_bar_id',
                                                figure = go.Figure(),
                                                            style={'width':'45%', 'display':'inline-block', 'border-style':'solid', 'border-color':'#405972'})
                                                ], style={'margin': '0 auto', 'align':'center'}),
                                        html.Div([
                                            html.Div([], style={'display':'inline-block', 'width':'3%'}),
                                                dcc.Graph(id = 'fsn_identified_not_trend',
                                                # figure = go.Figure(),
                                                figure=go.Figure(), 
                                                            style={'width':'45%', 'display':'inline-block', 'border-style':'solid', 'border-color':'#405972'}),
                                                html.Div([], style={'display':'inline-block', 'width':'2%'}),
                                                dcc.Graph(id = 'orphan_condition_trend',
                                                figure = go.Figure(),
                                                            style={'width':'45%', 'display':'inline-block', 'border-style':'solid', 'border-color':'#405972'})
                                                ], style={'float':'none'})
                            ], style={'background-color':'#33475b'})
                    ])
    ])
    return layout
@app.callback(
    Output('destination_bar_graph', 'figure'),
    Output('damaged_non_damaged_bar_graph', 'figure'),
    Output('damaged_BU_bar_id', 'figure'),
    Output('non_damaged_BU_bar_id', 'figure'),
    Output('fsn_identified_not_trend','figure'),
    Output('orphan_condition_trend','figure'),
    Input('dd_rcname','value')
    )
def reload_graphs(dd_rc_name_value):
    # print(dd_rc_name_value)
    if dd_rc_name_value=='All':
        destination_pivot, damaged_non_damaged, damaged_business_unit, non_damaged_business_unit, fsn_ident_non, orphan_condition = load_datasets(rcdf)
    else:
        destination_pivot, damaged_non_damaged, damaged_business_unit, non_damaged_business_unit, fsn_ident_non, orphan_condition = load_datasets(rcdf[rcdf.rc_name==dd_rc_name_value])
    # print(destination_pivot)
    # print(destination_pivot.empty)
    if destination_pivot.empty:
        dest_figure = fun_ret_dest_trend(pd.DataFrame(columns=['final_area_rc','orphan_count']))
    else:
        dest_figure = fun_ret_dest_trend(destination_pivot)
    
    if damaged_non_damaged.empty:
        dam_nondam_fig = fun_ret_dam_nondam_bar(pd.DataFrame(columns=['packaging_condition','orphan_count']))
    else:
        dam_nondam_fig = fun_ret_dam_nondam_bar(damaged_non_damaged)

    if damaged_business_unit.empty:
        dam_bu_fig = fun_ret_dam_bu_bar(pd.DataFrame(columns=['business_unit','orphan_count']))
    else:
        dam_bu_fig = fun_ret_dam_bu_bar(damaged_business_unit)
    
    if non_damaged_business_unit.empty:
        nondam_bu_fig = fun_ret_nondam_bu(pd.DataFrame(columns=['business_unit','orphan_count']))
    else:
        nondam_bu_fig = fun_ret_nondam_bu(non_damaged_business_unit)
    
    if fsn_ident_non.empty:
        fsn_idnet_not_fig = fun_fsn_idnet_not(pd.DataFrame(columns=['fsn_identified_warehouse','orphan_count']))
    else:
        fsn_idnet_not_fig = fun_fsn_idnet_not(fsn_ident_non)

    if orphan_condition.empty:
        orphan_condition_fig = fun_orphan_condition(pd.DataFrame(columns=['orphan_id_condition','orphan_count']))
    else:
        orphan_condition_fig = fun_orphan_condition(orphan_condition)
    
    return dest_figure, dam_nondam_fig, dam_bu_fig, nondam_bu_fig, fsn_idnet_not_fig, orphan_condition_fig

# @app.callback(Output('',''),
#     Input('interval_component','interval'))
# def update_df():
#     global rcdf, overall_pivot, rc_pivot, destination_pivot, damaged_non_damaged, damaged_business_unit, non_damaged_business_unit, dd_rc_name

#     rcdf = pd.read_csv(os.getcwd() +'/Dashboard/data/rc_full_data.csv')
#     # print(rcdf.columns)
#     rcdf['scanned_date'] = pd.to_datetime(rcdf['scanned_date'])
#     # app= dash.Dash(__name__, meta_tags=[])
#     # color_code = ['crimson','darkgreen','darkorange','blue','red', 'maroon', 'teal', 'darkblue', 'magenta','yellow','lightgreen']

#     # image_filename = 'flipkart-logo.png' # replace with your own image
#     # encoded_image = base64.b64encode(open(image_filename, 'rb').read())
#     overall_pivot = pd.DataFrame(pd.pivot_table(rcdf, index=['scanned_date'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
#     rc_pivot = pd.DataFrame(pd.pivot_table(rcdf, index=['scanned_date','rc_name'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
#     destination_pivot = pd.DataFrame(pd.pivot_table(rcdf, index=['final_area_rc'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
#     damaged_non_damaged = pd.DataFrame(pd.pivot_table(rcdf, index=['packaging_condition'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
#     damaged_business_unit = pd.DataFrame(pd.pivot_table(rcdf[rcdf.packaging_condition=='Product Damaged'], index=['business_unit'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
#     non_damaged_business_unit = pd.DataFrame(pd.pivot_table(rcdf[rcdf.packaging_condition=='Non-Damaged'], index=['business_unit'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
#     # non_damaged_business_unit
#     dd_rc_name = rc_pivot.rc_name.unique().tolist()
#     dd_rc_name.append('All')

    # return 

def func_return_bar_graph(df):
    #print(df)
    figure = go.Figure({
                     'data':[go.Bar(x = df.supply_type,
                                     y=df.return_id/df.return_id.sum()*100,
                                     text= df.return_id.apply(lambda x:"{:,}".format(x)),
                                     marker_color=['maroon','rgb(70,130,180)'])],
                     'layout':go.Layout({'title':'Total Returns'})
                     })
    return figure

def load_datasets(df):
    # overall_pivot = pd.DataFrame(pd.pivot_table(df, index=['scanned_date'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
    # rc_pivot = pd.DataFrame(pd.pivot_table(df, index=['scanned_date','rc_name'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
    destination_pivot = pd.DataFrame(pd.pivot_table(df, index=['final_area_rc'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
    # print(destination_pivot)
    damaged_non_damaged = pd.DataFrame(pd.pivot_table(df, index=['packaging_condition'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
    damaged_business_unit = pd.DataFrame(pd.pivot_table(df[df.packaging_condition=='Product Damaged'], index=['business_unit'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
    non_damaged_business_unit = pd.DataFrame(pd.pivot_table(df[df.packaging_condition=='Non-Damaged'], index=['business_unit'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
    fsn_ident_non = pd.DataFrame(pd.pivot_table(df, index=['scanned_date','fsn_identified_warehouse'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})
    orphan_id_condition = pd.DataFrame(pd.pivot_table(df, index=['scanned_date','orphan_id_condition'], values=['rc_received_timestamp'], aggfunc=len)).reset_index().rename(columns={'rc_received_timestamp': 'orphan_count'})

    return destination_pivot, damaged_non_damaged, damaged_business_unit, non_damaged_business_unit, fsn_ident_non, orphan_id_condition

def fun_ret_dest_trend(df):
    figure=go.Figure({
                    'data':[go.Bar(x = df.final_area_rc.unique(),
                                    # y= pd.DataFrame(pd.pivot_table(df, index=['final_area_rc'], values=['orphan_count'], aggfunc=sum)).reset_index()['orphan_count'],
                                    y=df.orphan_count,
                                    # destination_pivot.return_id/df.return_id.sum()*100,
                                    # text= destination_pivot.final_area_rc.apply(lambda x:"{:,}".format(x)),
                                    marker_color=color_code
                                    )],
                    'layout':go.Layout({'title':'RC Destination Area Split',
                                        'xaxis':{'title':'Destination Areas'},
                                        'yaxis':{'title':'Orphans Received'},
                                        'paper_bgcolor':'#33475b',
                                        'plot_bgcolor':'#aebfd0',
                                        'font':dict(
                                                    family="sans serif",
                                                    size=12,
                                                    color="white"
                                                ),
                                        'margin':go.layout.Margin(
                                                l=0, #left margin
                                                r=10, #right margin
                                                b=0, #bottom margin
                                                t=50, #top margin
                                            )
                        })
                })
    return figure

def fun_ret_dam_nondam_bar(df):
    figure=go.Figure({
                    'data':[go.Bar(x = df.packaging_condition.unique(),
                                    y= df.orphan_count,
                                    # destination_pivot.return_id/df.return_id.sum()*100,
                                    # text= destination_pivot.final_area_rc.apply(lambda x:"{:,}".format(x)),
                                    # marker_color=['green','rgb(255,69,0)']
                                    marker_color=color_code
                                    )],
                    'layout':go.Layout({'title':'RC packaging damage receiving split',
                                        # 'xaxis':{'title':'Package Condition'},
                                        'xaxis':dict(tickangle = 35,
                                                title='Package Condition'),
                                        'yaxis':{'title':'Orphans Received'},
                                        'paper_bgcolor':'#33475b',
                                        'plot_bgcolor':'#aebfd0',
                                        
                                        'font':dict(
                                                    family="sans serif",
                                                    size=12,
                                                    color="white"
                                                ),
                                        'margin':go.layout.Margin(
                                                l=0, #left margin
                                                r=10, #right margin
                                                b=0, #bottom margin
                                                t=50, #top margin
                                            )
                        })
                })
    return figure

def fun_ret_dam_bu_bar(df):
    figure=go.Figure({
                    'data':[go.Bar(x = df.business_unit,
                                    y= df.orphan_count,
                                    # destination_pivot.return_id/df.return_id.sum()*100,
                                    # text= destination_pivot.final_area_rc.apply(lambda x:"{:,}".format(x)),
                                    # marker_color=['green','rgb(255,69,0)']
                                    marker_color=color_code
                                    )],
                    'layout':go.Layout({'title':'Damaged Business Unit Split',
                                        'xaxis':{'title':'Business Units'},
                                        'xaxis':{'title':'Business Units',
                                        # 'showline':True, 'linewidth':1, 'linecolor':'black', 'mirror':True
                                        },
                                        'yaxis':{'title':'Orphans Recieved'},
                                        'paper_bgcolor':'#33475b',
                                        'plot_bgcolor':'#aebfd0',
                                        'height':400,
                                        # 'showline':True, 'linewidth':1, 'linecolor':'black', 'mirror':True,
                                        'font':dict(
                                                family="sans serif",
                                                size=12,
                                                color="white"
                                                ),
                                        'margin':go.layout.Margin(
                                                l=0, #left margin
                                                r=10, #right margin
                                                b=0, #bottom margin
                                                t=50, #top margin
                                            )
                                        })
                    })
    return figure

def fun_ret_nondam_bu(df):
    figure=go.Figure({
                    'data':[go.Bar(x = df.business_unit,
                                    y= df.orphan_count,
                                    # destination_pivot.return_id/df.return_id.sum()*100,
                                    # text= destination_pivot.final_area_rc.apply(lambda x:"{:,}".format(x)),
                                    # marker_color=['green','rgb(255,69,0)']
                                    marker_color=color_code
                                    )],
                    'layout':go.Layout({'title':'Non Damaged Business Unit Split',
                                        'xaxis':{'title':'Business Units'},
                                        'yaxis':{'title':'Orphans Recieved'},
                                        'paper_bgcolor':'#33475b',
                                        'plot_bgcolor':'#aebfd0',
                                        'height':400,
                                        'font':dict(
                                            family="sans serif",
                                            size=12,
                                            color="white"
                                        ),
                                    'margin':go.layout.Margin(
                                        l=0, #left margin
                                        r=10, #right margin
                                        b=0, #bottom margin
                                        t=50, #top margin
                                    )
                                        })
                    })
    return figure

def fun_fsn_idnet_not(df):
    figure = go.Figure({
                    'data':[go.Scatter(x=df[df.fsn_identified_warehouse==fsn_ident]['scanned_date'],
                                        y=df[df.fsn_identified_warehouse==fsn_ident].orphan_count,
                                        line = dict(width=1.5),
                                        marker=dict(size=3.5),
                                        name = fsn_ident,
                                        text = fsn_ident,
                                        line_color=rc_color,
                                        mode='markers+lines') for fsn_ident, rc_color in zip(df.fsn_identified_warehouse.unique(), color_code)],
                    'layout':{'title':'FSN Identified/Not Trend',
                    # 'plot_bgcolor':'#24A3B5',
                            # 'xaxis':{'title':'Business Units'},
                            'yaxis':{'title':'Orphans Recieved'},
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
                                        # tickformat = '%Y-%b-%d',
                                        title='Scanned Date',
                                        tickmode = 'array',
                                        nticks =7,
                                        ticktext = overall_pivot['scanned_date'].unique(),
                                        #tickvals = df[date_agg_val].unique(),
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

def fun_orphan_condition(df):
    figure = go.Figure({
                    'data':[go.Scatter(x=df[df.orphan_id_condition==fsn_ident]['scanned_date'],
                                        y=df[df.orphan_id_condition==fsn_ident].orphan_count,
                                        line = dict(width=1.5),
                                        marker=dict(size=3.5),
                                        name = fsn_ident,
                                        text = fsn_ident,
                                        line_color=rc_color,
                                        mode='markers+lines') for fsn_ident, rc_color in zip(df.orphan_id_condition.unique(), color_code)],
                    'layout':{'title':'Orphan ID Condition Trend',
                    # 'plot_bgcolor':'#24A3B5',
                            'yaxis':{'title':'Orphans Recieved'},
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
                                        title='Scanned Date',
                                        # tickformat = '%Y-%b-%d',
                                        tickmode = 'array',
                                        nticks =7,
                                        ticktext = overall_pivot['scanned_date'].unique(),
                                        #tickvals = df[date_agg_val].unique(),
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

def fun_orphan_scanned_trend(df):
    figure = go.Figure({
            'data':[go.Scatter(x=df['scanned_date'].unique(),
                                y=df.pivot_table(index='scanned_date',values='orphan_count',aggfunc=sum).reset_index().orphan_count,
                                line = dict(color='firebrick', width=2),
                                mode='markers+lines')],
            'layout':{'title':'Overall Orphan Receiving Trend',
                        # 'xaxis':{'title':'Business Units'},
                        'yaxis':{'title':'Orphans Recieved'},
                        'paper_bgcolor':'#ffffe6',
                        'plot_bgcolor':'#aebfd0',
                        'font':dict(
                            family="sans serif",
                            size=14,
                            color="black"
                        ),        
                        'xaxis' : dict(
                                # tickformat = '%Y-%b-%d',
                                title='Scanned Date',
                                tickmode = 'array',
                                nticks =7,
                                ticktext = df['scanned_date'].unique(),
                                #tickvals = df[date_agg_val].unique(),
                                # tick0 = 1.0,
                                tickangle = 35)}
            })
    return figure