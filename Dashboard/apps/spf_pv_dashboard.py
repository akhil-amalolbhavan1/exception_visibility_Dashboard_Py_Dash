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
from sqlalchemy import null
# from datetime import datetime as dt,timedelta
# from plotly.graph_objs import bar
from dashboard import app
from datetime import datetime, timedelta

basepath = '/Users/a/Documents/GitHub/exception_visibility/'

pvdf = pd.DataFrame()
spfdf = pd.DataFrame()
datesdf = pd.read_csv(basepath+'/Dashboard/Data/week_details.csv')
datesdf.weekday = pd.to_datetime(datesdf.weekday)
dd_date_agg_values = ['Month Wise']

def get_layout(pv, spf):
    global pvdf, spfdf
    pvdf = pv
    spfdf = spf
    layout = html.Div([
                        html.H1('Orphan Dashboard', style={'textAlign':'center', 'width':'100%', 'display':'inline-block'}),
                                        html.Br(),html.Br(),
                                        html.Div([
                            html.Label(['Choose the date range'], style={'color':'black','width':'200px','textAlign':'left','float':'left','align':'center','display':'inline-block','line-height': '50px','vertical-align': 'middle'}),
                            dcc.DatePickerRange(
                                            id='dt_range_spf_pv',
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
                                                dcc.Dropdown(id='dd_date_agg_spf_pv',
                                                        options = [{'label':name, 'value':name} for name in dd_date_agg_values],
                                                        value = 'Month Wise', multi=False, #multi=True,clearable=False,
                                                        style={'float':'left','width':'200px', 'line-height': '50px','vertical-align': 'middle'}
                                                )
                                         ],  style={'align':'center'}),
                        html.Div([
                            dash_table.DataTable(
                                                id='spf_pv_trend_table',
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
                        
    ])
    return layout

@app.callback([
                Output('spf_pv_trend_table','data'),
                Output('spf_pv_trend_table','columns'),
                ],
                [Input('dt_range_spf_pv','start_date'),
                Input('dt_range_spf_pv','end_date'),
                Input('dd_date_agg_spf_pv','value')])
def update_figures(pv_start_date, pv_end_date, date_agg_val):
    print(datetime.fromisoformat(pv_start_date))
    if date_agg_val=='Month Wise':
        date_agg_val = 'month'
    pv_pivot, spf_pivot = data_table_pivots(spf_df=spfdf, pv_df=pvdf, date_agg=date_agg_val)
    spf_data, spf_column = func_generate_table(pv_pivot)
    return spf_data,spf_column

def data_table_pivots(spf_df, pv_df, date_agg):
    if date_agg == 'weeknum':
        date_agg='weeknum_year'
    # orpdf['month_year'] = pd.to_datetime(orpdf.scanned_date).dt.strftime('%b') + '-' + pd.to_datetime(orpdf.scanned_date).dt.year.astype(str)
    # orpdf['weeknum_year'] = orpdf.weeknum.astype(str) + '-' + orpdf.year.astype(str)
    # logisticsdf['month_year'] = pd.to_datetime(logisticsdf.scanned_date).dt.strftime('%b') + '-' + pd.to_datetime(logisticsdf.scanned_date).dt.year.astype(str)
    # logisticsdf['weeknum_year'] = logisticsdf.weeknum.astype(str) + '-' + logisticsdf.year.astype(str)
    # hvdf['month_year'] = pd.to_datetime(hvdf.scanned_date).dt.strftime('%b') + '-' + pd.to_datetime(hvdf.scanned_date).dt.year.astype(str)
    # hvdf['weeknum_year'] = hvdf.weeknum.astype(str) + '-' + hvdf.year.astype(str)

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

    # mh_identified_area_mapping = pd.DataFrame(columns=['orphan_generated_area', 'orphan_identified_area'], data=[['Inbound Processing','Inbound Staging'],['Inbound Processing','Inbound area'],['Outbound Processing','Outbound Staging'],['Outbound Processing','Outbound area'],['Primary Processing','Primary processing'],['Secondary Processing','Secondary processing'],['3PL','3PL'],['CBS','CBS']])
    # orpdf = pd.merge(orpdf,mh_identified_area_mapping, on='orphan_identified_area', how='left')
    # orphan_area_pivot = pd.DataFrame(pd.pivot_table(orpdf, index=['orphan_generated_area'], columns=date_agg, fill_value=0, values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    # orphan_area_pivot.columns = orphan_area_pivot.columns.droplevel(0)
    # orphan_area_pivot = orphan_area_pivot.rename(columns={'':'MH Area'})

    pv_pivot = pd.DataFrame(pd.pivot_table(pv_df, index=['asset'], columns=date_agg, fill_value=0, values=['shipment_id'], aggfunc=sum)).reset_index().rename(columns={'shipment_id': 'count'})
    spf_pivot = pd.DataFrame(pd.pivot_table(spf_df, index=['asset'], columns=date_agg, fill_value=0, values=['shipment_id'], aggfunc=sum)).reset_index().rename(columns={'shipment_id': 'count'})


    # orphan_pivot = pd.DataFrame(pd.pivot_table(orpdf, index='asset', columns=[date_agg], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    # hv_pivot = pd.DataFrame(pd.pivot_table(hvdf, index='asset', columns=[date_agg], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    # logistics_pivot = pd.DataFrame(pd.pivot_table(logisticsdf, index='asset', columns=[date_agg], values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})

    # hvdf = pd.merge(hvdf,mh_identified_area_mapping, on='orphan_identified_area', how='left')
    # hv_orphan_area_pivot = pd.DataFrame(pd.pivot_table(hvdf, index=['orphan_generated_area'], columns=date_agg, fill_value=0, values=['scanned_timestamp'], aggfunc=len)).reset_index().rename(columns={'scanned_timestamp': 'orphan_count'})
    # hv_orphan_area_pivot.columns = hv_orphan_area_pivot.columns.droplevel(0)
    # hv_orphan_area_pivot = orphan_area_pivot.rename(columns={'':'MH Area'})

    # overall_orphans_generated = orphan_pivot.append(logistics_pivot).append(hv_pivot).fillna('0')
    # overall_orphans_generated.columns = overall_orphans_generated.columns.droplevel(0)
    # overall_orphans_generated = overall_orphans_generated.rename(columns={'':'asset'})
    # if date_agg=='month_year':
    #     table_columns = [x for x in month_year if x in overall_orphans_generated.columns.tolist()]
    #     table_columns.insert(0,'asset')
    #     overall_orphans_generated = overall_orphans_generated[table_columns].reset_index().drop(columns='index')

    #     table_columns = [x for x in month_year if x in orphan_area_pivot.columns.tolist()]
    #     table_columns.insert(0,'MH Area')
    #     orphan_area_pivot = orphan_area_pivot[table_columns].reset_index().drop(columns='index')

    #     table_columns = [x for x in month_year if x in hv_orphan_area_pivot.columns.tolist()]
    #     table_columns.insert(0,'MH Area')
    #     hv_orphan_area_pivot = hv_orphan_area_pivot[table_columns].reset_index().drop(columns='index')

    # elif date_agg=='weeknum_year':
    #     table_columns = [x for x in weeknum_year if x in overall_orphans_generated.columns.tolist()]
    #     table_columns.insert(0,'asset')
    #     overall_orphans_generated = overall_orphans_generated[table_columns].reset_index().drop(columns='index')

    #     table_columns = [x for x in weeknum_year if x in orphan_area_pivot.columns.tolist()]
    #     table_columns.insert(0,'MH Area')
    #     orphan_area_pivot = orphan_area_pivot[table_columns].reset_index().drop(columns='index')

    #     table_columns = [x for x in weeknum_year if x in hv_orphan_area_pivot.columns.tolist()]
    #     table_columns.insert(0,'MH Area')
    #     hv_orphan_area_pivot = hv_orphan_area_pivot[table_columns].reset_index().drop(columns='index')

    return pv_pivot, spf_pivot

def func_generate_table(df):
    dc_column = [{"name": str(i), "id": str(i)} for i in df.columns]
    # dc_column = df.columns.to_list()
    dc_data = df.to_dict('records')
    return dc_data, dc_column