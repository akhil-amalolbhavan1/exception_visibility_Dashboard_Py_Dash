# Owner : Akhil A
# Version V1
# Created on :
from dash_html_components.Center import Center
from dash_html_components.Div import Div
from numpy.core.fromnumeric import trace
import pandas as pd
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
import os
import dash_bootstrap_components as dbc
from sqlalchemy import asc, null
# from Dashboard.apps.orphan_dashboard import fun_converted_perc_bar_fig
from dashboard import app
from datetime import datetime, timedelta

basepath = '/Users/a/Documents/GitHub/exception_visibility/'

auditdf = pd.DataFrame()
# spfdf = pd.DataFrame()
datesdf = pd.read_csv(basepath+'/Dashboard/Data/week_details.csv')
datesdf.weekday = pd.to_datetime(datesdf.weekday)
dd_date_agg_values = ['Month Wise', 'Week Wise']

def get_layout(audit_df):
    global auditdf 
    auditdf = audit_df
    layout = html.Div([
                        html.H1('Audit Dashboard', style={'textAlign':'center', 'width':'100%', 'display':'inline-block'}),
                                        html.Br(),html.Br(),
                                        html.Div([
                            html.Label(['Choose the date range'], style={'color':'black','width':'200px','textAlign':'left','float':'left','align':'center','display':'inline-block','line-height': '50px','vertical-align': 'middle'}),
                            dcc.DatePickerRange(
                                            id='dt_range_audit',
                                            min_date_allowed=datesdf.weekday.min(),
                                            max_date_allowed=datetime.today(),
                                            initial_visible_month=datetime.today(),
                                            #style={'width':'30%','display':'block', 'padding':'0', 'max-height':'300px'},
                                            start_date= datetime.today()-timedelta(days=60),
                                            # end_date=datesdf.weekday.max()-timedelta(days=1)
                                            end_date = datetime.today(),
                                            # display_format = 'MMM-YYYY',
                                            style={'width':'300px','float':'left'}
                                        ),
                                    html.Label(['Choose the x axis for date'], style={'color':'black','width':'200px','textAlign':'left','float':'left','line-height': '50px','vertical-align': 'middle'}),
                                                dcc.Dropdown(id='dd_date_agg_audit',
                                                        options = [{'label':name, 'value':name} for name in dd_date_agg_values],
                                                        value = 'Week Wise', multi=False, #multi=True,clearable=False,
                                                        style={'float':'left','width':'200px', 'line-height': '50px','vertical-align': 'middle'}
                                                )
                                         ],  style={'align':'center'}),
                                         html.Div(style={'float':'clear'}), html.Br(),html.Br(),
                        html.Div([
                            html.Div([
                                            dcc.Graph(id='result_perc_bar',
                                            figure = go.Figure(), style={'width':'100%'})
                                            # dcc.Graph(id='ageing_bar',
                                            # figure = go.Figure(), style={'width':'50%', 'float': 'left'}),
                                        ]),
                                        html.H3('Hub Wise Fail Percentage', style={'textAlign':'center', 'width':'100%', 'display':'inline-block'}),
                            dash_table.DataTable(
                                                id='audit_trend_table',
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
                                                )]),html.Br(),html.Br(),
                                    # html.Div([
                                    #     html.Div([
                                    #         html.H3('Audit Hub wise'),
                                    #         dash_table.DataTable(
                                    #                             id='audit_hub_table',
                                    #                             columns = [],
                                    #                             data = [],
                                    #                             sort_action ='native',
                                    #                             export_headers = 'names',
                                    #                             page_size=15,
                                    #                             style_data_conditional=[
                                    #                                                     {
                                    #                                                         'if': {'row_index': 'odd'},
                                    #                                                         'backgroundColor': '#e3e6e8',
                                    #                                                         'color':'black'
                                    #                                                     },
                                    #                                                     {
                                    #                                                         'if': {'row_index': 'even'},
                                    #                                                         'backgroundColor': '#d9d9d9',
                                    #                                                         'color':'black'
                                    #                                                     }
                                    #                                                 ],
                                    #                             style_header={
                                    #                                             'backgroundColor': '#034f84',
                                    #                                             # 'fontWeight': 'bold',
                                    #                                             'color':'white'
                                    #                                         },
                                    #                             style_data={ 'border-color': '#034f84' }
                                    #             )], style={'width':'45%','float':'left'}),
                                    #             html.Div(style={'width':'10%', 'float':'left', 'height':'100px'}),
                                    #  ])
                        
    ])
    return layout

