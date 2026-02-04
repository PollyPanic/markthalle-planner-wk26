from dash import html, dcc
import dash_bootstrap_components as dbc
from src.index import TIME_OPTIONS
from src.config import TYPE_OPTIONS, LANG_OPTIONS, ROOM_OPTIONS


def create_edit_modal():
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Eintrag bearbeiten / löschen")),
        dbc.ModalBody([
            dbc.Label("Raum"),
            dcc.Dropdown(
                id='edit-room-dropdown',
                options=ROOM_OPTIONS, # type: ignore
                clearable=False
            ),
            dbc.Collapse(
                dbc.Input(id='edit-other-room-input', className="mt-2"),
                id='edit-collapse-room',
                is_open=False
            ),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Startzeit", className="mt-2"),
                    dcc.Dropdown(id='edit-time-dropdown', options=TIME_OPTIONS)
                ], width=8),
                dbc.Col([
                    dbc.Label("Dauer", className="mt-2"),
                    dbc.Input(id='edit-duration-input', type='text')
                ], width=4),
            ]),
            html.Div(id='edit-time-conflict-warning', className="mt-2"),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Typ"),
                    dcc.Dropdown(id='edit-type-dropdown', options=TYPE_OPTIONS, clearable=False) # type: ignore
                ], width=6),
                dbc.Col([
                    dbc.Label("Sprache"),
                    dcc.Dropdown(
                        id='edit-lang-dropdown',
                        options=[{'label': 'Deutsch', 'value': 'Deutsch'},
                                {'label': 'English', 'value': 'English'},
                                {'label': 'Français', 'value': 'Français'}],
                        clearable=False
                    )
                ], width=6)
            ], className="mt-2"),
            dbc.Label("Titel", className="mt-2"),
            dbc.Input(id='edit-title-input', type='text'),
            dbc.Label("Beschreibung", className="mt-2"),
            dbc.Textarea(id='edit-desc-input', style={'height': 100}),
            dbc.Label("Name", className="mt-2"),
            dbc.Input(id='edit-name-input', type='text'),
        ]),
        dbc.ModalFooter([
            dbc.Button("Löschen", id="btn-delete-init", color="danger", outline=True, className="me-auto"),
            dbc.Button("Abbrechen", id="btn-edit-cancel", color="secondary", className="me-2"),
            dbc.Button("Änderungen speichern", id="btn-save-init", color="success")
        ])
    ], id="edit-modal", size="lg", is_open=False, centered=True)


def create_confirm_save_modal():
    return dbc.Modal([
        dbc.ModalHeader("Änderungen speichern?"),
        dbc.ModalBody("Möchtest du diese Änderungen wirklich vornehmen?"),
        dbc.ModalFooter([
            dbc.Button("Nein", id="btn-confirm-save-no", color="secondary", className="me-2"),
            dbc.Button("Ja, speichern", id="btn-confirm-save-yes", color="success")
        ])
    ], id="confirm-save-modal", is_open=False, centered=True)


def create_confirm_delete_modal():
    return dbc.Modal([
        dbc.ModalHeader("Event löschen?"),
        dbc.ModalBody("Bist du sicher? Das Eintrag wird unwiderruflich gelöscht."),
        dbc.ModalFooter([
            dbc.Button("Nein", id="btn-confirm-delete-no", color="secondary", className="me-2"),
            dbc.Button("Ja, löschen", id="btn-confirm-delete-yes", color="danger")
        ])
    ], id="confirm-delete-modal", is_open=False, centered=True)
