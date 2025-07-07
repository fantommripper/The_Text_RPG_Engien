import json5

class Localization:
    def __init__(self):
        self.strings = None

    def set_language(self, lang_code: str):
        with open(f"locales/{lang_code}.json5", "r", encoding="utf-8") as file:
            self.strings = json5.load(file)

    def t(self, key):
        if self.strings is None:
            raise ValueError("Localization strings not loaded. Please check the language code or file path.")
        return self.strings.get(key, f"[{key}]")

loc = Localization()