@app.callback([
                Output('audit_trend_table','data'),
                Output('audit_trend_table','columns'),
                Output('result_perc_bar', 'figure'),
                # Output('audit_hub_table','data'),
                # Output('audit_hub_table','columns'),
                ],
                [Input('dt_range_audit','start_date'),
                Input('dt_range_audit','end_date'),
                Input('dd_date_agg_audit','value')])
def update_figures(audit_start_date, audit_end_date, date_agg_val):
    # global pvdf, spfdf
    # print(type(pv_start_date))
    # print(pv_start_date[0:10])
    start_date = datetime.strptime(audit_start_date[0:10], '%Y-%m-%d')
    # end_date = datetime.strptime(pv_end_date, '%Y-%m-%dT%H:%M:%S.%f')
    end_date = datetime.strptime(audit_end_date[0:10], '%Y-%m-%d')
    auditdf.scanned_date = pd.to_datetime(auditdf.scanned_date)
    auditdf.weeknum =auditdf.weeknum.astype(int)
    # pvdf.month_year = pd.to_datetime(pvdf.month_year)
    
    # filter_start_date = str(start_date.year) + '-' + str(start_date.month) + '-' + '01'
    # if end_date.month==2:
    #     filter_end_date = str(end_date.year) + '-' + str(end_date.month) + '-' + '28'
    # else:    
    #     filter_end_date = str(end_date.year) + '-' + str(end_date.month) + '-' + '31'

    # print(filter_start_date)
    auditf_temp = auditdf[(auditdf.scanned_date >= pd.to_datetime(start_date)) & (auditdf.scanned_date <= pd.to_datetime(end_date)) ]
    # spfdf_temp = spfdf[(spfdf.month_year >= pd.to_datetime(start_date)) & (spfdf.month_year <= pd.to_datetime(end_date)) ]
    # print(filter_start_date)
    # dttm = datetime.strptime(pv_start_date, '%Y-%m-%dT%H:%M:%S.%f')
    
    xaxisname = ''
    # print(datetime.fromisoformat(pv_start_date))
    if date_agg_val=='Month Wise':
        date_agg_val = 'month_year'
        xaxisname = 'Monthly'
    else:
        date_agg_val = 'weeknum_year'
        xaxisname = 'Weekly'
    audit_pivot, hub_result_pivot = data_table_pivots(auditf_temp, date_agg=date_agg_val)
    audit_data, audit_column = func_generate_table(audit_pivot)
    perc_fig = fun_result_perc_bar_fig(audit_pivot, date_agg_val, xaxisname)
    audit_hub_data, audit_hub_column = func_generate_table(hub_result_pivot)
    # pv_hub_data, pv_hub_column = func_generate_table(pv_hub_pviot)
    return audit_hub_data, audit_hub_column, perc_fig

