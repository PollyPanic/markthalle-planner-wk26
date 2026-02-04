import dash
import dash_bootstrap_components as dbc
from src.data_manager import DataManager
from src.config import JSON_FILE, APP_PATH
import os

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    assets_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets'),
    routes_pathname_prefix='/',
    requests_pathname_prefix=APP_PATH
)

app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        
        <link rel="icon" type="image/svg+xml" href="{APP_PATH}assets/logo_kongress.svg">
        
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''

app.title = "Markthalle Winterkongress 2026"
server = app.server

manager = DataManager(JSON_FILE)

TIME_OPTIONS = manager.get_time_options(step_minutes=15)
