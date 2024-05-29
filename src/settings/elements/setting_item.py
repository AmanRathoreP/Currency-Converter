from src.settings.elements.common.search_backend import searchBackend

import os

from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivy.uix.behaviors import ButtonBehavior

kivy_design_files = ["setting_item"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", "elements", kv_file + ".kv"))

class SettingsItem(MDCard, ButtonBehavior, searchBackend):
    def __init__(self, icon: str, text: str, subtext: str, settings_section_name: str, alternate_searchable_string: list[str] = []):
        super(SettingsItem, self).__init__()
        searchBackend.__init__(self, settings_section_name, alternate_searchable_string)
        
        self.icon = icon
        self.text = text
        self.subtext = subtext
