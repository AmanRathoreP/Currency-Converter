import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.config import ConfigParser
from kivymd.app import MDApp

kivy_design_files = ["settings_screen"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", kv_file + ".kv"))

class settingsScreen(Screen):
    def __init__(self, config: ConfigParser, **kwargs):
        super(settingsScreen, self).__init__(**kwargs)
        self.config = config
    
    def toggle_theme(self):
        self.config["look and feel"]["theme"] = "Dark" if self.config["look and feel"]["theme"] == "Light" else "Light"
        self.config.write()
        MDApp.get_running_app().apply_settings_to_app()

if __name__ == "__main__":
    class __test_temp_app(MDApp):  
        def build(self):
            return settingsScreen(ConfigParser())
    __test_temp_app().run()