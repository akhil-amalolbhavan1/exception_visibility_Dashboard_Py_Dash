import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_html_components.Div import Div
from dash_html_components.H1 import H1
from dash_html_components.P import P
from dashboard import app
from dashboard import server
from apps import rc_dashboard, download_raw_data, orphan_dashboard, spf_pv_dashboard, audit_dashboard
import base64
import os
import pandas as pd

image_filename = os.getcwd() +'/Dashboard/apps/flipkart-logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height=60, width=210),
        html.H2("Exception Dashboard", className="display-5"),
        html.Hr(),
        html.P(
            # "This Dashboard gives the visibility of orphan generation in the FK system", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                # dbc.NavLink("MH Dashboard", href="/apps/mh_dashboard", active="exact"),
                dbc.NavLink("Orphan Dashboard", href="/apps/orphan_dashboard", active="exact"),
                dbc.NavLink("RC Dashboard", href="/apps/rc_dashboard", active="exact"),
                dbc.NavLink("SPF & PV", href="/apps/spf_pv", active="exact"),
                dbc.NavLink("Audit Dashboard", href="/apps/audit_dashboard", active="exact"),
                dbc.NavLink("Download Data", href="/apps/download_raw_data", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

rcdf = pd.DataFrame()
orphandf = pd.DataFrame()
def layout():
    # global mhdf
    global rcdf
    global orphandf
    global logisticsdf
    global hvdf
    global pvdf
    global spfdf
    global auditdf
    global historicdf
    global materialisticattritiondf
    # mhdf = pd.read_csv(os.getcwd() +'/Dashboard/data/mh_full_data.csv', low_memory=False)
    basepath = '/Users/a/Documents/GitHub/exception_visibility/'
    rcdf = pd.read_csv(basepath + '/Dashboard/data/rc_full_data.csv', low_memory=False)
    orphandf = pd.read_csv(basepath +'/Dashboard/data/orphan_full_data.csv', low_memory=False)
    hvdf = pd.read_csv(basepath +'/Dashboard/data/hv_orphan_full_data.csv', low_memory=False)
    logisticsdf = pd.read_csv(basepath +'/Dashboard/data/logistcs_orphan_full_data.csv', low_memory=False)
    pvdf = pd.read_csv(basepath +'/Dashboard/data/pv_full_data.csv', low_memory=False)
    spfdf = pd.read_csv(basepath +'/Dashboard/data/spf_full_data.csv', low_memory=False)
    auditdf = pd.read_csv(basepath +'/Dashboard/data/audit_full_data.csv', low_memory=False)
    historicdf = pd.read_csv(basepath +'/Dashboard/data/historicmetric_full_data.csv', low_memory=False)
    materialisticattritiondf = pd.read_csv(basepath +'/Dashboard/data/materialistic_attrition_full_data.csv', low_memory=False)
    # print(mhdf.scanned_date.count())
    return html.Div([
            dcc.Location(id="url"),
            sidebar,
            content
            ])

# layout = layout()

app.layout = layout

@app.callback(Output('page-content', 'children'),
              #[Input('link_returns_dashboard', 'href')])
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/rc_dashboard':
        return rc_dashboard.get_layout(rcdf)
    # elif pathname == '/apps/mh_dashboard':
    #     return  mh_dashboard.get_layout(mhdf)
    elif pathname == '/apps/orphan_dashboard':
        return  orphan_dashboard.get_layout(orphandf,rcdf,logisticsdf, hvdf, historicdf, materialisticattritiondf)
    elif pathname == '/apps/spf_pv':
        return  spf_pv_dashboard.get_layout(pvdf, spfdf)
    elif pathname == '/apps/audit_dashboard':
        return  audit_dashboard.get_layout(auditdf)
    elif pathname == '/apps/download_raw_data':
        return  download_raw_data.layout
    elif pathname == '/':
        layout_index = html.Div([
                        # html.H3('Please find below information before going to dashboard'),
                        html.H1(),
                        html.Div([
                        # dcc.Markdown('All the data is based on google tracker filled by the respective teams'),
                        html.H1(['Flipkart Exception Visibility']),
                        html.P("This Dashboard gives the visibility of orphan generation in the FK system", className="lead"),
                        html.P("The dashboard is based on the data generated on the google sheets by the ground staffs at different legs", className="lead"),
                        html.P("Please click on the side links to see the respective dashboards", className="lead")
                        ],style={'text-align':'center', 'display': 'inline-block', 'vertical-align': 'middle', 'line-height': 'normal'})
                        # dcc.Link('RC Dashboard',id='rc_dashboard', href='apps/rc_dashboard'),
                        # html.Div([]),
                        # dcc.Link('Download Raw Data',id='download_dashboard', href='apps/download_raw_data'),
                        # html.Div(id='page-content', children=[])
                    ],style={'textAlign':'center', 'margin':'0px', 'min-height':'500px'})

        return layout_index
    else:
        return 404


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port = '8050')
    # app.run_server(debug=True)
