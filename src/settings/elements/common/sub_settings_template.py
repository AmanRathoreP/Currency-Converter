from src.settings.elements.common.combobox_template import comboBox

import os

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivymd.uix.screen import MDScreen

kivy_design_files = ["sub_settings_template"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", "elements", "common", kv_file + ".kv"))

class subSettingsTemplate(MDScreen):
    def __init__(self, config: ConfigParser, title = "No title provided", **kwargs):
        MDScreen.__init__(self, **kwargs)
        self.config = config
        self.ids.top_bar.title = title
    
    def clear_all_available_settings(self):
        self.ids.sub_settings.clear_widgets()
    
    def add_combo_box(self, section_name, setting_name, options, title):
        self.ids.sub_settings.add_widget(comboBox(self.config, section_name, setting_name, options, title))
