import json
import uuid
import os
from datetime import datetime, timedelta

class DataManager:
    def __init__(self, json_path):
        self.json_path = json_path
        self.data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self.json_path):
            return self._create_empty_schedule()       
        with open(self.json_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return self._create_empty_schedule()

    def save_data(self):
        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def reload_data(self):
        """Reload data from file to ensure freshness"""
        self.data = self._load_data()
        return self.data

    def _create_empty_schedule(self):
        return {
            "schedule": {
                "version": "1.0",
                "conference": {
                    "acronym": "markthalle-wk26",
                    "title": "Programm Markthalle Winterkongress 2026",
                    "start": "2026-02-20",
                    "end": "2026-02-21",
                    "daysCount": 2,
                    "timeslot_duration": "00:15",
                    "days": [
                        {
                            "index": 1,
                            "date": "2026-02-20",
                            "day_start": "2026-02-20T19:00:00+01:00",
                            "day_end": "2026-02-20T22:00:00+01:00",
                            "rooms": {"SoS-Kubus": [], "Markthalle": []}
                        },
                        {
                            "index": 2,
                            "date": "2026-02-21",
                            "day_start": "2026-02-21T11:00:00+01:00",
                            "day_end": "2026-02-21T20:00:00+01:00",
                            "rooms": {"SoS-Kubus": [], "Markthalle": []}
                        }
                    ],
                    "rooms": [{"name": "SoS-Kubus", "guid": str(uuid.uuid4())}]
                }
            }
        }

    def get_time_options(self, step_minutes=15):
        options = []
        if 'schedule' not in self.data: 
             self.data = self._create_empty_schedule()
        days = self.data['schedule']['conference']['days']
        for day in days:
            try:
                fmt = "%Y-%m-%dT%H:%M:%S"
                start_clean = day['day_start'][:19]
                end_clean = day['day_end'][:19]
                current_time = datetime.strptime(start_clean, fmt)
                end_time = datetime.strptime(end_clean, fmt)
                while current_time < end_time:
                    day_name = "Fr" if current_time.weekday() == 4 else "Sa"
                    label = f"{day_name}, {current_time.strftime('%d.%m. - %H:%M')} Uhr"
                    value_iso = current_time.strftime(fmt) + "+01:00"
                    options.append({'label': label, 'value': value_iso})
                    current_time += timedelta(minutes=step_minutes)
            except Exception as e:
                continue
        return options

    def get_event_by_guid(self, guid):
        days = self.data['schedule']['conference']['days']
        for day in days:
            for room, events in day['rooms'].items():
                for event in events:
                    if event.get('guid') == guid:
                        return event
        return None

    def delete_event(self, guid):
        days = self.data['schedule']['conference']['days']
        something_deleted = False
        for day in days:
            for room_key in day['rooms']:
                original_list = day['rooms'][room_key]
                new_list = [e for e in original_list if e.get('guid') != guid]
                if len(new_list) < len(original_list):
                    day['rooms'][room_key] = new_list
                    something_deleted = True
        if something_deleted:
            self.save_data()
        return something_deleted

    def update_event(self, guid, title, description, speaker, start_time_iso, duration, room_name, event_type, language):
        lang_map = {"Deutsch": "de", "English": "en", "Français": "fr"}
        type_map = {
            "Talk": "talk", "Workshop": "workshop", "Hands-On": "hands-on",
            "Diskussion": "discussion", "Treffen": "meeting", "Game": "game", 
            "Ausstellung": "exhibition", "Infostand": "infobooth", "Anderes": "other"
        }

        event_data = {
            "guid": guid if guid else str(uuid.uuid4()),
            "id": int(datetime.now().timestamp()),
            "date": start_time_iso, 
            "start": start_time_iso.split("T")[-1][:5], 
            "duration": duration,
            "room": room_name,
            "slug": title.lower().replace(" ", "-") if title else "event",
            "url": "",
            "title": title,
            "subtitle": "",
            "track": None,
            "type": type_map.get(event_type, "other"),
            "language": lang_map.get(language, "de"),
            "abstract": description[:50] + "..." if description else "",
            "description": description,
            "persons": [{"name": speaker, "public_name": speaker, "id": 0}],
            "links": [],
            "attachments": [] 
        }
        if guid:
            self.delete_event(guid)
        return self._insert_event_into_schedule(event_data)

    def _insert_event_into_schedule(self, new_event):
        days = self.data['schedule']['conference']['days']
        event_date_str = new_event['date'].split("T")[0]
        target_day = None
        for d in days:
            if d['date'] == event_date_str:
                target_day = d
                break
        if not target_day:
            return False

        real_room_name = new_event['room']
        if real_room_name == 'SoS-Kubus':
            group_key = 'SoS-Kubus'
        else:
            group_key = 'Markthalle'
        if group_key not in target_day['rooms']:
            target_day['rooms'][group_key] = []          
        target_day['rooms'][group_key].append(new_event)
        self.save_data()
        return True

    def add_event(self, title, description, speaker, start_time_iso, duration, room_name, event_type, language):
        return self.update_event(None, title, description, speaker, start_time_iso, duration, room_name, event_type, language)

    def check_time_conflict(self, start_time_iso, duration, room_name='SoS-Kubus', exclude_guid=None):
        if room_name != 'SoS-Kubus':
            return {'conflict': False, 'conflicting_events': []}

        try:
            new_start = datetime.fromisoformat(start_time_iso)
            dur_parts = duration.split(':')
            dur_delta = timedelta(hours=int(dur_parts[0]), minutes=int(dur_parts[1]))
            new_end = new_start + dur_delta

            event_date_str = start_time_iso.split("T")[0]
            days = self.data['schedule']['conference']['days']
            target_day = None
            for d in days:
                if d['date'] == event_date_str:
                    target_day = d
                    break

            if not target_day:
                return {'conflict': False, 'conflicting_events': []}

            sos_events = target_day['rooms'].get('SoS-Kubus', [])
            conflicting_events = []

            for event in sos_events:
                if exclude_guid and event.get('guid') == exclude_guid:
                    continue

                event_start = datetime.fromisoformat(event['date'])
                event_dur_parts = event['duration'].split(':')
                event_dur_delta = timedelta(hours=int(event_dur_parts[0]), minutes=int(event_dur_parts[1]))
                event_end = event_start + event_dur_delta

                if new_start < event_end and new_end > event_start:
                    conflicting_events.append({
                        'title': event['title'],
                        'start': event_start.strftime('%H:%M'),
                        'end': event_end.strftime('%H:%M'),
                        'guid': event['guid']
                    })

            return {
                'conflict': len(conflicting_events) > 0,
                'conflicting_events': conflicting_events
            }

        except Exception as e:
            return {'conflict': False, 'conflicting_events': []}