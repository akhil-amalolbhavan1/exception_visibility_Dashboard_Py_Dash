# import dash
import pandas as pd
# import numpy as np
#import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
# import plotly.graph_objs as go
import dash_table
# import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import datetime as dt,timedelta
import os
from dashboard import app
# from dashboard import app

basePath = '/Users/a/Documents/GitHub/exception_visibility/'
datesdf = pd.read_csv(basePath + 'Dashboard/Data/week_details.csv')
datesdf.weekday = pd.to_datetime(datesdf.weekday)

ddformvalues = ['RC Data', 'MH Orphan Data', 'MH HV Orphan Data', 'Logistics Orphan Data']

dbc.Row(dbc.Col(
            dbc.Spinner(children=[dcc.Graph(id="loading-output")], size="lg", color="primary", type="border", fullscreen=True,),
            # spinner_style={"width": "10rem", "height": "10rem"}),
            # spinnerClassName="spinner"),
            # dcc.Loading(children=[dcc.Graph(id="loading-output")], color="#119DFF", type="dot", fullscreen=True,),

            width={'size': 12, 'offset': 0}),
        ),


layout = html.Div([
                html.Div([
                    dcc.DatePickerRange(
                                            id='dt_range',
                                            min_date_allowed=datesdf.weekday.min(),
                                            max_date_allowed=dt.today(),
                                            initial_visible_month=dt.today(),
                                            #style={'width':'30%','display':'block', 'padding':'0', 'max-height':'300px'},
                                            start_date= dt.today()-timedelta(days=10),
                                            # end_date=datesdf.weekday.max()-timedelta(days=1)
                                            end_date = dt.today(),
                                            style={'width':'300px'}
                                        )], style={'width':'300px', 'align':'center'}),
                    dcc.Dropdown(id='dd_formselector', 
                                        options = [{'label':name, 'value':name} for name in ddformvalues],
                                        value = 'RC Data', #multi=True,clearable=False,
                                        style={'width':'300px'}),
                    # dbc.DropdownMenu( id='dbc_dropdown',
                    #                     label="Menu", bs_size="lg", color='primary',right=False,
                    #                     children=[
                    #                         dbc.DropdownMenuItem(name) for name in ddformvalues
                    #                     ]),
                    html.Div([
                        dbc.Row(dbc.Col(
                                dbc.Spinner(children=[
                                                    dash_table.DataTable(
                                                                id='dc_table',
                                                                columns = [],
                                                                data = [],
                                                                filter_action = 'native',
                                                                sort_action ='native',
                                                                export_format = 'csv',
                                                                export_columns='visible',
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
                                                                                'backgroundColor': '#004d80',
                                                                                # 'fontWeight': 'bold',
                                                                                'color':'white'
                                                                            },
                                                                style_data={ 'border-color': 'rgb(0, 77, 128)' }
                                                                ),
                                                                html.Button("Export Data", id="export_table", **{"data-dummy": ""}, className="btn btn-primary")
                                                                
                                                ], color="success", type="border", fullscreen=False, 
                                                spinner_style={"width": "10rem", "height": "10rem"},),#size="lg", 
                                
                                # spinnerClassName="spinner"),
                                # dcc.Loading(children=[dcc.Graph(id="loading-output")], color="#119DFF", type="dot", fullscreen=True,),

                                width={'size': 12, 'offset': 0}),
                            ),
                    ], style={'overflow':'auto', 'width':'100%'})
                    ],
                                        style={'width':'100%','align':'center'})


@app.callback([
            Output("dc_table", "data"),
            Output('dc_table', 'columns')],
            [Input('dd_formselector','value'),
            Input('dt_range','start_date'),
            Input('dt_range','end_date')])
def reload_rejection_reason_trend_graphs( dd_formselector_value, start_date, end_date):
    dc_data, dc_column = fun_datatable_column_data(dd_formselector_value, start_date, end_date)
    # print(start_date)
    return dc_data, dc_column

app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0)
            document.querySelector("#dc_table button.export").click()
        return ""
    }
    """,
    Output("export_table", "data-dummy"),
    [Input("export_table", "n_clicks")]
)


def fun_datatable_column_data(form_value, start_date, end_date):
    #print(df.count())
    # df_DC = df[((df[rejection_column] != "0") & (df[rejection_column] != "CP"))]
    rc_raw_data_location = basePath + 'ETL/RC_Raw_Data/'
    # mh_raw_data_location = basePath + 'ETL/MH_Raw_Data/'
    orphan_raw_data_location = basePath + 'ETL/Orphan_Raw_Data/'
    hv_orphan_raw_data_location = basePath + 'ETL/HV_Orphan_Raw_Data/'
    logistics_raw_data_location = basePath + 'ETL/Logistics_Raw_Data/'
    df = pd.DataFrame()
    if form_value=='RC Data':
        df = collate_data(start_date, end_date, rc_raw_data_location)
        # df = pd.read_csv(os.getcwd() +'/Dashboard/data/rc_full_data.csv')
    elif form_value == 'MH Orphan Data':
        df = collate_data(start_date, end_date, orphan_raw_data_location)
        # df = pd.read_csv(os.getcwd() +'/Dashboard/data/orphan_full_data.csv')
    elif form_value == 'MH HV Orphan Data':
        df = collate_data(start_date, end_date, hv_orphan_raw_data_location)
        # df = pd.read_csv(os.getcwd() +'/Dashboard/data/hv_orphan_full_data.csv')
    elif form_value == 'Logistics Orphan Data':
        df = collate_data(start_date, end_date, logistics_raw_data_location)
        # df = pd.read_csv(os.getcwd() +'/Dashboard/data/logistcs_orphan_full_data.csv')
    dc_column = [{"name": i, "id": i} for i in df.columns]
    # dc_column = df.columns.to_list()
    dc_data = df.to_dict('records')
    return dc_data, dc_column

def collate_data(start_date, end_date, location):
    all_files = os.listdir(location)
    print(all_files)
    csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
    # csv_files = 
    tempfile = ''
    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()
    no_of_days = (end_date - start_date).days
    df = pd.DataFrame() 
    print(no_of_days)
    for i in range(0, no_of_days):
        start_date = start_date - timedelta(1)
        file = start_date.strftime("%Y-%m-%d") + '.csv'
        if file in csv_files:
            df = df.append(pd.read_csv(location + file))
    return df