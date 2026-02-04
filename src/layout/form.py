from dash import html, dcc
import dash_bootstrap_components as dbc
from src.index import TIME_OPTIONS
from src.config import TYPE_OPTIONS, LANG_OPTIONS, ROOM_OPTIONS

def create_add_form():
    return dbc.Row(dbc.Col([
        dbc.Collapse(
            dbc.Card([
                dbc.CardHeader("Etwas zum Programm hinzufügen", className="bg-success text-white fw-bold"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Alert([
                                html.H4("Macht mit!", className="alert-heading mb-3"),
                                html.P("Für Self-Organized Sessions steht in der Markthalle ein Raum (\"SoS-Kubus\") zur Verfügung (nicht betreut).", className="mb-2"),
                                html.P("Der Raum bietet Platz für bis zu 20-25 Personen und ist mit einem Projektor/Beamer sowie einem Flipchart ausgestattet.", className="mb-2"),
                                html.P("Wenn ihr den Raum nutzen möchtet, könnt ihr ihn hier reservieren.", className="mb-2"),
                                html.Hr(),
                                html.P("Kleinere Sessions, Treffen etc. können auch 'lose' in der Markthalle stattfinden. Wenn ihr etwas organisieren möchtet, habt ihr hier die Möglichkeit es zu veröffentlichen.", className="mb-0 small")
                            ], color="light", className="border h-100")
                        ], width=12, lg=4, className="mb-3 mb-lg-0"),
                        dbc.Col([
                            dbc.Label("Raum"),
                            dcc.Dropdown(
                                id='room-dropdown',
                                options=ROOM_OPTIONS, # type: ignore
                                value='SoS-Kubus',
                                clearable=False
                            ),
                            dbc.Collapse(
                                dbc.Input(id='other-room-input', placeholder='Name des Ortes...', className="mt-2"),
                                id='collapse-room-input',
                                is_open=False
                            ),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Startzeit", className="mt-2"),
                                    dcc.Dropdown(id='time-dropdown', options=TIME_OPTIONS, placeholder="Zeit wählen...")
                                ], width=12, md=8),
                                dbc.Col([
                                    dbc.Label("Dauer", className="mt-2"),
                                    dbc.Input(id='duration-input', type='text', value="00:30")
                                ], width=12, md=4),
                            ]),
                            html.Div(id='time-conflict-warning', className="mt-2"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label("Typ", className="mt-2"),
                                    dcc.Dropdown(id='type-dropdown', options=TYPE_OPTIONS, value='Talk', clearable=False) # type: ignore
                                ], width=6),
                                dbc.Col([
                                    dbc.Label("Sprache", className="mt-2"),
                                    dcc.Dropdown(id='lang-dropdown', options=LANG_OPTIONS, value='Deutsch', clearable=False) # type: ignore
                                ], width=6)
                            ]),
                            dbc.Label("Titel", className="mt-3"),
                            dbc.Input(id='title-input', type='text', value='', placeholder='Titel des Beitrags'),
                            dbc.Label("Beschreibung", className="mt-2"),
                            dbc.Textarea(id='desc-input', style={'height': 80}, placeholder='Kurze Beschreibung'),
                            dbc.Label("Name / Orga", className="mt-3"),
                            dbc.Input(id='name-input', type='text', value='', placeholder='Name (optional: Organisation)'),
                            html.Hr(className="my-4"),
                            dbc.Row([
                                dbc.Col(dbc.Button("Abbrechen", id='btn-cancel', color="secondary", outline=True, className="w-100"), width=6),
                                dbc.Col(dbc.Button("Speichern", id='submit-btn', color="success", className="w-100"), width=6)
                            ]),
                            html.Div(id='status-msg', className="mt-3 text-center fw-bold")
                        ], width=12, lg=8)
                    ])
                ])
            ], className="mb-4 shadow border-0"),
            id="collapse-form-container",
            is_open=False
        )
    ], width=12, lg=10), justify="center")
