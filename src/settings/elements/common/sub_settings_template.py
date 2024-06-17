from src.settings.elements.common.combobox_template import comboBox
from src.settings.elements.common.info_label_template import infoLabel

import os
import json

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivy.resources import resource_find
from kivymd.uix.screen import MDScreen

kivy_design_files = ["sub_settings_template"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.dirname(os.path.realpath( __file__ )), kv_file + ".kv"))

class subSettingsTemplate(MDScreen):
    sub_settings_list = []
    def __init__(self, config: ConfigParser, setting_section_name:str, **kwargs):
        MDScreen.__init__(self, **kwargs)
        self.config = config
        self.setting_section_name = setting_section_name
        self.name = setting_section_name

        with open(resource_find("available_options_for_each_setting.json"), 'r') as json_file:
            self.setting_properties = json.load(json_file)[setting_section_name]
    
        self.ids.top_bar.title = self.setting_properties["title"]

    def clear_all_available_settings(self):
        self.ids.sub_settings.clear_widgets()
        return self
    
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

    def add_info_label(self, setting_name_in_settings_properties_json_file, **kwargs):
        info_label = infoLabel(None, None, None,
                             self.setting_properties["data"][setting_name_in_settings_properties_json_file]["title"],
                             self.setting_properties["data"][setting_name_in_settings_properties_json_file]["description"],
                             **kwargs)
        self.sub_settings_list.append(info_label)
        self.ids.sub_settings.add_widget(info_label)

        return self

    def add_all_possible_settings(self, clear_all_the_available_settings=True, **kwargs) -> tuple:
        """
        Adds all the settings which are available in the JSON `self.setting_properties["data"]`,
        and whose template is also available.

        Args:
        - clear_all_the_available_settings (bool): Clears previous setting(s) before adding any setting(s). Default is True.
        - **kwargs: Additional keyword arguments passed to individual setting addition methods.

        Returns:
        - Tuple containing (self, settings_not_added):
            - self: The instance of the class.
            - settings_not_added (list): List of setting names which could not be added due to unsupported types or other issues.
        """
        
        if clear_all_the_available_settings:
            self.clear_all_available_settings()

        settings_not_added = []
        for setting_name_in_settings_properties_json_file in self.setting_properties["data"]:
            if self.setting_properties["data"][setting_name_in_settings_properties_json_file]["type"] == "combo box":
                self.add_combo_box(setting_name_in_settings_properties_json_file, **kwargs)
            elif self.setting_properties["data"][setting_name_in_settings_properties_json_file]["type"] == "info label":
                self.add_info_label(setting_name_in_settings_properties_json_file, **kwargs)
            else:
                settings_not_added.append(setting_name_in_settings_properties_json_file)
        
        return self, settings_not_added

