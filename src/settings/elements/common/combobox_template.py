import os

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivymd.uix.boxlayout import MDBoxLayout

kivy_design_files = ["combobox_template"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", "elements", "common", kv_file + ".kv"))

class comboBox(MDBoxLayout):
    def __init__(self, config: ConfigParser, section_name, setting_name, options, title, **kwargs):
        MDBoxLayout.__init__(self, **kwargs)
        self.config = config
