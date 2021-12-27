from re import A

from googleapiclient.discovery import V1_DISCOVERY_URI


# Owner : Akhil A
# Version V1
# Created on :
from dash_html_components.Center import Center
from dash_html_components.Div import Div
from numpy.core.fromnumeric import trace
import pandas as pd
from pandas.io.formats import style
import plotly.express as px
import numpy as np
#import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
# from dash_extensions.enrich import ServersideOutput, Trigger
import plotly.graph_objs as go
import dash_table
import plotly.express as px
# from datetime import datetime
import os
import dash_bootstrap_components as dbc
# from datetime import datetime as dt,timedelta
# from plotly.graph_objs import bar
from dashboard import app
from datetime import datetime, timedelta


orphan_df = pd.read_csv(os.getcwd() +'/Dashboard/data/orphan_full_data.csv', low_memory=False)
rcdf = pd.read_csv(os.getcwd() +'/Dashboard/data/rc_full_data.csv', low_memory=False)
logistics_df = pd.read_csv(os.getcwd() +'/Dashboard/data/logistcs_orphan_full_data.csv', low_memory=False)
hvdf = pd.read_csv(os.getcwd() +'/Dashboard/data/hv_orphan_full_data.csv', low_memory=False)
datesdf = pd.read_csv(os.getcwd()+'/Dashboard/Data/week_details.csv')
datesdf.weekday = pd.to_datetime(datesdf.weekday)
color_code = ['crimson','darkgreen','darkorange','blue','red', 'maroon', 'teal', 'darkblue', 'magenta','yellow','lightgreen']
# mhdf['month_year'] = ['-'.join(i) for i in zip(mhdf["month"].map(str),mhdf["year"].map(str))]
orphan_df['month_yr'] = pd.to_datetime(orphan_df['scanned_date']).dt.month_name().str.slice(stop=3)+"-"+orphan_df["year"].map(str)


dd_date_agg_values = ['Day Wise','Week Wise', 'Month Wise']

cat_order = ['Jan-2021','Feb-2021','Mar-2021','Apr-2021','May-2021','Jun-2021','Jul-2021','Aug-2021','Sep-2021','Oct-2021','Nov-2021','Dec-2021','Jan-2022','Feb-2022','Mar-2022','Apr-2022','May-2022','Jun-2022',
            'Jul-2022','Aug-2022','Sep-2022','Oct-2022','Nov-2022','Dec-2022','Jan-2023','Feb-2023','Mar-2023','Apr-2023','May-2023','Jun-2023','Jul-2023','Aug-2023','Sep-2023','Oct-2023','Nov-2023','Dec-2023']
df_sorter = pd.DataFrame(data ={ 'month_yr': cat_order,
                                'priority':[1,	2,	3,	4,	5,	6,	7,	8,	9,	10,	11,	12,	13,	14,	15,	16,	17,	18,	19,	20,	21,	22,	23,	24,	25,	26,	27,	28,	29,	30,	31,	32,	33,	34,	35,	36]})


