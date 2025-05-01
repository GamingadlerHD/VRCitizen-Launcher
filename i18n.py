import json
import os

_current_lang = 'it'
_translations = {}

def set_language(lang_code):
    global _current_lang, _translations
    _current_lang = lang_code
    path = os.path.join(os.path.dirname(__file__), 'locales', f'{lang_code}.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            _translations = json.load(f)
    except FileNotFoundError:
        print(f"[i18n] Warning: Language file '{lang_code}.json' not found. Falling back to empty.")
        _translations = {}

def translate(tag):
    set_language(_current_lang)  # Ensure the language is set before translation
    return _translations.get(tag, f"[{tag}]")

