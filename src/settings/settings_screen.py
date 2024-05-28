from src.settings.elements.setting_item import SettingsItem

import os

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

kivy_design_files = ["settings_screen"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", kv_file + ".kv"))

class settingsDefaultScreen(MDScreen):
    def __init__(self, config: ConfigParser, **kwargs):
        super(settingsDefaultScreen, self).__init__(**kwargs)
        self.config = config
