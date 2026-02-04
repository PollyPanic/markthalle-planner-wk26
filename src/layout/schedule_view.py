from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from src.index import manager
from src.config import TARGET_COLUMNS

def calculate_end_time(start_dt, duration_str):
    try:
        dur_parts = duration_str.split(':')
        duration = timedelta(hours=int(dur_parts[0]), minutes=int(dur_parts[1]))
        end_dt = start_dt + duration
        return end_dt.strftime('%H:%M')
    except:
        return "??"

def create_event_card(event):
    guid = event['guid']
    start_dt = datetime.fromisoformat(event['date'])
    end_time_str = calculate_end_time(start_dt, event['duration'])
    time_str = f"{start_dt.strftime('%H:%M')} - {end_time_str}"
    
    evt_type_raw = event.get('type', 'talk')
    evt_type = evt_type_raw.capitalize()
    
    person_names = ", ".join([p.get('public_name', p.get('name', '???')) for p in event.get('persons', [])])

    type_class = f"event-type-{evt_type_raw}"
    border_class = f"border-type-{evt_type_raw}"

    real_room_name = event.get('room', '')
    room_element = None
    if real_room_name and real_room_name != 'OTHER':
        room_element = html.Span(
            [html.I(className="bi bi-geo-alt-fill me-1"), real_room_name], 
            className="small text-muted fw-bold align-middle ms-2" 
        )

    return dbc.Card([
        dbc.CardBody([
            

            html.Div([

                html.Div([
                    html.Span(time_str, className="badge bg-light text-dark border me-1 align-middle"),
                    html.Span(evt_type, className=f"badge {type_class} align-middle"),
                    room_element 
                ], className="d-inline-block"), 

                dbc.Button(
                    html.I(className="bi bi-pencil-square"),
                    id={'type': 'edit-btn', 'index': guid},
                    color="link",
                    size="sm",
                    className="p-0 text-muted align-top ms-2"
                )
            ], className="d-flex justify-content-between align-items-start mb-2"),

            html.H5(event['title'], className="card-title fw-bold mb-1"),

            dbc.Button(
                "▼ Details",
                id={'type': 'card-toggler', 'index': guid},
                color="link",
                size="sm",
                className="p-0 text-decoration-none text-secondary mt-1",
                style={"fontSize": "0.85rem", "boxShadow": "none"}
            ),

            dbc.Collapse([
                html.Hr(className="my-2"),
                
                html.Div([
                    html.I(className="bi bi-person-fill me-2"),
                    html.Span(person_names, className="fw-bold")
                ], className="mb-2 text-dark"),
                
                html.P(event.get('description', ''), className="card-text small text-secondary", 
                       style={'whiteSpace': 'pre-line'}),
                       
            ], id={'type': 'card-collapse', 'index': guid}, is_open=False),
        ])
    ], className=f"mb-3 shadow-sm border-top-0 border-end-0 border-bottom-0 border-start border-4 {border_class}")

def build_schedule_view():
    data = manager.reload_data()
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
            events.sort(key=lambda x: (x['date'], x.get('title', '').lower()))
            
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
                column_content.append(create_event_card(event))

            room_columns.append(dbc.Col(column_content, width=12, lg=col_width, className="px-2 border-end"))

        tabs.append(dbc.Tab(dbc.Row(room_columns, className="g-0 pt-3"), label=tab_label, tab_id=day['date']))

    return dbc.Tabs(tabs, active_tab=days[0]['date'], className="nav-fill bg-white shadow-sm rounded")
