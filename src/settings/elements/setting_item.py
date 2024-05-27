# from src.settings.elements.settings_panel import SettingsPanel

import os

from kivy.lang import Builder

kivy_design_files = ["setting_item"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", "elements", kv_file + ".kv"))

class SettingsItem():
    pass
