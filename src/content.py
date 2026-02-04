from dash import html, dcc
import dash_bootstrap_components as dbc
import flask
import os
from src.index import app, server
from src.config import JSON_FILE, SLIDES_JSON_FILE, APP_PATH
from src.layout.header import create_header
from src.layout.schedule_view import build_schedule_view
from src.layout.form import create_add_form
from src.layout.modals import create_edit_modal, create_confirm_save_modal, create_confirm_delete_modal

from src.callbacks import form_callbacks, edit_callbacks, validation_callbacks, ui_callbacks

@server.route('/schedule/export/schedule.json')
def serve_schedule_json():
    file_path = os.path.join(os.getcwd(), JSON_FILE)
    if not os.path.exists(file_path):
        from src.config import JSON_FILE as ABS_JSON_FILE
        file_path = ABS_JSON_FILE  
        
    response = flask.send_file(file_path, mimetype='application/json')
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@server.route('/schedule/export/slides.json')
def serve_slides_json():
    file_path = SLIDES_JSON_FILE
    if not os.path.exists(file_path):
        from src.config import JSON_FILE as FALLBACK
        file_path = FALLBACK
    
    response = flask.send_file(file_path, mimetype='application/json')
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

def serve_layout():
    return dbc.Container([
        dcc.Store(id='edit-guid-store'),
        dcc.Store(id='op-success-signal'),
        create_header(),
        create_add_form(),
        dbc.Row(dbc.Col([
            html.Div(id='schedule-container', children=build_schedule_view())
        ], width=12)),
        dbc.Row(dbc.Col([
            html.Hr(className="mt-5"),
            html.P([
                "Export ",
                html.A("full schedule", href=f"{APP_PATH}schedule/export/schedule.json", target="_blank",
                       className="fw-bold text-decoration-none"), 
                " or ",
                html.A("schedule for slides", href=f"{APP_PATH}schedule/export/slides.json", target="_blank",
                       className="fw-bold text-decoration-none")
            ], className="text-center text-muted small pb-4")
        ])),
        create_edit_modal(),
        create_confirm_save_modal(),
        create_confirm_delete_modal(),
    ], fluid=True, className="min-vh-100 p-3 p-md-5")

app.layout = serve_layout
