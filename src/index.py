import dash
import dash_bootstrap_components as dbc
from src.data_manager import DataManager
from src.config import JSON_FILE

import os
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    assets_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
)

app.title = "Markthalle Winterkongress 2026"
server = app.server

manager = DataManager(JSON_FILE)

TIME_OPTIONS = manager.get_time_options(step_minutes=15)
