if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

    from src.settings.elements.sub_settings.currency_converter import ExchangeRates
else:
    from src.settings.elements.sub_settings.currency_converter import ExchangeRates

import os
from vendor.format_currency.src.format_currency.format import format_currency

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
    er:ExchangeRates = None

    def __init__(self, config: ConfigParser, **kwargs):
        super(homeScreen, self).__init__(**kwargs)
        self.config = config
        self.er = ExchangeRates("exchange_rates.json", True)

        value_to_convert = 50
        if __name__ == "__main__":
            currencies_to_add = ['INR', 'JPY', 'EUR', 'USD']
        else:
            currencies_to_add = self.config["currencies to include"]["active-non-custom-currencies"].replace('\'', '').replace(' ', '')[1:-1].split(',')
        currencies_to_add.sort()
        for currency in currencies_to_add:
            __converted_value = round(self.er.convert_currency(value_to_convert, "USD".lower(), currency.lower()), 2)
            self.__add_currency(currency, "assets/icons/work-in-progress.png", f"{format_currency(__converted_value, currency_code = currency)}")
    
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