def data_table_pivots(audit_df, date_agg):
    # if date_agg == 'weeknum':
    #     date_agg='weeknum_year'
    # elif date_agg == 'month':
    #     date_agg='month_year'
    audit_df['month_year'] = pd.to_datetime(audit_df.scanned_date).dt.strftime('%b') + '-' + pd.to_datetime(audit_df.scanned_date).dt.year.astype(str)
    audit_df['weeknum_year'] = audit_df.weeknum.astype(str) + '-' + audit_df.year.astype(str)

    month_year = ['Jan-2021','Feb-2021', 'Mar-2021','Apr-2021','May-2021','Jun-2021','Jul-2021','Aug-2021','Sep-2021','Oct-2021','Nov-2021','Dec-2021',
                    'Jan-2022','Feb-2022', 'Mar-2022','Apr-2022','May-2022','Jun-2022','Jul-2022','Aug-2022','Sep-2022','Oct-2022','Nov-2022','Dec-2022',
                    'Jan-2023','Feb-2023', 'Mar-2023','Apr-2023','May-2023','Jun-2023','Jul-2023','Aug-2023','Sep-2023','Oct-2023','Nov-2023','Dec-2023']

    weeknum_year = ['1-2021',	'2-2021',	'3-2021',	'4-2021',	'5-2021',	'6-2021',	'7-2021',	'8-2021',	'9-2021',	'10-2021',	'11-2021',	'12-2021',	'13-2021',	'14-2021',	'15-2021',	'16-2021',	'17-2021',	'18-2021',	'19-2021',	'20-2021',	'21-2021',	'22-2021',	'23-2021',	'24-2021',	'25-2021',	
                        '26-2021',	'27-2021',	'28-2021',	'29-2021',	'30-2021',	'31-2021',	'32-2021',	'33-2021',	'34-2021',	'35-2021',	'36-2021',	'37-2021',	'38-2021',	'39-2021',	'40-2021',	'41-2021',	'42-2021',	'43-2021',	'44-2021',	'45-2021',	'46-2021',	'47-2021',	'48-2021',	'49-2021',	'50-2021',	'51-2021',	'52-2021',	'53-2021',	
                    '1-2022',	'2-2022',	'3-2022',	'4-2022',	'5-2022',	'6-2022',	'7-2022',	'8-2022',	'9-2022',	'10-2022',	'11-2022',	'12-2022',	'13-2022',	'14-2022',	'15-2022',	'16-2022',	'17-2022',	'18-2022',	'19-2022',	'20-2022',	'21-2022',	'22-2022',	'23-2022',	'24-2022',	'25-2022',	
                        '26-2022',	'27-2022',	'28-2022',	'29-2022',	'30-2022',	'31-2022',	'32-2022',	'33-2022',	'34-2022',	'35-2022',	'36-2022',	'37-2022',	'38-2022',	'39-2022',	'40-2022',	'41-2022',	'42-2022',	'43-2022',	'44-2022',	'45-2022',	'46-2022',	'47-2022',	'48-2022',	'49-2022',	'50-2022',	'51-2022',	'52-2022',	'53-2022',	
                    '1-2023',	'2-2023',	'3-2023',	'4-2023',	'5-2023',	'6-2023',	'7-2023',	'8-2023',	'9-2023',	'10-2023',	'11-2023',	'12-2023',	'13-2023',	'14-2023',	'15-2023',	'16-2023',	'17-2023',	'18-2023',	'19-2023',	'20-2023',	'21-2023',	'22-2023',	'23-2023',	'24-2023',	'25-2023',	
                        '26-2023',	'27-2023',	'28-2023',	'29-2023',	'30-2023',	'31-2023',	'32-2023',	'33-2023',	'34-2023',	'35-2023',	'36-2023',	'37-2023',	'38-2023',	'39-2023',	'40-2023',	'41-2023',	'42-2023',	'43-2023',	'44-2023',	'45-2023',	'46-2023',	'47-2023',	'48-2023',	'49-2023',	'50-2023',	'51-2023',	'52-2023',	'53-2023',	
                    '1-2024',	'2-2024',	'3-2024',	'4-2024',	'5-2024',	'6-2024',	'7-2024',	'8-2024',	'9-2024',	'10-2024',	'11-2024',	'12-2024',	'13-2024',	'14-2024',	'15-2024',	'16-2024',	'17-2024',	'18-2024',	'19-2024',	'20-2024',	'21-2024',	'22-2024',	'23-2024',	'24-2024',	'25-2024',	
                        '26-2024',	'27-2024',	'28-2024',	'29-2024',	'30-2024',	'31-2024',	'32-2024',	'33-2024',	'34-2024',	'35-2024',	'36-2024',	'37-2024',	'38-2024',	'39-2024',	'40-2024',	'41-2024',	'42-2024',	'43-2024',	'44-2024',	'45-2024',	'46-2024',	'47-2024',	'48-2024',	'49-2024',	'50-2024',	'51-2024',	'52-2024',	'53-2024']
    sort_order_monthly = [1, 2,	3, 4, 5, 6,	7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]
    sort_order_weekly = [1,	2,	3,	4,	5,	6,	7,	8,	9,	10,	11,	12,	13,	14,	15,	16,	17,	18,	19,	20,	21,	22,	23,	24,	25,	26,	27,	28,	29,	30,	31,	32,	33,	34,	35,	36,	37,	38,	39,	40,	41,	
                        42,	43,	44,	45,	46,	47,	48,	49,	50,	51,	52,	53,	54,	55,	56,	57,	58,	59,	60,	61,	62,	63,	64,	65,	66,	67,	68,	69,	70,	71,	72,	73,	74,	75,	76,	77,	78,	79,	80,	81,	82,	
                        83,	84,	85,	86,	87,	88,	89,	90,	91,	92,	93,	94,	95,	96,	97,	98,	99,	100, 101, 102, 103,	104,	105,	106,	107,	108,	109,	110,	111,	112,	113,	114,	115,
                        116, 117,	118,	119,	120,	121,	122,	123,	124,	125,	126,	127,	128,	129,	130,	131,	132,	133,	134,	135,	136,	137,	138,	139,	140,	141,	142,	143,	144,	145,	146,	147,	148,	149,	150,	151,	152,	153,	154,	155,	156,	157,	158,	159,	160,	161,	162,	163,	164,	165,	166,	167,	168,	169,	170,	171,	172,	173,	174,	175,	176,	177,	178,	179,	180,	181,	182,	183,	184,	185,	186,	187,	188,	189,	190,	191,	192,	193,	194,	195,	196,	197,	198,	199,	200,	201,	202,	203,	204,	205,	206,	207,	208,	209,	210,	211,	212,	213,	214,	215,	216,	217,	218,	219,	220,	221,	222,	223,	224,	225,	226,	227,	228]
    # sorted_list1 = [element for _, element in zipped_month]
    if date_agg=='month_year':
        zipped_list = list(zip(sort_order_monthly, month_year))
        sort_order_df = pd.DataFrame( zipped_list, columns=['sort_order',date_agg])
    else:
        zipped_list = list(zip(sort_order_weekly, weeknum_year))
        sort_order_df = pd.DataFrame( zipped_list, columns=['sort_order',date_agg])
    result_pivot = pd.DataFrame(pd.pivot_table(audit_df, index=[date_agg, 'result'], fill_value=0, values=['count'], aggfunc=sum)).reset_index()
    result_total = pd.DataFrame(pd.pivot_table(audit_df, index=[date_agg], fill_value=0, values=['count'], aggfunc=sum)).reset_index().rename(columns={'count':'total'})
    result_pivot = pd.merge(result_pivot, result_total, on = date_agg, how='left')
    result_pivot['percentage'] = round((result_pivot['count']/result_pivot['total']) * 100,2)
    # print(result_pivot)
    # result_pivot = result_pivot[result_pivot.result=='Pass']
    result_pivot = pd.merge(result_pivot, sort_order_df, on = date_agg, how='left').sort_values(by= 'sort_order')

    # hub_result_pivot =  pd.DataFrame(pd.pivot_table(audit_df, index=['motherhub_name','result'], fill_value=0, values=['count'], aggfunc=sum)).reset_index().sort_values(by='count', ascending=False)
    hub_result_pivot = pd.DataFrame(pd.pivot_table(audit_df, index=['motherhub_name'],columns=['result'], fill_value=0, values=['count'], aggfunc=sum)).reset_index().droplevel(0, axis=1).rename(columns={'':'motherhub'})
    hub_result_pivot['Total'] = hub_result_pivot.Fail + hub_result_pivot.Pass
    hub_result_pivot['Fail_Percentage'] = round((hub_result_pivot.Fail/hub_result_pivot.Total) * 100, 2)
    # hub_result_pivot = hub_result_pivot[hub_result_pivot.result=='Fail'].sort_values(by='percentage', ascending=False)
    print(hub_result_pivot)
    # hub_result_pivot = result_pivot[hub_result_pivot.result=='Pass']
    # hub_result_pivot = pd.merge(hub_result_pivot, sort_order_df, on = date_agg, how='left').sort_values(by= 'sort_order')
    # print(result_pivot)
    
    # mh_identified_area_mapping = pd.DataFrame(columns=['orphan_generated_area', 'orphan_identified_area'], data=[['Inbound Processing','Inbound Staging'],['Inbound Processing','Inbound area'],['Outbound Processing','Outbound Staging'],['Outbound Processing','Outbound area'],['Primary Processing','Primary processing'],['Secondary Processing','Secondary processing'],['3PL','3PL'],['CBS','CBS']])
    # orpdf = pd.merge(orpdf,mh_identified_area_mapping, on='orphan_identified_area', how='left')
    # orphan_area_pivot = pd.DataFrame(pd.pivot_table(orpdf, index=['orphan_generated_area'], columns=date_agg, fill_value=0, values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    # orphan_area_pivot.columns = orphan_area_pivot.columns.droplevel(0)
    # orphan_area_pivot = orphan_area_pivot.rename(columns={'':'MH Area'})
    # print(spf_df.columns)
    # pv_pivot = pd.DataFrame(pd.pivot_table(pv_df, index=['asset'], columns=date_agg, fill_value=0, values=['count'], aggfunc=sum)).reset_index()
    # pv_pivot = pv_pivot.droplevel(0,axis=1).rename(columns={'':'asset'})
    # table_columns = [x for x in month_year if x in pv_pivot.columns.tolist()]
    # table_columns.insert(0,'asset')
    # pv_pivot = pv_pivot[table_columns].reset_index().drop(columns='index')
    # spf_pivot = pd.DataFrame(pd.pivot_table(spf_df, index=['asset'], columns=date_agg, fill_value=0, values=['count'], aggfunc=sum)).reset_index()
    # # print(spf_pivot)
    # spf_pivot = spf_pivot.droplevel(0,axis=1).rename(columns={'':'asset'})
    # table_columns = [x for x in month_year if x in spf_pivot.columns.tolist()]
    # table_columns.insert(0,'asset')
    # spf_pivot = spf_pivot[table_columns].reset_index().drop(columns='index')
    # spf_pv_pivot = pv_pivot.append(spf_pivot)


    # pv_hub_pviot =  pd.DataFrame(pd.pivot_table(pv_df, index=['motherhub_name'], fill_value=0, values=['count'], aggfunc=sum)).reset_index().sort_values(by='count', ascending=False)
    # spf_hub_pviot =  pd.DataFrame(pd.pivot_table(spf_df, index=['motherhub_name'], fill_value=0, values=['count'], aggfunc=sum)).reset_index().sort_values(by='count', ascending=False)

    return result_pivot, hub_result_pivot

def func_generate_table(df):
    # print(df)
    # print(df.columns)
    dc_column = [{"name": str(i), "id": str(i)} for i in df.columns]
    # dc_column = df.columns.to_list()
    dc_data = df.to_dict('records')
    return dc_data, dc_column

def fun_result_perc_bar_fig(df, date_agg, xasisname):
    figure = px.bar(df, x=date_agg, y='percentage', color='result', 
                            barmode='group', orientation='v', #category_orders={'month_year':cat_order},
                            text='percentage',
                            template= {'layout':{'paper_bgcolor':'#ffffe6', 'plot_bgcolor':'#aebfd0',
                                                'xaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,},
                                                'yaxis': {'gridcolor':'white','showgrid':True, 'gridwidth':1,}
                                                }},
                            labels={'scanned_date' if xasisname=='Scanned Date' else ('weeknum_year' if xasisname=='Week' else 'month_year'):xasisname,
                                    'orphan_count': 'Orphans Generated',
                                    'shipment_type': 'Shipment Type'},
                                    title="Audit Pass/Fail Percentage")
    return figure