def get_layout(df, rc_df, logisticsdf, hv_df):
    global orphan_df, rcdf, logistics_df, hvdf
    rcdf = rc_df
    orphan_df = df
    hvdf = hv_df
    logistics_df = logisticsdf
    orphan_df['month_yr'] = pd.to_datetime(orphan_df['scanned_date']).dt.month_name().str.slice(stop=3)+"-"+orphan_df["year"].map(str)
    logistics_df['month_yr'] = pd.to_datetime(logistics_df['scanned_date']).dt.month_name().str.slice(stop=3)+"-"+logistics_df["year"].map(str)
    layout = html.Div([
                        html.H1('Orphan Dashboard', style={'textAlign':'center', 'width':'100%', 'display':'inline-block'}),
                        html.Br(),html.Br(),
                        html.Div([
                            html.Label(['Choose the date range'], style={'color':'black','width':'200px','textAlign':'left','float':'left','align':'center','display':'inline-block','line-height': '50px','vertical-align': 'middle'}),
                            dcc.DatePickerRange(
                                            id='dt_range_orphan',
                                            min_date_allowed=datesdf.weekday.min(),
                                            max_date_allowed=datetime.today(),
                                            initial_visible_month=datetime.today(),
                                            #style={'width':'30%','display':'block', 'padding':'0', 'max-height':'300px'},
                                            start_date= datetime.today()-timedelta(days=60),
                                            # end_date=datesdf.weekday.max()-timedelta(days=1)
                                            end_date = datetime.today(),
                                            style={'width':'300px','float':'left'}
                                        ),
                                    html.Label(['Choose the x axis for date'], style={'color':'black','width':'200px','textAlign':'left','float':'left','line-height': '50px','vertical-align': 'middle'}),
                                                dcc.Dropdown(id='dd_date_agg_orphan',
                                                        options = [{'label':name, 'value':name} for name in dd_date_agg_values],
                                                        value = 'Week Wise', multi=False, #multi=True,clearable=False,
                                                        style={'float':'left','width':'200px', 'line-height': '50px','vertical-align': 'middle'}
                                                )
                                         ],  style={'align':'center'}),
                        html.Br(),html.Br(),html.Br(),html.Br(),
                        html.Div([ html.H4(['Overall Orphan Generation']),
                                    dash_table.DataTable(
                                                        id='overall_orphan_generated_table',
                                                        columns = [],
                                                        data = [],
                                                        # filter_action = 'native',
                                                        sort_action ='native',
                                                        # export_format = 'csv',
                                                        # export_columns='visible',
                                                        export_headers = 'names',
                                                        # columns=[{"name": i, "id": i} for i in q2_dc_cross_tab.columns],
                                                        # data=q2_dc_cross_tab.to_dict('records'),
                                                        page_size=20,
                                                        style_data_conditional=[
                                                                                {
                                                                                    'if': {'row_index': 'odd'},
                                                                                    'backgroundColor': '#e3e6e8',
                                                                                    'color':'black'
                                                                                },
                                                                                {
                                                                                    'if': {'row_index': 'even'},
                                                                                    'backgroundColor': '#d9d9d9',
                                                                                    'color':'black'
                                                                                }
                                                                            ],
                                                        style_header={
                                                                        'backgroundColor': '#034f84',
                                                                        # 'fontWeight': 'bold',
                                                                        'color':'white'
                                                                    },
                                                        style_data={ 'border-color': '#034f84' }
                                                        )]),
                                                        dcc.Graph(id='ageing_rc_bar',
                                            figure = go.Figure(), style={'width':'100%', 'float': 'left'}),
                                        html.Div([
                                            dcc.Graph(id='ageing_mh_zone_bar',
                                            figure = go.Figure(), style={'width':'100%', 'float': 'left'}),
                                        ]),html.Div(),
                                        html.Div(
                                            [
                                                html.Button("Download Ageing Data", className="btn btn-info", id="btn_csv"),
                                                dcc.Download(id="download-dataframe-csv"),
                                            ]
                                        ),
                                                        html.Br(),html.Br(),
                        html.H3(['MH Specific Metrics']),
                        html.Div([
                            
                            html.Div([
                                html.Br(),html.Br(),
                                
                                html.H5(['Orphans Generated'], style={'color':'#707B7C','width':'100%','textAlign':'center'}),
                                html.Div(id='total_orphans',children=[])
                                ], style={'height':'150px', 'width':'150px', 
                                            'backgroundColor':'#F4D03F', 'color':'#707B7C', 
                                            'border': '3px solid #9A7D0A','verticalAlign': 'middle',
                                            'borderRadius': '5px', 'float':'left'}),
                                html.Div([], style={'width':'50px', 'float':'left', 'margin':'10px'}),
                                html.Div([
                                html.Br(),
                                html.H5(['Shipment Converted'], style={'color':'#707B7C','width':'100%','textAlign':'center'}),
                                html.Div(id='conversion_block',children=[])
                            ], style={'height':'150px', 'width':'150px', 
                                        'backgroundColor':'#F4D03F', 'color':'#707B7C', 
                                        'border': '3px solid #9A7D0A','verticalAlign': 'middle',
                                        'borderRadius': '5px', 'float':'left'}),
                                html.Div([], style={'width':'50px', 'float':'left', 'margin':'10px'}),
                                html.Div([
                                html.Br(),html.Br(),
                                html.H5(['Missing Orphan Ids'], style={'color':'#707B7C','width':'100%','textAlign':'center'}),
                                html.Div(id='missing_orphan_ids',children=[])
                            ], style={'height':'150px', 'width':'150px', 
                                        'backgroundColor':'#F4D03F', 'color':'#707B7C', 
                                        'border': '3px solid #9A7D0A','verticalAlign': 'middle',
                                        'borderRadius': '5px', 'float':'left'}),
                                html.Div([], style={'width':'50px', 'float':'left', 'margin':'10px'}),
                            #     html.Div([
                            #     html.Br(),
                            #     html.H5(['Orphan Value Identified'], style={'color':'#707B7C','width':'100%','textAlign':'center'}),
                            #     html.Div(id='orphan_valuation',children=[])
                            # ], style={'height':'150px', 'width':'150px', 
                            #             'backgroundColor':'#F4D03F', 'color':'#707B7C', 
                            #             'border': '3px solid #9A7D0A','verticalAlign': 'middle',
                            #             'borderRadius': '5px', 'float':'left'})
                                ], style={'align':'center','display':'flex', 'justify-content': 'center'}),
                            html.Div([], style={'float':'none'}),
                        html.Br(),
                        html.Br(),
                        dbc.Tabs(
                            [
                                dbc.Tab(
                                html.Div([
                                    html.Br(),
                                    # html.Div([
                                    #         dcc.Graph(id='overall_trend_orphan_count',
                                    #         figure = go.Figure(), style={'width':'50%', 'float': 'left'}),

                                    #         dcc.Graph(id='overall_trend_orphan_value',
                                    #         figure = go.Figure(), style={'width':'50%', 'float': 'left'}),
                                            
                                    #         # dcc.Graph(id='converted_perc_bar',
                                    #         # figure=go.Figure())
                                    #         ], style={'width':'100%'}),
                                    html.Div([
                                            dcc.Graph(id='converted_perc_bar',
                                            figure = go.Figure(), style={'width':'50%', 'float': 'left'})
                                            # dcc.Graph(id='ageing_bar',
                                            # figure = go.Figure(), style={'width':'50%', 'float': 'left'}),
                                        ]),
                                        
                                        html.Div([
                                            dcc.Graph(id = 'shipment_type_bar',
                                            figure = go.Figure(),
                                                            style={'width':'100%', 'display':'inline-block'}
                                                            )
                                    ], style={'oveflow':'hidden'}),
                                    html.Div([
                                        dcc.Graph(id = 'orphan_reason_trend',
                                        figure = go.Figure(),
                                        style={'width':'100%', 'display':'inline-block'}),
                                    ]),
                                    html.Div([
                                        # dcc.Graph(id = 'orphan_area_trend',
                                        # figure = go.Figure(),
                                        # style={'width':'100%', 'display':'inline-block'}),
                                        html.Div([ html.H4(['Orphan Generation in respective Areas']),
                                    dash_table.DataTable(
                                                        id='orphan_area_trend_table',
                                                        columns = [],
                                                        data = [],
                                                        # filter_action = 'native',
                                                        sort_action ='native',
                                                        # export_format = 'csv',
                                                        # export_columns='visible',
                                                        export_headers = 'names',
                                                        # columns=[{"name": i, "id": i} for i in q2_dc_cross_tab.columns],
                                                        # data=q2_dc_cross_tab.to_dict('records'),
                                                        page_size=20,
                                                        style_data_conditional=[
                                                                                {
                                                                                    'if': {'row_index': 'odd'},
                                                                                    'backgroundColor': '#e3e6e8',
                                                                                    'color':'black'
                                                                                },
                                                                                {
                                                                                    'if': {'row_index': 'even'},
                                                                                    'backgroundColor': '#d9d9d9',
                                                                                    'color':'black'
                                                                                }
                                                                            ],
                                                        style_header={
                                                                        'backgroundColor': '#034f84',
                                                                        # 'fontWeight': 'bold',
                                                                        'color':'white'
                                                                    },
                                                        style_data={ 'border-color': '#034f84' }
                                                        )])
                                    ])
                                ])
                            
                                              
                                            , label='Normal Orphans'),
                                dbc.Tab([
                                    html.Div([
                                    html.Br(),
                                    html.Div([
                                            dcc.Graph(id='hv_converted_perc_bar',
                                            figure = go.Figure(), style={'width':'50%', 'float': 'left'})

                                        ]),
                                        
                                        html.Div([
                                            dcc.Graph(id = 'hv_shipment_type_bar',
                                            figure = go.Figure(),
                                                            style={'width':'100%', 'display':'inline-block'}
                                                            )
                                    ], style={'oveflow':'hidden'}),
                                    html.Div([
                                        dcc.Graph(id = 'hv_orphan_reason_trend',
                                        figure = go.Figure(),
                                        style={'width':'100%', 'display':'inline-block'}),
                                    ]),
                                    html.Div([
                                        html.Div([ html.H4(['Orphan Generation in respective Areas']),
                                    dash_table.DataTable(
                                                        id='hv_orphan_area_trend_table',
                                                        columns = [],
                                                        data = [],
                                                        # filter_action = 'native',
                                                        sort_action ='native',
                                                        # export_format = 'csv',
                                                        # export_columns='visible',
                                                        export_headers = 'names',
                                                        # columns=[{"name": i, "id": i} for i in q2_dc_cross_tab.columns],
                                                        # data=q2_dc_cross_tab.to_dict('records'),
                                                        page_size=20,
                                                        style_data_conditional=[
                                                                                {
                                                                                    'if': {'row_index': 'odd'},
                                                                                    'backgroundColor': '#e3e6e8',
                                                                                    'color':'black'
                                                                                },
                                                                                {
                                                                                    'if': {'row_index': 'even'},
                                                                                    'backgroundColor': '#d9d9d9',
                                                                                    'color':'black'
                                                                                }
                                                                            ],
                                                        style_header={
                                                                        'backgroundColor': '#034f84',
                                                                        # 'fontWeight': 'bold',
                                                                        'color':'white'
                                                                    },
                                                        style_data={ 'border-color': '#034f84' }
                                                        )])
                                    ])
                                ])
                            
                                ], label='High Value Orphans')
                            ], style={'width':'100%'}
                        )
                    ], style={'width':'100%', 'margin':'0', 'padding':'-5em'})
    return layout

