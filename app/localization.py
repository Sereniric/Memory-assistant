import json
from pathlib import Path


_TRANSLATIONS = {}


def _load_translations():
    if _TRANSLATIONS:
        return _TRANSLATIONS

    base_dir = Path(__file__).resolve().parent.parent
    translations_dir = base_dir / "translations"

    for code in ("en", "as"):
        file_path = translations_dir / f"{code}.json"
        with file_path.open("r", encoding="utf-8") as handle:
            _TRANSLATIONS[code] = json.load(handle)

    return _TRANSLATIONS


def get_active_language(language_data=None):
    if isinstance(language_data, dict):
        lang = language_data.get("lang") or language_data.get("language") or "as"
    elif isinstance(language_data, str):
        lang = language_data
    else:
        lang = "as"

    if lang not in {"en", "as"}:
        lang = "as"
    return lang


def translate_text(key, language=None):
    translations = _load_translations()
    lang = get_active_language(language)

    if key in translations.get(lang, {}):
        return translations[lang][key]

    if key in translations.get("en", {}):
        return translations["en"][key]

    return key
