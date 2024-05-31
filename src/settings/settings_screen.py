from src.settings.elements.setting_item import SettingsItem

import os

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast

kivy_design_files = ["settings_screen"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", kv_file + ".kv"))

class settingsDefaultScreen(MDScreen):
    def __init__(self, config: ConfigParser, **kwargs):
        super(settingsDefaultScreen, self).__init__(**kwargs)
        self.config = config

        self.individual_settings_row = {}
        for individual_settings_row_section_name in ["currencies to include", "format numbers' looks", "look and feel", "sync", "about"]:
            self.individual_settings_row[individual_settings_row_section_name] = SettingsItem(individual_settings_row_section_name)
            self.ids.sub_settings_list.add_widget(self.individual_settings_row[individual_settings_row_section_name])

        self.config = config

    def on_search_field_text_change(self, text):
        if text == ' ' or text == '':
            self.ids.search_field.text = ''
            self.ids.sub_settings_list.clear_widgets()
            for setting_item_str in self.individual_settings_row:
                self.individual_settings_row[setting_item_str].toggle_search_view()
                self.ids.sub_settings_list.add_widget(self.individual_settings_row[setting_item_str])

            return
        
        search_results = {}
        for child_widget in self.ids.sub_settings_list.children:
            res = child_widget.get_search_results(text, 75, 4)
            if res != -1:
                search_results[child_widget.settings_section_name] = child_widget.get_search_results(text, 75, 4)
        
        self.ids.sub_settings_list.clear_widgets()
        for setting_item_str in self.individual_settings_row:
            if setting_item_str in search_results:
                strings_list_to_send = []
                self.ids.sub_settings_list.add_widget(self.individual_settings_row[setting_item_str])
                for info_tuple in search_results[setting_item_str]:
                    strings_list_to_send.append(info_tuple[1])
                self.individual_settings_row[setting_item_str].toggle_search_view(strings_list_to_send, info_tuple[0])
                continue
            self.individual_settings_row[setting_item_str].toggle_search_view()
            self.ids.sub_settings_list.remove_widget(self.individual_settings_row[setting_item_str])

        if len(search_results) == 0:
            toast("No settings found!")
            for setting_item_str in self.individual_settings_row:
                self.ids.sub_settings_list.add_widget(self.individual_settings_row[setting_item_str])