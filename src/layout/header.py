from dash import html
import dash_bootstrap_components as dbc
from src.index import app
from src.config import LOGO_FILENAME

def create_header():
    return dbc.Row([
        dbc.Col(
            html.Div(
                html.Img(src=app.get_asset_url(LOGO_FILENAME), className="logo-img"),
                className="d-flex justify-content-center justify-content-lg-start"
            ),
            width=12, lg=3, className="mb-3 mb-lg-0"
        ),
        dbc.Col(
            html.Div([
                html.H1("Programm Markthalle", className="mb-0 lh-1"),
                html.P("Self-Organized Sessions, Ausstellungen, Infostände, Treffen...", className="header-subtitle mb-0")
            ], className="text-center"),
            width=12, lg=6, className="mb-3 mb-lg-0"
        ),
        dbc.Col(
            html.Div(
                dbc.Button("Etwas anmelden", id="btn-toggle-form", color="success", className="shadow-sm", size="sm"),
                className="d-flex justify-content-center justify-content-lg-end"
            ),
            width=12, lg=3
        ),
    ], className="py-4 border-bottom mb-4 align-items-center")