@app.callback([
                Output('overall_orphan_generated_table','data'),
                Output('overall_orphan_generated_table','columns'),
                # Output('overall_trend_orphan_count','figure'),
                # Output('overall_trend_orphan_value','figure'),
                Output('converted_perc_bar','figure'),
                # Output('ageing_bar','figure'),
                Output('total_orphans','children'),
                Output('ageing_rc_bar','figure'),
                Output('conversion_block', 'children'),
                Output('missing_orphan_ids','children'),
                # Output('orphan_valuation','children'),
                Output('shipment_type_bar','figure'),
                Output('orphan_reason_trend','figure'),
                # Output('orphan_area_trend','figure'),
                # Output('ageing_mh_zone_bar','figure'),
                Output('orphan_area_trend_table','data'),
                Output('orphan_area_trend_table','columns'),
                Output('hv_converted_perc_bar','figure'),
                Output('hv_shipment_type_bar','figure'),
                Output('hv_orphan_reason_trend','figure'),
                Output('hv_orphan_area_trend_table','data'),
                Output('hv_orphan_area_trend_table','columns'),
                ],
                [Input('dt_range_orphan','start_date'),
                Input('dt_range_orphan','end_date'),
                Input('dd_date_agg_orphan','value')])
def update_figures(orphan_start_date, orphan_end_date, date_agg_val):
    column_name = ''
    tickformat = ''
    xaxis_name =''

    if date_agg_val=='Day Wise':
        tickformat = '%Y-%b-%d'
        xaxis_name = 'Scanned Date'
        column_name = 'scanned_date'
    elif date_agg_val == 'Week Wise':
        column_name = 'weeknum'
        xaxis_name = 'Week'
    else:
        column_name = 'month_yr'
        tickformat = '%Y-%b'
        xaxis_name = 'Months'
    
    orphan_df_temp = orphan_df[(orphan_df.scanned_date >=orphan_start_date)&(orphan_df.scanned_date<=orphan_end_date)].copy()
    logistics_df_temp = logistics_df[(logistics_df.scanned_date >=orphan_start_date)&(logistics_df.scanned_date<=orphan_end_date)].copy()
    hv_df_temp = hvdf[(hvdf.scanned_date >=orphan_start_date)&(hvdf.scanned_date<=orphan_end_date)].copy()
    orphan_df_temp = orphan_df_temp[~orphan_df_temp.shipment_category.isin(['Prone to Orphan'])]
    overall_pivot_count, overall_pivot_value, converted_pivot, shipment_type_pivot, orphan_reason_pivot, hv_converted_pivot, hv_shipment_type_pivot, hv_orphan_reason_pivot = func_load_pivots(orphan_df_temp, hv_df_temp, column_name)
    
    orphan_df_temp['month_year'] = pd.to_datetime(orphan_df_temp.scanned_date).dt.strftime('%b') + '-' + pd.to_datetime(orphan_df_temp.scanned_date).dt.year.astype(str)
    logistics_df_temp['month_year'] = pd.to_datetime(logistics_df_temp.scanned_date).dt.strftime('%b') + '-' + pd.to_datetime(logistics_df_temp.scanned_date).dt.year.astype(str)
    hv_df_temp['month_year'] = pd.to_datetime(hv_df_temp.scanned_date).dt.strftime('%b') + '-' + pd.to_datetime(hv_df_temp.scanned_date).dt.year.astype(str)

    # overall_trend_count_fig = func_overall_trend_count_fig(overall_pivot_count, column_name, tickformat, xaxis_name)
    # overall_trend_value_fig = func_overall_trend_val_fig(overall_pivot_value, column_name, tickformat, xaxis_name)
    converted_perc_fig =  fun_converted_perc_bar_fig(converted_pivot, column_name, tickformat, xaxis_name)
    shipment_type_bar_fig = func_generate_shiptype_bar_figure(shipment_type_pivot, column_name, xaxis_name)
    orphan_reason_trend_fig = func_generate_orphan_reason_trend_fig(orphan_reason_pivot,column_name, xaxis_name)
    # orphan_area_trend_fig = func_generate_area_fig(orphan_area_pivot, column_name, xaxis_name)
    
    #############Ageing Pivots
    ageing_rc_pivot, ageing_zone_pivot = func_load_age_data(orphan_df_temp,rcdf, logistics_df_temp)
    
    # ageing_fig =  fun_ageing_bar_fig(ageing_pivot)
    ageing_rc_fig = fun_ageing_rc_bar_fig(ageing_rc_pivot)
    overall_orphan_generation_pivot, orphan_area_pivot, hv_orphan_area_pivot = data_table_pivots(orphan_df_temp, hv_df_temp, logistics_df_temp,column_name)
    overall_orphan_data, overall_orphan_column = func_generate_table(overall_orphan_generation_pivot)
    orphan_area_data, orphan_area_column = func_generate_table(orphan_area_pivot)


    hv_converted_perc_fig =  fun_converted_perc_bar_fig(hv_converted_pivot, column_name, tickformat, xaxis_name)
    hv_shipment_type_bar_fig = func_generate_shiptype_bar_figure(hv_shipment_type_pivot, column_name, xaxis_name)
    hv_orphan_reason_trend_fig = func_generate_orphan_reason_trend_fig(hv_orphan_reason_pivot,column_name, xaxis_name)
    hv_orphan_area_data, hv_orphan_area_column = func_generate_table(hv_orphan_area_pivot)
    # total_count = orphan_df.scanned_timestamp.count()
    overal_count_labl = html.H6(["{:,}".format(orphan_df_temp.scanned_timestamp.count())], style={'textAlign':'center','width':'100%', 'color':'#1F618D', 'fontSize': '2.5em'}),
    overal_rc_pend_count_labl = [html.H6(["{:,}".format(ageing_rc_pivot.orphan_count.sum())], style={'textAlign':'center','width':'100%', 'color':'#1F618D', 'fontSize': '2.5em'}),
                                html.P([str(round(ageing_rc_pivot.orphan_count.sum()/orphan_df_temp.scanned_timestamp.count()*100,2))+'%'], style={'textAlign':'center', 'color':'red'})]

    orphan_id_missing_labl = [html.H6(["{:,}".format(orphan_df_temp[(orphan_df_temp.orphan_id.isna())]['scanned_timestamp'].count())], style={'textAlign':'center','width':'100%', 'color':'#1F618D', 'fontSize': '2.5em'}),
                                html.P([str(round(orphan_df_temp[(orphan_df_temp.orphan_id.isna())]['scanned_timestamp'].count()/orphan_df_temp.scanned_timestamp.count()*100,2))+'%'], style={'textAlign':'center', 'color':'red'})]
    # orphan_val_labl = [html.H6(["{:,}".format(orphan_df_temp[orphan_df_temp.orphan_id.isna()]['shipment_value'].sum())], style={'textAlign':'center','width':'100%', 'color':'#1F618D', 'fontSize': '2em'}),
    #                             html.P(["{:,}".format(round(orphan_df_temp[~orphan_df_temp.shipment_value.isna()]['scanned_timestamp'].count(),2))], style={'textAlign':'center', 'color':'red'})]
    overall_conversion_count = [html.H6(["{:,}".format(orphan_df_temp[(orphan_df_temp.is_tracking_id_available=='Yes')&(orphan_df_temp.shipment_category=='Orphan (Non-damage)')].is_tracking_id_available.count())], style={'textAlign':'center','width':'100%', 'color':'#1F618D', 'fontSize': '2.5em'}),
                        html.P([str(round(orphan_df_temp[(orphan_df_temp.is_tracking_id_available=='Yes')&(orphan_df_temp.shipment_category=='Orphan (Non-damage)')].is_tracking_id_available.count()/orphan_df_temp[(orphan_df_temp.shipment_category=='Orphan (Non-damage)')].is_tracking_id_available.count()*100,2))+'%'], style={'textAlign':'center', 'color':'red'})]

    return [overall_orphan_data, overall_orphan_column, converted_perc_fig,  overal_count_labl, ageing_rc_fig, overall_conversion_count, orphan_id_missing_labl, shipment_type_bar_fig, orphan_reason_trend_fig, orphan_area_data, orphan_area_column, hv_converted_perc_fig, hv_shipment_type_bar_fig, hv_orphan_reason_trend_fig, hv_orphan_area_data, hv_orphan_area_column]
    # return [overall_trend_count_fig, overall_trend_value_fig, converted_perc_fig,  overal_count_labl, ageing_rc_fig,overal_rc_pend_count_labl, orphan_id_missing_labl, orphan_val_labl, shipment_type_bar_fig, orphan_reason_trend_fig, orphan_area_trend_fig]

