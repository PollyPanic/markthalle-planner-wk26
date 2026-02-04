from dash import callback, Input, Output
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
