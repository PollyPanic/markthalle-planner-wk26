from dash import callback, Input, Output, State, no_update, ctx
from datetime import datetime
from src.index import app, manager
from src.layout.schedule_view import build_schedule_view

@callback(
    Output('schedule-container', 'children'),
    Output('status-msg', 'children'),
    Output('collapse-form-container', 'is_open'),
    Output('title-input', 'value'),
    Output('desc-input', 'value'),
    Output('op-success-signal', 'data'),

    Input('btn-toggle-form', 'n_clicks'),
    Input('submit-btn', 'n_clicks'),
    Input('btn-cancel', 'n_clicks'),
    Input('btn-confirm-save-yes', 'n_clicks'),
    Input('btn-confirm-delete-yes', 'n_clicks'),

    State('collapse-form-container', 'is_open'),
    State('room-dropdown', 'value'),
    State('other-room-input', 'value'),
    State('time-dropdown', 'value'),
    State('duration-input', 'value'),
    State('title-input', 'value'),
    State('desc-input', 'value'),
    State('name-input', 'value'),
    State('type-dropdown', 'value'),
    State('lang-dropdown', 'value'),
    State('edit-guid-store', 'data'),
    State('edit-room-dropdown', 'value'),
    State('edit-other-room-input', 'value'),
    State('edit-time-dropdown', 'value'),
    State('edit-duration-input', 'value'),
    State('edit-type-dropdown', 'value'),
    State('edit-lang-dropdown', 'value'),
    State('edit-title-input', 'value'),
    State('edit-desc-input', 'value'),
    State('edit-name-input', 'value'),

    prevent_initial_call=True
)
def manage_data(btn_open, btn_save, btn_cancel, confirm_save, confirm_delete,
                is_open,
                room_s, room_t, time, dur, title, desc, name, typ, lang,
                guid, e_room_s, e_room_t, e_time, e_dur, e_typ, e_lang, e_title, e_desc, e_name):
    trigger = ctx.triggered_id
    success_signal = {'ts': datetime.now().timestamp()}

    if trigger == 'btn-toggle-form':
        if not is_open:
            return no_update, "", True, "", "", no_update
        else:
            return no_update, "", False, no_update, no_update, no_update

    if trigger == 'btn-cancel':
        return no_update, "", False, "", "", no_update

    if trigger == 'submit-btn':
        if not title or not name or not time:
            return no_update, "Erforderliche Felder: Titel, Name, Zeit", True, no_update, no_update, no_update
        room = room_t if room_s == 'OTHER' and room_t else room_s

        if room == 'SoS-Kubus':
            conflict_result = manager.check_time_conflict(time, dur, room)
            if conflict_result['conflict']:
                conflicts = conflict_result['conflicting_events']
                conflict_info = ", ".join([f"'{c['title']}' ({c['start']}-{c['end']})" for c in conflicts])
                return no_update, f"Bitte eine andere Zeit wählen - Raum bereits belegt: {conflict_info}", True, no_update, no_update, no_update

        if manager.update_event(None, title, desc, name, time, dur, room, typ, lang):
            return build_schedule_view(), "", False, "", "", success_signal
        return no_update, "AAAAaaaaaaaah...Fehler! >.<", True, no_update, no_update, no_update

    if trigger == 'btn-confirm-save-yes':
        room = e_room_t if e_room_s == 'OTHER' and e_room_t else e_room_s

        if room == 'SoS-Kubus':
            conflict_result = manager.check_time_conflict(e_time, e_dur, room, exclude_guid=guid)
            if conflict_result['conflict']:
                conflicts = conflict_result['conflicting_events']
                conflict_info = ", ".join([f"'{c['title']}' ({c['start']}-{c['end']})" for c in conflicts])
                return no_update, f"Bitte eine andere Zeit wählen - Raum bereits belegt: {conflict_info}", False, no_update, no_update, no_update

        manager.update_event(guid, e_title, e_desc, e_name, e_time, e_dur, room, e_typ, e_lang)
        return build_schedule_view(), "", False, no_update, no_update, success_signal

    if trigger == 'btn-confirm-delete-yes':
        manager.delete_event(guid)
        return build_schedule_view(), "", False, no_update, no_update, success_signal

    return no_update, no_update, is_open, no_update, no_update, no_update
