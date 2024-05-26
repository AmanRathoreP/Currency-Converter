import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

kivy_design_files = ["home"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "home", kv_file + ".kv"))

class homeScreen(Screen):
    pass


if __name__ == "__main__":
    class __test_temp_app(MDApp):  
        def build(self):
            return homeScreen()
    __test_temp_app().run()