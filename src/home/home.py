from src.settings.elements.sub_settings.currency_converter import ExchangeRates

import os
from sympy import sympify
import json

from vendor.format_currency.src.format_currency.format import format_currency

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.config import ConfigParser
from kivy.metrics import dp
from kivy.resources import resource_find
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
        self.er = ExchangeRates(resource_find("exchange_rates.json"), True)

        self.__load_self_configuration_data()

        with open(resource_find(os.path.join('.', "vendor", "countries_flag", "currency_code_to_flag.json")), 'r', encoding = "utf-8") as currency_code_to_flag_json_file:
            self.currency_code_to_flag_json_data = json.load(currency_code_to_flag_json_file)
            print(self.currency_code_to_flag_json_data["USD"])

        currencies_to_add = self.config["currencies to include"]["active-non-custom-currencies"].replace('\'', '').replace(' ', '')[1:-1].split(',')
        currencies_to_add.sort()
        for currency in currencies_to_add:
            if currency.upper() in self.currency_code_to_flag_json_data:
                self.__add_currency(currency, f"vendor/countries_flag/png/{self.currency_code_to_flag_json_data[currency.upper()].lower()}.png", '.')
            else:
                self.__add_currency(currency, "assets/icons/work-in-progress.png", '.')
    
        self.add_widget(InputKeyboard(self.on_typed_string_change, str(self.config["currencies to include"]["currently-typed-currency-value"])))
        self.on_typed_string_change(str(self.config["currencies to include"]["currently-typed-currency-value"]))
    
    def __add_currency(self, name:str, icon:str, text_to_show:str):
        self.added_currencies_holder.append(IndividualCurrencyItem(name, icon, text_to_show))
        self.ids.currencies_panel.add_widget(self.added_currencies_holder[-1])

    def on_typed_string_change(self, string:str):
        main_app_bar_text = string
        self.config["currencies to include"]["currently-typed-currency-value"] = string
        self.config.write()
        try:
            secondary_app_bar_text = InputKeyboard.evaluate_expression(string)
        except:
            secondary_app_bar_text = "CHECK INPUT"
        
        for currency_holder in self.added_currencies_holder:
            try:
                converted_value_str = format_currency(
                    currency_code = currency_holder.name.lower(),
                    number_format_system = self.__number_format_system,
                    smart_number_formatting = self.__smart_formatting,
                    place_currency_symbol_at_end = True,
                    decimal_places = self.__decimal_places_to_show,
                    number = round(
                        self.er.convert_currency(
                            float(secondary_app_bar_text), 
                            self.config["currencies to include"]["currently-selected-currency"].lower(),
                            currency_holder.name.lower()
                            ),
                        self.__decimal_places_to_show
                        ),
                    )
            except:
                converted_value_str: str = "."
            currency_holder.update_currency_value_to_show(converted_value_str)
        self.ids.main_app_bar.title = main_app_bar_text
        self.ids.secondary_app_bar.title = ("= " + str(round(float(secondary_app_bar_text), self.__decimal_places_to_show))) if "CHECK INPUT" != secondary_app_bar_text else "CHECK INPUT"

    def __load_self_configuration_data(self):
        self.__number_format_system = str(self.config["format numbers' looks"]["number-format-system"])
        self.__decimal_places_to_show = int(self.config["format numbers' looks"]["decimal-precision"])
        self.__smart_formatting = bool(self.config["format numbers' looks"]["smart-formatting"])

        if self.__number_format_system == "International Number System":
            self.__number_format_system = "global"
        elif self.__number_format_system == "Indian Number System":
            self.__number_format_system = "indian"
        elif self.__number_format_system == "Chinese Number System":
            self.__number_format_system = "chinese"
        elif self.__number_format_system == "According to Currency":
            self.__number_format_system = "auto"

class IndividualCurrencyItem(MDCard):
    def __init__(self, name:str, icon:str, text_to_show:str):
        super(IndividualCurrencyItem, self).__init__()
        
        self.icon = icon
        self.text = text_to_show
        self.name = name
    
    def update_currency_value_to_show(self, text_to_show:str):
        self.ids.currency_text.text = text_to_show
        self.ids.currency_text.font_name = resource_find("assets/fonts/custom/NotoSans (only certain characters).ttf")

class InputKeyboard(MDCard):
    typed_string:str = ''
    buttons_to_add_text = ['7', '8', '9', 'x', '4', '5', '6', '/', '1', '2', '3', '-', '.', '0', "000", '+', '(', "DEL", "AC", ')']

    def __init__(self, update_callback, typed_string:str = ''):
        super(InputKeyboard, self).__init__()
        self.update_callback = update_callback
        self.typed_string = typed_string

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
