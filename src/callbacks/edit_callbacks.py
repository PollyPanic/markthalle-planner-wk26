from dash import callback, Input, Output, no_update, ctx, ALL
from src.index import app, manager
from src.config import TYPE_INTERNAL_TO_DISPLAY, LANG_INTERNAL_TO_DISPLAY

@callback(
    Output('edit-modal', 'is_open'),
    Output('edit-guid-store', 'data'),
    Output('edit-room-dropdown', 'value'),
    Output('edit-other-room-input', 'value'),
    Output('edit-time-dropdown', 'value'),
    Output('edit-duration-input', 'value'),
    Output('edit-type-dropdown', 'value'),
    Output('edit-lang-dropdown', 'value'),
    Output('edit-title-input', 'value'),
    Output('edit-desc-input', 'value'),
    Output('edit-name-input', 'value'),

    Input({'type': 'edit-btn', 'index': ALL}, 'n_clicks'),
    Input('btn-edit-cancel', 'n_clicks'),
    Input('op-success-signal', 'data'),
    prevent_initial_call=True
)
def toggle_edit_modal(n_clicks_list, cancel, success_signal):
    triggered_ids = [t['prop_id'] for t in ctx.triggered]
    is_cancel = any('btn-edit-cancel' in tid for tid in triggered_ids)
    is_success = any('op-success-signal' in tid for tid in triggered_ids)

    if is_cancel or is_success:
        return False, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

    trigger_id = ctx.triggered_id
    if isinstance(trigger_id, dict) and trigger_id['type'] == 'edit-btn':
        guid = trigger_id['index']
        event = manager.get_event_by_guid(guid)
        if not event:
            return False, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

        e_type = TYPE_INTERNAL_TO_DISPLAY.get(event.get('type'), 'Talk')
        e_lang = LANG_INTERNAL_TO_DISPLAY.get(event.get('language'), 'Deutsch')
        is_std_room = event['room'] == 'SoS-Kubus'
        room_dd = 'SoS-Kubus' if is_std_room else 'OTHER'
        room_txt = "SoS-Kubus" if is_std_room else event['room']

        return True, guid, room_dd, room_txt, event['date'], event['duration'], e_type, e_lang, event['title'], event['description'], event['persons'][0]['name']

    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update


@callback(
    Output('confirm-save-modal', 'is_open'),
    Output('confirm-delete-modal', 'is_open'),
    Input('btn-save-init', 'n_clicks'),
    Input('btn-delete-init', 'n_clicks'),
    Input('btn-confirm-save-no', 'n_clicks'),
    Input('btn-confirm-save-yes', 'n_clicks'),
    Input('btn-confirm-delete-no', 'n_clicks'),
    Input('btn-confirm-delete-yes', 'n_clicks'),
    prevent_initial_call=True
)
def handle_confirmations(save_init, del_init, save_no, save_yes, del_no, del_yes):
    trigger = ctx.triggered_id
    if trigger == 'btn-save-init':
        return True, False
    if trigger == 'btn-delete-init':
        return False, True
    return False, False
