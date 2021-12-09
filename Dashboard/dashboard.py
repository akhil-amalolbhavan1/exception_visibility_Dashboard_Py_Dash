import dash
import dash_bootstrap_components as dbc
# app = dash.Dash(__name__, suppress_callback_exceptions=True, meta_tags=[{'name':'viewport',
#                                                                         'content':'width = device-width, initial-scale=1.0'}])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.LUMEN, '/assets/custom.css'], suppress_callback_exceptions=True)
server = app.server
