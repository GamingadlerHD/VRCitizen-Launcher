import json
import os

_current_lang = 'it'
_translations = {}

def load_translations_from_file(lang_code):
    path = os.path.join('locales', f'{lang_code}.json')
    print(f"[i18n] Loading language file: {path}")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {k.lower(): v for k, v in data.items()}
    except FileNotFoundError:
        print(f"[i18n] Warning: Language file '{lang_code}.json' not found. Falling back to empty.")
        return {}

def set_language(lang_code):
    global _current_lang, _translations # pylint: disable=global-statement
    _current_lang = lang_code
    _translations = load_translations_from_file(lang_code)

def translate(tag: str, lang_code=None):
    if lang_code:
        other_translations = load_translations_from_file(lang_code)
        return other_translations.get(tag, f"[{tag}]")
    return _translations.get(tag.lower(), f"[{tag}]")
