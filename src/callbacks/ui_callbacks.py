from dash import callback, Input, Output, State, MATCH
from src.index import app

@callback(
    Output('edit-collapse-room', 'is_open'),
    Input('edit-room-dropdown', 'value')
)
def toggle_edit_room_collapse(val):
    return val == 'OTHER'

@callback(
    Output('collapse-room-input', 'is_open'),
    Input('room-dropdown', 'value')
)
def toggle_new_room_collapse(val):
    return val == 'OTHER'

@app.callback(
    Output({'type': 'card-collapse', 'index': MATCH}, 'is_open'),
    Output({'type': 'card-toggler', 'index': MATCH}, 'children'),
    Input({'type': 'card-toggler', 'index': MATCH}, 'n_clicks'),
    State({'type': 'card-collapse', 'index': MATCH}, 'is_open'),
    prevent_initial_call=True
)
def toggle_card(n, is_open):
    if n:
        if is_open:
            return False, "Details"
        else:
            return True, "Schließen"
    return is_open, "Details"
