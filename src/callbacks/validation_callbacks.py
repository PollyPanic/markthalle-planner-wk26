from dash import callback, Input, Output, State, html
import dash_bootstrap_components as dbc
from src.index import app, manager

@callback(
    Output('time-conflict-warning', 'children'),
    Input('room-dropdown', 'value'),
    Input('time-dropdown', 'value'),
    Input('duration-input', 'value'),
    prevent_initial_call=True
)
def check_new_event_conflict(room, start_time, duration):
    if not start_time or not duration or room != 'SoS-Kubus':
        return ""

    try:
        result = manager.check_time_conflict(start_time, duration, room)
        if result['conflict']:
            conflicts = result['conflicting_events']
            conflict_info = ", ".join([f"'{c['title']}' ({c['start']}-{c['end']})" for c in conflicts])
            return dbc.Alert([
                html.I(className="bi bi-exclamation-triangle-fill me-2"),
                html.Span(f"Bitte eine andere Zeit wählen - Raum bereits belegt: {conflict_info}")
            ], color="danger", className="mb-0")
        return dbc.Alert([
            html.I(className="bi bi-check-circle-fill me-2"),
            html.Span("Raum verfügbar!")
        ], color="success", className="mb-0")
    except:
        return ""

@callback(
    Output('edit-time-conflict-warning', 'children'),
    Input('edit-room-dropdown', 'value'),
    Input('edit-time-dropdown', 'value'),
    Input('edit-duration-input', 'value'),
    State('edit-guid-store', 'data'),
    prevent_initial_call=True
)
def check_edit_event_conflict(room, start_time, duration, guid):
    if not start_time or not duration or room != 'SoS-Kubus':
        return ""

    try:
        result = manager.check_time_conflict(start_time, duration, room, exclude_guid=guid)
        if result['conflict']:
            conflicts = result['conflicting_events']
            conflict_info = ", ".join([f"'{c['title']}' ({c['start']}-{c['end']})" for c in conflicts])
            return dbc.Alert([
                html.I(className="bi bi-exclamation-triangle-fill me-2"),
                html.Span(f"Bitte eine andere Zeit wählen - Raum bereits belegt: {conflict_info}")
            ], color="danger", className="mb-0")
        return dbc.Alert([
            html.I(className="bi bi-check-circle-fill me-2"),
            html.Span("Raum verfügbar!")
        ], color="success", className="mb-0")
    except:
        return ""
