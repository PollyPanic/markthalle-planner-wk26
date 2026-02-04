from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from src.index import manager
from src.config import TARGET_COLUMNS

def build_schedule_view():
    data = manager._load_data()
    days = data['schedule']['conference']['days']
    tabs = []

    for day in days:
        day_date = datetime.strptime(day['date'], "%Y-%m-%d")
        wochentage = {4: "Freitag", 5: "Samstag", 6: "Sonntag"}
        day_name = wochentage.get(day_date.weekday(), day_date.strftime("%A"))
        tab_label = f"{day_name}, {day_date.strftime('%d.%m.')}"

        col_width = 6
        room_columns = []

        for room_key in TARGET_COLUMNS:
            events = day['rooms'].get(room_key, [])
            events.sort(key=lambda x: x['date'])
            column_content = []
            column_content.append(
                html.H4(room_key, className="text-center mb-4 pb-2 border-bottom sticky-top bg-light pt-2",
                        style={"top": "0px", "zIndex": "10"})
            )

            if not events:
                column_content.append(
                    html.Div("Noch leer", className="text-muted text-center fst-italic p-3 border rounded bg-white")
                )

            for event in events:
                start_dt = datetime.fromisoformat(event['date'])
                dur_parts = event['duration'].split(':')
                duration = timedelta(hours=int(dur_parts[0]), minutes=int(dur_parts[1]))
                end_dt = start_dt + duration
                time_str = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
                evt_type_raw = event.get('type', 'talk')
                evt_type = evt_type_raw.capitalize()
                evt_lang = event.get('language', 'de').upper()
                real_room_name = event.get('room', '')

                type_class = f"event-type-{evt_type_raw}"
                border_class = f"border-type-{evt_type_raw}"

                location_badge = None
                if real_room_name != 'Markthalle' and real_room_name != 'OTHER':
                    location_badge = html.Div([
                        html.I(className="bi bi-geo-alt-fill me-1 text-dark"),
                        html.Span(real_room_name, className="fw-bold text-dark")
                    ], className="mb-2 border-bottom pb-1")

                card = dbc.Card([
                    dbc.CardBody([
                        location_badge,
                        html.Div([
                            html.Div([
                                html.Span(time_str, className="badge bg-light text-dark border me-1"),
                                html.Span(evt_type, className=f"badge {type_class} me-1"),
                                html.Span(evt_lang, className="badge bg-info text-white"),
                            ]),
                            dbc.Button(
                                html.I(className="bi bi-pencil-square"),
                                id={'type': 'edit-btn', 'index': event['guid']},
                                color="link",
                                size="sm",
                                className="p-0 text-muted"
                            )
                        ], className="d-flex justify-content-between align-items-start mb-2"),
                        html.H5(event['title'], className="card-title fw-bold mt-1"),
                        html.P([html.I(className="bi bi-person-fill me-1"), event['persons'][0]['name']],
                               className="text-muted small mb-2"),
                        html.P(event['description'], className="card-text small text-secondary")
                    ])
                ], className=f"mb-3 shadow-sm border-top-0 border-end-0 border-bottom-0 border-start border-4 {border_class}")
                column_content.append(card)

            room_columns.append(dbc.Col(column_content, width=12, lg=col_width, className="px-2 border-end"))

        tabs.append(dbc.Tab(dbc.Row(room_columns, className="g-0 pt-3"), label=tab_label, tab_id=day['date']))

    return dbc.Tabs(tabs, active_tab=days[0]['date'], className="nav-fill bg-white shadow-sm rounded")
