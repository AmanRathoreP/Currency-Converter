import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.config import ConfigParser
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard

kivy_design_files = ["home", "individual_currency_item"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.dirname(os.path.realpath( __file__ )), kv_file + ".kv"))

class homeScreen(Screen):
    def __init__(self, config: ConfigParser, **kwargs):
        super(homeScreen, self).__init__(**kwargs)
        self.config = config

        self.__add_currency("INR", "assets/icons/work-in-progress.png", "4,54,871.54 rupees")
    
    def __add_currency(self, name:str, icon:str, text_to_show:str):
        self.ids.currencies_panel.add_widget(IndividualCurrencyItem(name, icon, text_to_show))

class IndividualCurrencyItem(MDCard):
    def __init__(self, name:str, icon:str, text_to_show:str):
        super(IndividualCurrencyItem, self).__init__()
        
        self.icon = icon
        self.text = text_to_show
        self.name = name

if __name__ == "__main__":
    from kivymd.app import MDApp
    class __test_temp_app(MDApp):  
        def build(self):
            return homeScreen(ConfigParser())
    __test_temp_app().run()