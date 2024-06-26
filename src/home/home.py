import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.config import ConfigParser

kivy_design_files = ["home"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.dirname(os.path.realpath( __file__ )), kv_file + ".kv"))

class homeScreen(Screen):
    def __init__(self, config: ConfigParser, **kwargs):
        super(homeScreen, self).__init__(**kwargs)
        self.config = config

if __name__ == "__main__":
    from kivymd.app import MDApp
    class __test_temp_app(MDApp):  
        def build(self):
            return homeScreen(ConfigParser())
    __test_temp_app().run()