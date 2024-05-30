from src.settings.elements.common.combobox_template import comboBox

import os
import json

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivymd.uix.screen import MDScreen

kivy_design_files = ["sub_settings_template"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", "elements", "common", kv_file + ".kv"))

class subSettingsTemplate(MDScreen):
    sub_settings_list = []
    def __init__(self, config: ConfigParser, setting_section_name:str, **kwargs):
        MDScreen.__init__(self, **kwargs)
        self.config = config
        self.setting_section_name = setting_section_name
        self.name = setting_section_name

        with open("available_options_for_each_setting.json", 'r') as json_file:
            self.setting_properties = json.load(json_file)[setting_section_name]
    
        self.ids.top_bar.title = self.setting_properties["title"]

    def clear_all_available_settings(self):
        self.ids.sub_settings.clear_widgets()
    
    def add_combo_box(self, setting_name_in_settings_properties_json_file, **kwargs):
        combo_box = comboBox(self.config,
                             self.setting_section_name,
                             self.setting_properties["data"][setting_name_in_settings_properties_json_file]["config file's setting name"],
                             self.setting_properties["data"][setting_name_in_settings_properties_json_file]["options"],
                             self.setting_properties["data"][setting_name_in_settings_properties_json_file]["title"],
                             **kwargs)
        self.sub_settings_list.append(combo_box)
        self.ids.sub_settings.add_widget(combo_box)

    def highlight_setting(self, section_name: str, setting_name: str):
        for sub_setting in self.sub_settings_list:
            if (sub_setting.section_name == section_name) and (sub_setting.setting_name == setting_name):
                sub_setting.animate_for_easy_navigation()