@app.callback(Output('ageing_mh_zone_bar', 'figure'),
               [Input('ageing_rc_bar', 'clickData')],
              [State('ageing_rc_bar', 'figure'),
              State('dt_range_orphan','start_date'),
            State('dt_range_orphan','end_date'),])
def update_zone_ageing(click_data, fig, start_date, end_date):
    trace_name=''
    if (click_data is None)|(click_data == ''):
        trace_name='Orphan Data'
    else:
        curve_number = click_data['points'][0]['curveNumber']
        trace_name = fig['data'][curve_number]['name']
    df = pd.DataFrame()
    if trace_name=='Orphan Data':
        df = orphan_df[(orphan_df.scanned_date >=start_date)&(orphan_df.scanned_date<=end_date)].copy()
    elif trace_name=='Last Mile':
        df = logistics_df[(logistics_df.asset=='Last Mile')&(logistics_df.scanned_date >=start_date)&(logistics_df.scanned_date<=end_date)].copy()
    else:
        df = logistics_df[(logistics_df.asset=='First Mile')&(logistics_df.scanned_date >=start_date)&(logistics_df.scanned_date<=end_date)].copy()
    
    merged_df = pd.merge(df[~df.orphan_id.isna()], rcdf[~rcdf.orphan_id.isna()][['orphan_id']], left_on='orphan_id', right_on = 'orphan_id', how='left')
    merged_df['age']=0
    merged_df['age'] = (datetime.today().date() - pd.to_datetime(merged_df['scanned_date']).dt.date)/np.timedelta64(1, 'D')
    merged_df['ageing_category'] = merged_df['age'].apply(lambda x: '1-9 days' if x <= 9 else ('10-16 days' if ((x >9) & (x <= 16) ) else ('17-23') if ((x >16) & (x <= 23) ) else ('24-31' if ((x >23) & (x <= 31) ) else 'Older 31 days')))
    ageing_zone_pivot = pd.DataFrame(pd.pivot_table(merged_df[~merged_df.orphan_id.isna()], index=['ageing_category','zone'], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    ageing_zone_fig = fun_ageing_zone_bar_fig(ageing_zone_pivot, trace_name)
    return ageing_zone_fig

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    [State('ageing_rc_bar', 'figure'),
    State('dt_range_orphan','start_date'),
    State('dt_range_orphan','end_date'),
    State('ageing_rc_bar', 'clickData')],
    prevent_initial_call=True)
def func(click_data, nclicks, fig, start_date, end_date):
    trace_name=''
    if click_data is None:
        trace_name=='Orphan Data'
    else:
        curve_number = click_data['points'][0]['curveNumber']
        trace_name = fig['data'][curve_number]['name']
    
    if trace_name=='Orphan Data':
        df = orphan_df[(orphan_df.scanned_date >=start_date)&(orphan_df.scanned_date<=end_date)].copy()
    elif trace_name=='Last Mile':
        df = logistics_df[(logistics_df.asset=='Last Mile')&(logistics_df.scanned_date >=start_date)&(logistics_df.scanned_date<=end_date)].copy()
    else:
        df = logistics_df[(logistics_df.asset=='First Mile')&(logistics_df.scanned_date >=start_date)&(logistics_df.scanned_date<=end_date)].copy()

    merged_df = pd.merge(df[~df.orphan_id.isna()], rcdf[~rcdf.orphan_id.isna()][['orphan_id']], left_on='orphan_id', right_on = 'orphan_id', how='left')
    merged_df['age']=0
    merged_df['age'] = (datetime.today().date() - pd.to_datetime(merged_df['scanned_date']).dt.date)/np.timedelta64(1, 'D')
    merged_df['ageing_category'] = merged_df['age'].apply(lambda x: '1-9 days' if x <= 9 else ('10-16 days' if ((x >9) & (x <= 16) ) else ('17-23') if ((x >16) & (x <= 23) ) else ('24-31' if ((x >23) & (x <= 31) ) else 'Older 31 days')))
    return dcc.send_data_frame(merged_df.to_csv, "ageing_data.csv")

def func_load_pivots(df, hv_df, date_agg):
    # df['shipment_type']
    overall_pivot_count = pd.DataFrame(pd.pivot_table(df, index=[date_agg], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    overall_pivot_value = pd.DataFrame(pd.pivot_table(df, index=[date_agg],fill_value=0, values=['shipment_value'], aggfunc=sum)).reset_index().rename(columns={'shipment_value': 'orphan_count'})
    shipment_type_pivot = pd.DataFrame(pd.pivot_table(df, index=[date_agg,'shipment_type'],fill_value=0, values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    orphan_reason_pivot = pd.DataFrame(pd.pivot_table(df, index=[date_agg,'orphan_reason'],fill_value=0, values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    # orphan_area_pivot = pd.DataFrame(pd.pivot_table(df, index=[date_agg,'orphan_idnetified_mh_area'],fill_value=0, values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
  
    converted_pivot = pd.DataFrame(pd.pivot_table(df[(df.shipment_category=='Orphan (Non-damage)')], index=[date_agg,'is_tracking_id_available'], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    converted_total = pd.DataFrame(pd.pivot_table(df[(df.shipment_category=='Orphan (Non-damage)')], index=[date_agg], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_total'})
    converted_total = pd.merge(converted_pivot,converted_total[[date_agg,'orphan_total']], on=date_agg, how='left')
    converted_total['percentage'] = round(converted_total.orphan_count/converted_total.orphan_total*100,2)
    converted_total = converted_total[converted_total.is_tracking_id_available=='Yes']
    # ageing_pivot = pd.DataFrame(pd.pivot_table(df[df.is_tracking_id_available=='Yes'], index=['ageing_category'], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    hv_converted_pivot = pd.DataFrame(pd.pivot_table(hv_df[(hv_df.shipment_category=='Orphan (Non-damage)')], index=[date_agg,'is_tracking_id_available'], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    hv_converted_total = pd.DataFrame(pd.pivot_table(hv_df[(hv_df.shipment_category=='Orphan (Non-damage)')], index=[date_agg], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_total'})
    hv_converted_total = pd.merge(hv_converted_pivot,hv_converted_total[[date_agg,'orphan_total']], on=date_agg, how='left')
    hv_converted_total['percentage'] = round(hv_converted_total.orphan_count/hv_converted_total.orphan_total*100,2)
    hv_converted_total = hv_converted_total[hv_converted_total.is_tracking_id_available=='Yes']

    hv_shipment_type_pivot = pd.DataFrame(pd.pivot_table(hv_df, index=[date_agg,'shipment_type'],fill_value=0, values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    hv_orphan_reason_pivot = pd.DataFrame(pd.pivot_table(hv_df, index=[date_agg,'orphan_reason'],fill_value=0, values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})

    if date_agg=='month_yr':
        overall_pivot_count = pd.merge(overall_pivot_count, df_sorter, on='month_yr', how='left').sort_values(by='priority')
        overall_pivot_value = pd.merge(overall_pivot_value, df_sorter, on='month_yr', how='left').sort_values(by='priority')
        converted_total = pd.merge(converted_total, df_sorter, on='month_yr', how='left').sort_values(by='priority')
        hv_converted_total = pd.merge(converted_total, df_sorter, on='month_yr', how='left').sort_values(by='priority')
        shipment_type_pivot = pd.merge(shipment_type_pivot, df_sorter, on='month_yr', how='left').sort_values(by='priority')
        hv_shipment_type_pivot = pd.merge(shipment_type_pivot, df_sorter, on='month_yr', how='left').sort_values(by='priority')
        orphan_reason_pivot = pd.merge(orphan_reason_pivot, df_sorter, on='month_yr', how='left').sort_values(by='priority')
        hv_orphan_reason_pivot = pd.merge(orphan_reason_pivot, df_sorter, on='month_yr', how='left').sort_values(by='priority')
        # orphan_area_pivot = pd.merge(orphan_area_pivot, df_sorter, on='month_yr', how='left').sort_values(by='priority')

    return overall_pivot_count, overall_pivot_value, converted_total, shipment_type_pivot, orphan_reason_pivot, hv_converted_total, hv_shipment_type_pivot, hv_orphan_reason_pivot #orphan_area_pivot #, ageing_pivot

def data_table_pivots(orpdf, hvdf, logisticsdf, date_agg):
    orpdf['month_year'] = pd.to_datetime(orpdf.scanned_date).dt.strftime('%b') + '-' + pd.to_datetime(orpdf.scanned_date).dt.year.astype(str)
    logisticsdf['month_year'] = pd.to_datetime(logisticsdf.scanned_date).dt.strftime('%b') + '-' + pd.to_datetime(logisticsdf.scanned_date).dt.year.astype(str)
    hvdf['month_year'] = pd.to_datetime(hvdf.scanned_date).dt.strftime('%b') + '-' + pd.to_datetime(hvdf.scanned_date).dt.year.astype(str)

    month_year = ['Jan-2021','Feb-2021', 'Mar-2021','Apr-2021','May-2021','Jun-2021','Jul-2021','Aug-2021','Sep-2021','Oct-2021','Nov-2021','Dec-2021',
                    'Jan-2022','Feb-2022', 'Mar-2022','Apr-2022','May-2022','Jun-2022','Jul-2022','Aug-2022','Sep-2022','Oct-2022','Nov-2022','Dec-2022',
                    'Jan-2023','Feb-2023', 'Mar-2023','Apr-2023','May-2023','Jun-2023','Jul-2023','Aug-2023','Sep-2023','Oct-2023','Nov-2023','Dec-2023']

    if date_agg=='month_yr':
        date_agg='month_year'

    mh_identified_area_mapping = pd.DataFrame(columns=['orphan_generated_area', 'orphan_identified_area'], data=[['Inbound Processing','Inbound Staging'],['Inbound Processing','Inbound area'],['Outbound Processing','Outbound Staging'],['Outbound Processing','Outbound area'],['Primary Processing','Primary processing'],['Secondary Processing','Secondary processing'],['3PL','3PL'],['CBS','CBS']])
    orpdf = pd.merge(orpdf,mh_identified_area_mapping, on='orphan_identified_area', how='left')
    orphan_area_pivot = pd.DataFrame(pd.pivot_table(orpdf, index=['orphan_generated_area'], columns=date_agg, fill_value=0, values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    orphan_area_pivot.columns = orphan_area_pivot.columns.droplevel(0)
    orphan_area_pivot = orphan_area_pivot.rename(columns={'':'MH Area'})

    orphan_pivot = pd.DataFrame(pd.pivot_table(orpdf, index='asset', columns=[date_agg], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    hv_pivot = pd.DataFrame(pd.pivot_table(hvdf, index='asset', columns=[date_agg], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    logistics_pivot = pd.DataFrame(pd.pivot_table(logisticsdf, index='asset', columns=[date_agg], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})

    hvdf = pd.merge(hvdf,mh_identified_area_mapping, on='orphan_identified_area', how='left')
    hv_orphan_area_pivot = pd.DataFrame(pd.pivot_table(hvdf, index=['orphan_generated_area'], columns=date_agg, fill_value=0, values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    hv_orphan_area_pivot.columns = hv_orphan_area_pivot.columns.droplevel(0)
    hv_orphan_area_pivot = orphan_area_pivot.rename(columns={'':'MH Area'})

    overall_orphans_generated = orphan_pivot.append(logistics_pivot).append(hv_pivot).fillna('0')
    overall_orphans_generated.columns = overall_orphans_generated.columns.droplevel(0)
    overall_orphans_generated = overall_orphans_generated.rename(columns={'':'asset'})
    if date_agg=='month_year':
        table_columns = [x for x in month_year if x in overall_orphans_generated.columns.tolist()]
        table_columns.insert(0,'asset')
        overall_orphans_generated = overall_orphans_generated[table_columns].reset_index().drop(columns='index')

        table_columns = [x for x in month_year if x in orphan_area_pivot.columns.tolist()]
        table_columns.insert(0,'MH Area')
        orphan_area_pivot = orphan_area_pivot[table_columns].reset_index().drop(columns='index')

        table_columns = [x for x in month_year if x in hv_orphan_area_pivot.columns.tolist()]
        table_columns.insert(0,'MH Area')
        hv_orphan_area_pivot = hv_orphan_area_pivot[table_columns].reset_index().drop(columns='index')

    return overall_orphans_generated, orphan_area_pivot, hv_orphan_area_pivot

def func_load_age_data(orphan_df1, rcdf, logisticsdf):
    # ageing_sort = ['1-9 days', '10-16 days', '17-23 days', '24-31 days', 'Older 31 days']

    orphan_df1 = orphan_df1[orphan_df1['is_tracking_id_available']=='No']
    merged_orphan = pd.merge(orphan_df1[~orphan_df1.orphan_id.isna()], rcdf[~rcdf.orphan_id.isna()][['orphan_id']], left_on='orphan_id', right_on = 'orphan_id', how='left')
    merged_orphan['age']=0
    merged_orphan['age'] = (datetime.today().date() - pd.to_datetime(merged_orphan['scanned_date']).dt.date)/np.timedelta64(1, 'D')

    lastmile_df = logistics_df[logistics_df.asset=='Last Mile']
    merged_lastmile = pd.merge(lastmile_df[~lastmile_df.orphan_id.isna()], rcdf[~rcdf.orphan_id.isna()][['orphan_id']], left_on='orphan_id', right_on = 'orphan_id', how='left')
    merged_lastmile['age']=0
    merged_lastmile['age'] = (datetime.today().date() - pd.to_datetime(merged_lastmile['scanned_date']).dt.date)/np.timedelta64(1, 'D')

    firstmile_df = logistics_df[logistics_df.asset=='First Mile']
    merged_firstmile = pd.merge(firstmile_df[~firstmile_df.orphan_id.isna()], rcdf[~rcdf.orphan_id.isna()][['orphan_id']], left_on='orphan_id', right_on = 'orphan_id', how='left')
    merged_firstmile['age']=0
    merged_firstmile['age'] = (datetime.today().date() - pd.to_datetime(merged_firstmile['scanned_date']).dt.date)/np.timedelta64(1, 'D')
    if merged_orphan.empty:
        ageing_mh_pivot = pd.DataFrame(columns=['ageing_category','orphan_count'])
        ageing_lastmile_pivot = pd.DataFrame(columns=['ageing_category','orphan_count'])
    else:
        merged_orphan['ageing_category'] = merged_orphan['age'].apply(lambda x: '1-9 days' if x <= 9 else ('10-16 days' if ((x >9) & (x <= 16) ) else ('17-23 days') if ((x >16) & (x <= 23) ) else ('24-31 days' if ((x >23) & (x <= 31) ) else 'Above 31 days')))
        ageing_mh_pivot = pd.DataFrame(pd.pivot_table(merged_orphan[~merged_orphan.orphan_id.isna()], index=['asset','ageing_category'], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
        ageing_mh_zone_pivot = pd.DataFrame(pd.pivot_table(merged_orphan[~merged_orphan.orphan_id.isna()], index=['ageing_category','zone'], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})

        merged_lastmile['ageing_category'] = merged_lastmile['age'].apply(lambda x: '1-9 days' if x <= 9 else ('10-16 days' if ((x >9) & (x <= 16) ) else ('17-23 days') if ((x >16) & (x <= 23) ) else ('24-31 days' if ((x >23) & (x <= 31) ) else 'Above 31 days')))
        ageing_lastmile_pivot = pd.DataFrame(pd.pivot_table(merged_lastmile[~merged_lastmile.orphan_id.isna()], index=['asset','ageing_category'], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})

        merged_firstmile['ageing_category'] = merged_firstmile['age'].apply(lambda x: '1-9 days' if x <= 9 else ('10-16 days' if ((x >9) & (x <= 16) ) else ('17-23 days') if ((x >16) & (x <= 23) ) else ('24-31 days' if ((x >23) & (x <= 31) ) else 'Above 31 days')))
        ageing_firstmile_pivot = pd.DataFrame(pd.pivot_table(merged_firstmile[~merged_firstmile.orphan_id.isna()], index=['asset','ageing_category'], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})

    ageing_pivot = ageing_mh_pivot.append(ageing_lastmile_pivot).append(ageing_firstmile_pivot).fillna(0)
    ageing_pivot = ageing_pivot.sort_values(by='ageing_category')
    return ageing_pivot, ageing_mh_zone_pivot



def func_overall_trend_count_fig(df, date_agg, tickformat, xasisname):
    figure = go.Figure({
                    'data':[go.Scatter(x=df[date_agg],
                                        y=df.orphan_count,
                                        line = dict(color='firebrick', width=2),
                                        # xperiod='M7',
                                        mode='markers+lines')],
                    'layout':{'title':'Overall Orphans generation Trend',
                                # 'xaxis':{'title':'Business Units'},
                                'yaxis':{'title':'Orphans Generated'},
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

def func_overall_trend_val_fig(df, date_agg, tickformat, xasisname):
    figure = go.Figure({
                    'data':[go.Scatter(x=df[date_agg],
                                        y=df.orphan_count,
                                        line = dict(color='firebrick', width=2),
                                        # xperiod='M7',
                                        mode='markers+lines')],
                    'layout':{'title':'Overall Orphans generation Value Trend',
                                # 'xaxis':{'title':'Business Units'},
                                'yaxis':{'title':'Orphans Generated'},
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

def fun_converted_perc_bar_fig(df, date_agg, tickformat, xasisname):
    # figure = go.Figure({
    #                      'data':[go.Bar(x = df[(df.is_tracking_id_available=='Yes')&(df[date_agg]==date_val)][date_agg],
    #                                      y=df[(df.is_tracking_id_available=='Yes')&(df[date_agg]==date_val)].orphan_count/df[df[date_agg]==date_val].orphan_count.sum()*100 ,
    #                                     #  text= df.orphan_count.apply(lambda x:"{:,}".format(x)),
    #                                     text=round(df[(df.is_tracking_id_available=='Yes')&(df[date_agg]==date_val)].orphan_count/df[df[date_agg]==date_val].orphan_count.sum()*100,2),
    #                                      marker_color=['#236CB9']
    #                                      ) for date_val in df[date_agg].unique() ],
    #                      'layout':go.Layout({'title':'Shipment Identified Ratio', 'showlegend':False,
    #                                         'xaxis':dict(title=xasisname,
    #                                         nticks =7,
    #                                         # ticktext = df[date_agg],
    #                                         tickvals = df[date_agg].unique()),
    #                                         'yaxis':dict(title='orphans conversion %'),
    #                                         'paper_bgcolor':'#ffffe6', 'plot_bgcolor':'#aebfd0'})
    #                  })
    # fig = px.line(df, x=date_agg, y="percentage",
    #                         template= {'layout':{'paper_bgcolor':'#ffffe6', 'plot_bgcolor':'#aebfd0',
    #                                             'xaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,},
    #                                             'yaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,}
    #                                             }},
    #                                             title="Conversion Percentage")
    
    fig = go.Figure()
    fig.update_layout({
                'plot_bgcolor': '#aebfd0',
                'paper_bgcolor': '#ffffe6','title':"Conversion Percentage",
                'yaxis':dict(title='orphans conversion %'),
                'xaxis':dict(title=xasisname),
                })
    fig.add_scattergl(x=df[date_agg], y=df.percentage, line={'color': 'red'}, name = 'Below 60%', mode='lines', opacity=0.5)
    fig.add_scattergl(x=df[date_agg], y=df.percentage.where(df.percentage >= 70), line={'color': 'green'}, name = 'Above 70%' , mode='markers+lines+text')
    fig.add_scattergl(x=df[date_agg], y=df.percentage.where((df.percentage >= 60) & (df.percentage < 70)), line={'color': 'orange'}, name = '60 - 70%', mode='markers+lines+text')
    # fig.add_scattergl(x=df[date_agg], y=df.percentage.where(df.percentage < 60 ), line={'color': 'red'}, name = 'Below 60%')
    return fig

def fun_ageing_bar_fig(df):
    figure = px.bar(df, x='ageing_category', y='orphan_count', text='orphan_count', color='asset', barmode='group',
                            # orientation='v', #category_orders={'month_yr':cat_order},
                            # template= {'layout':{'paper_bgcolor':'#ffffe6', 'plot_bgcolor':'#aebfd0',
                            #                     'xaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,},
                            #                     'yaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,}
                            #                     }},
                            labels={'ageing_category':'Ageing',
                                    'orphan_count': 'Orphans'},
                            title="Orphan Identified count")
                 
    return figure

def fun_ageing_zone_bar_fig(df, asset):
    figure = px.bar(df, x='ageing_category', y='orphan_count', text='orphan_count',barmode="group", facet_col="zone", color='orphan_count',
                            orientation='v', #category_orders={'month_yr':cat_order},
                            template= {'layout':{'paper_bgcolor':'#ffffe6', 'plot_bgcolor':'#aebfd0',
                                                'xaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,},
                                                'yaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,}
                                                }},
                            labels={'ageing_category':'Ageing',
                                    'orphan_count': 'Orphans'},
                            title=asset + " Ageing Zone wise")
                 
    return figure

def fun_ageing_rc_bar_fig(df):
    figure = px.bar(df, x='ageing_category', y='orphan_count', text='orphan_count',color='asset', barmode='group',
                            orientation='v', #category_orders={'month_yr':cat_order},
                            template= {'layout':{'paper_bgcolor':'#ffffe6', 'plot_bgcolor':'#aebfd0',
                                                'xaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,},
                                                'yaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,}
                                                }},
                            labels={'ageing_category':'Ageing',
                                    'orphan_count': 'Orphans'},
                            title="Ageing of Orphans pending to be Received at RC ")
                 
    return figure

def func_generate_shiptype_bar_figure(df, date_agg, xasisname):
    figure = px.bar(df, x=date_agg, y='orphan_count', color='shipment_type', 
                            barmode='group', orientation='v', category_orders={'month_yr':cat_order},
                            template= {'layout':{'paper_bgcolor':'#ffffe6', 'plot_bgcolor':'#aebfd0',
                                                'xaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,},
                                                'yaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,}
                                                }},
                            labels={'scanned_date' if xasisname=='Scanned Date' else ('weeknum' if xasisname=='Week' else 'month_yr'):xasisname,
                                    'orphan_count': 'Orphans Generated',
                                    'shipment_type': 'Shipment Type'},
                                    title="Shipment Type Exception generation")
    return figure

def func_generate_orphan_reason_trend_fig(df, date_agg, xasisname):
    figure = go.Figure({
                'data':[go.Scatter(x=df[date_agg].unique(),
                                    y=df[df.orphan_reason==reason].orphan_count,
                                    line = dict(color='firebrick', width=2),
                                    name = reason,
                                    text = reason,
                                    line_color=rc_color,
                                    mode='markers+lines') for reason, rc_color in zip(df.orphan_reason.unique(), color_code)],
                'layout':{'title':'Orphan Reason Trend',
                            # 'xaxis':{'title':'Business Units'},
                            'yaxis':{'title':'Orphans Generated'},
                            'paper_bgcolor':'#ffffe6',
                            'plot_bgcolor':'#aebfd0',
                            'font':dict(
                                family="sans serif",
                                size=14,
                                color="black"
                            ),
                        'xaxis' : dict(
                                    # tickformat = '%Y-%b-%d',
                                    title=xasisname,
                                    tickmode = 'array',
                                    # nticks =7,
                                    ticktext = df[date_agg].unique(),
                                    #tickvals = df[date_agg_val].unique(),
                                    # tick0 = 1.0,
                                    tickangle = 35)}
            })
    
    # figure = px.line(df, x=date_agg, y=)
    return figure

def func_generate_area_fig(df, date_agg, xasisname):
    figure = go.Figure({
                'data':[go.Scatter(x=df[date_agg].unique(),
                                    y=df[df.orphan_identified_mh_area==area].orphan_count,
                                    line = dict(color='firebrick', width=2),
                                    name = area,
                                    text = area,
                                    line_color=rc_color,stackgroup='one',
                                    mode='lines') for area, rc_color in zip(df.orphan_identified_mh_area.unique(), color_code)],
                'layout':{'title':'Orphan Reason Trend',
                            # 'xaxis':{'title':'Business Units'},
                            'yaxis':{'title':'Orphans Generated'},
                            'paper_bgcolor':'#ffffe6',
                            'plot_bgcolor':'#aebfd0',
                            'font':dict(
                                family="sans serif",
                                size=14,
                                color="black"
                            ),
                'xaxis' : dict(
                            # tickformat = '%Y-%b-%d',
                            title=xasisname,
                            tickmode = 'array',
                            # nticks =7,
                            ticktext = df[date_agg].unique(),
                            #tickvals = df[date_agg_val].unique(),
                            # tick0 = 1.0,
                            tickangle = 35)}
            })
    return figure

def func_generate_table(df):
    dc_column = [{"name": str(i), "id": str(i)} for i in df.columns]
    # dc_column = df.columns.to_list()
    dc_data = df.to_dict('records')
    return dc_data, dc_column