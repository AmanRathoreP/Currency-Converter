from src.settings.elements.setting_item import SettingsItem

import os

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivymd.uix.screen import MDScreen

kivy_design_files = ["settings_screen"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", kv_file + ".kv"))

class settingsDefaultScreen(MDScreen):
    def __init__(self, config: ConfigParser, **kwargs):
        super(settingsDefaultScreen, self).__init__(**kwargs)
        self.config = config

        self.ids.sub_settings_list.add_widget(SettingsItem("cash-sync", "Currency", "todo", "Currency", ["Currency", "Money"]))
        self.ids.sub_settings_list.add_widget(SettingsItem("format-text", "Format Currency Values", "todo", "Format Currency Values", ["Precision", "Format", "Numbers"]))
        self.ids.sub_settings_list.add_widget(SettingsItem("invert-colors", "Look & Feel", "todo", "look and feel", ["Look", "Feel"]))
        self.ids.sub_settings_list.add_widget(SettingsItem("sync", "Synchronisation", "todo", "Synchronisation", ["Synchronisation"]))
        self.ids.sub_settings_list.add_widget(SettingsItem("information-variant-circle", "About", "todo", "About", ["About", "Info", "Version"]))

        self.config = config

    def on_search_field_text_change(self, text):
        if text == ' ':
            self.ids.search_field.text = ''
            return
        search_result = []
        for child_widget in self.ids.sub_settings_list.children:
            res = child_widget.get_search_results(text, 75, 4)
            search_result.extend(res if res != -1 else [])
        
        print("---------------------------------------------------------------------------------------------"*5)
        for res in search_result:
            print(res)
        print("---------------------------------------------------------------------------------------------"*5)

