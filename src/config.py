import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JSON_FILE = os.path.join(BASE_DIR, 'data', 'schedule.json')
SLIDES_JSON_FILE = os.path.join(BASE_DIR, 'data', 'slides.json')
APP_PATH = '/e_projekte/markthalle-winterkongress/'
LOGO_FILENAME = 'logo_kongress.svg'

TYPE_DISPLAY_TO_INTERNAL = {
    "Talk": "talk",
    "Workshop": "workshop",
    "Hands-On": "hands-on",
    "Diskussion": "discussion",
    "Treffen": "meeting",
    "Game": "game",
    "Ausstellung": "exhibition",
    "Infostand": "infobooth",
    "Anderes": "other"
}

TYPE_INTERNAL_TO_DISPLAY = {
    "talk": "Talk",
    "workshop": "Workshop",
    "hands-on": "Hands-On",
    "discussion": "Diskussion",
    "meeting": "Treffen",
    "game": "Game",
    "exhibition": "Ausstellung",
    "infobooth": "Infostand",
    "other": "Anderes"
}

LANG_DISPLAY_TO_INTERNAL = {
    "Deutsch": "de",
    "English": "en",
    "Français": "fr"
}

LANG_INTERNAL_TO_DISPLAY = {
    "de": "Deutsch",
    "en": "English",
    "fr": "Français"
}

TYPE_OPTIONS = [
    {'label': 'Talk', 'value': 'Talk'},
    {'label': 'Workshop', 'value': 'Workshop'},
    {'label': 'Hands-On', 'value': 'Hands-On'},
    {'label': 'Diskussion', 'value': 'Diskussion'},
    {'label': 'Treffen', 'value': 'Treffen'},
    {'label': 'Game', 'value': 'Game'},
    {'label': 'Ausstellung', 'value': 'Ausstellung'},
    {'label': 'Infostand', 'value': 'Infostand'},
    {'label': 'Anderes', 'value': 'Anderes'}
]

LANG_OPTIONS = [
    {'label': 'Deutsch', 'value': 'Deutsch'},
    {'label': 'English', 'value': 'English'},
    {'label': 'Français', 'value': 'Français'},
    {'label': 'n/a', 'value': 'n/a'}
]

ROOM_OPTIONS = [
    {'label': 'SoS-Kubus', 'value': 'SoS-Kubus'},
    {'label': 'Markthalle (anderer Ort)', 'value': 'OTHER'}
]

TARGET_COLUMNS = ['SoS-Kubus', 'Markthalle']
