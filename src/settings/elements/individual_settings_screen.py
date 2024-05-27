import os

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen

kivy_design_files = ["individual_settings_screen"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", "elements", kv_file + ".kv"))

class settingsIndividualScreen(MDScreen):
    def __init__(self, config: ConfigParser, title = "No title provided", **kwargs):
        super(settingsIndividualScreen, self).__init__(**kwargs)
        self.config = config
        self.ids.title.text=title

if __name__ == "__main__":
    from kivymd.app import MDApp
    class __test_temp_app(MDApp):  
        def build(self):
            return settingsIndividualScreen(ConfigParser(), title="Heading", name = "bla bla bal")
    __test_temp_app().run()