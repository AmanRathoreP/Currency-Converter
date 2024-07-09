if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

    from src.settings.elements.sub_settings.currency_converter import ExchangeRates
else:
    from src.settings.elements.sub_settings.currency_converter import ExchangeRates

import os
from sympy import sympify


from vendor.format_currency.src.format_currency.format import format_currency

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.config import ConfigParser
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton

kivy_design_files = ["home", "individual_currency_item", "input_keyboard"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.dirname(os.path.realpath( __file__ )), kv_file + ".kv"))

class homeScreen(Screen):
    er:ExchangeRates = None
    added_currencies_holder = []

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
            #todo https://github.com/hampusborgos/country-flags
            self.__add_currency(currency, "assets/icons/work-in-progress.png", f"{format_currency(__converted_value, currency_code = currency)}")
    
        self.add_widget(InputKeyboard(self.on_typed_string_change))
    
    def __add_currency(self, name:str, icon:str, text_to_show:str):
        self.added_currencies_holder.append(IndividualCurrencyItem(name, icon, text_to_show))
        self.ids.currencies_panel.add_widget(self.added_currencies_holder[-1])

    def on_typed_string_change(self, string:str):
        main_app_bar_text = string
        try:
            secondary_app_bar_text = InputKeyboard.evaluate_expression(string)
        except:
            secondary_app_bar_text = "CHECK INPUT"
        
        for currency_holder in self.added_currencies_holder:
            try:
                converted_value_str = format_currency(round(self.er.convert_currency(float(secondary_app_bar_text), "USD".lower(), currency_holder.name.lower()), 2), currency_code = currency_holder.name.lower())
            except:
                converted_value_str: str = "."
            currency_holder.update_currency_value_to_show(converted_value_str)
        self.ids.main_app_bar.title = main_app_bar_text
        self.ids.secondary_app_bar.title = ("= " + secondary_app_bar_text) if "CHECK INPUT" != secondary_app_bar_text else "CHECK INPUT"

class IndividualCurrencyItem(MDCard):
    def __init__(self, name:str, icon:str, text_to_show:str):
        super(IndividualCurrencyItem, self).__init__()
        
        self.icon = icon
        self.text = text_to_show
        self.name = name
    
    def update_currency_value_to_show(self, text_to_show:str):
        self.ids.currency_text.text = text_to_show

class InputKeyboard(MDCard):
    typed_string:str = ''
    buttons_to_add_text = ['7', '8', '9', 'x', '4', '5', '6', '/', '1', '2', '3', '-', '.', '0', "000", '+', '(', "DEL", "AC", ')']

    def __init__(self, update_callback):
        super(InputKeyboard, self).__init__()
        self.update_callback = update_callback

        for btn_text in self.buttons_to_add_text:
            btn = MDRaisedButton(text = btn_text, elevation = 0.5)
            btn.on_release = lambda bt=btn_text: self.button_press(bt)
            self.ids.buttons_grid.add_widget(btn)
        
    
    def button_press(self, button_text:str):
        #todo constrain inputs as a whole to resolve ambiguities
        if button_text == "AC":
            self.typed_string = ''
        elif button_text == "DEL":
            self.typed_string = '' if len(self.typed_string) == 0 else self.typed_string[:-1] 
        else:
            self.typed_string += button_text

        if self.update_callback:
                self.update_callback(self.typed_string)

    @staticmethod
    def evaluate_expression(expression:str) -> str:
        expression = expression.replace('X', '*').replace('x', '*')
        expr = sympify(expression)
        result = expr.evalf()
        return str(result) if str(result) != "zoo" else "NaN"

if __name__ == "__main__":
    from kivymd.app import MDApp
    class __test_temp_app(MDApp):  
        def build(self):
            return homeScreen(ConfigParser())
    __test_temp_app().run()