from src.settings.elements.sub_settings.currency_converter import ExchangeRates

import os
from sympy import sympify
import json
import ast
from time import time as unix_sec
import webbrowser
from random import shuffle as rd_shuffle

from vendor.format_currency.src.format_currency.format import format_currency

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.config import ConfigParser
from kivy.metrics import dp
from kivy.resources import resource_find
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast

kivy_design_files = ["home", "individual_currency_item", "input_keyboard"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.dirname(os.path.realpath( __file__ )), kv_file + ".kv"))

class homeScreen(Screen):
    er:ExchangeRates = None
    added_currencies_holder = []
    scroll_view_previous_y_scroll_value:float = 1

    def __init__(self, config: ConfigParser, **kwargs):
        super(homeScreen, self).__init__(**kwargs)
        self.config = config
        self.special_formatting_on:bool = False
        self.__on_typed_string_change_scheduled_event = None

        self.__load_self_configuration_data()

        with open(resource_find(os.path.join('.', "vendor", "countries_flag", "currency_code_to_flag.json")), 'r', encoding = "utf-8") as currency_code_to_flag_json_file:
            self.currency_code_to_flag_json_data = json.load(currency_code_to_flag_json_file)

        currencies_to_add = ast.literal_eval(self.config["currencies to include"]["active-non-custom-currencies"])
        currencies_to_add = self.sort_currencies(currencies_to_add, self.config["currencies to include"]["sort-type"])
        for currency in currencies_to_add:
            if currency.upper() in self.currency_code_to_flag_json_data:
                self.__add_currency(currency, f"vendor/countries_flag/png/{self.currency_code_to_flag_json_data[currency.upper()].lower()}.png", '.')
            else:
                self.__add_currency(currency, "assets/icons/work-in-progress.png", '.')
    
        self.input_keyboard = InputKeyboard(
                update_callback = self.on_typed_string_change,
                decimal_places_to_show = self.__decimal_places_to_show,
                typed_string = str(self.config["currencies to include"]["currently-typed-currency-value"]),
                special_buttons = self.__special_keyboard_buttons,
                )
        self.add_widget(self.input_keyboard)
        
        self.on_typed_string_change(str(self.config["currencies to include"]["currently-typed-currency-value"]))
        self.update_convert_from_currency(self.config["currencies to include"]["currently-selected-currency"])
    
    def __add_currency(self, name:str, icon:str, text_to_show:str):
        self.added_currencies_holder.append(IndividualCurrencyItem(name, icon, text_to_show, self.update_convert_from_currency))
        self.ids.currencies_panel.add_widget(self.added_currencies_holder[-1])

    def on_typed_string_change(self, string:str, things_to_write = "actual stuff"):
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
                    smart_number_formatting = (self.__smart_formatting or "only Smart Formatting" in things_to_write) and "only Normal Formatting" not in things_to_write,
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
                if "both Smart & Normal" in things_to_write:
                    converted_value_str = ''
                    for smart_format_true_or_false in [True, False]:
                        converted_value_str += format_currency(
                            currency_code = currency_holder.name.lower(),
                            number_format_system = self.__number_format_system,
                            smart_number_formatting = smart_format_true_or_false,
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
                            ) + " i.e. \n"
                    
                    converted_value_str = converted_value_str[:-len(" i.e. \n")]
                    
            except:
                converted_value_str: str = "."
            currency_holder.update_currency_value_to_show(converted_value_str)
        self.ids.main_app_bar.title = main_app_bar_text
        self.ids.secondary_app_bar.title = ("= " + str(round(float(secondary_app_bar_text), self.__decimal_places_to_show))) if "CHECK INPUT" != secondary_app_bar_text else "CHECK INPUT"

    def __load_self_configuration_data(self):
        self.__number_format_system = str(self.config["format numbers' looks"]["number-format-system"])
        self.__decimal_places_to_show = int(self.config["format numbers' looks"]["decimal-precision"])
        self.__smart_formatting = self.config["format numbers' looks"]["smart-formatting"] == "True"
        self.__special_keyboard_buttons:dict = {k: v for k, v in (
                ast.literal_eval(s) for s in [
                    self.config["format numbers' looks"]["special-keyboard-button-1"],
                    self.config["format numbers' looks"]["special-keyboard-button-2"],
                    self.config["format numbers' looks"]["special-keyboard-button-3"],
                ]
            )
        }

        if self.__number_format_system == "International Number System":
            self.__number_format_system = "global"
        elif self.__number_format_system == "Indian Number System":
            self.__number_format_system = "indian"
        elif self.__number_format_system == "Chinese Number System":
            self.__number_format_system = "chinese"
        elif self.__number_format_system == "According to Currency":
            self.__number_format_system = "auto"

        __sync_update_period = -1 #* in seconds
        if "Hour" == self.config["sync"]["sync-period"]:
            __sync_update_period = 3600
        elif "Day" == self.config["sync"]["sync-period"]:
            __sync_update_period = 86400
        elif "Week" == self.config["sync"]["sync-period"]:
            __sync_update_period = 607800
        elif "Month" == self.config["sync"]["sync-period"]:
            __sync_update_period = 2419200 #* 7*4 days
        elif "Season" == self.config["sync"]["sync-period"]:
            __sync_update_period = 7257600 #* 7*4*3 days i.e. 3 months

        if int(self.config["sync"]["last-sync-time-unix-seconds"]) + __sync_update_period < unix_sec():
            __load_er_from_file:bool = False
        else:
            __load_er_from_file:bool = True

        if self.config["sync"]["last-sync-time-unix-seconds"] == -1:
            __load_er_from_file:bool = False
        
        self.__load_er_data(__load_er_from_file)
    
    def __load_er_data(self, __load_er_from_file:bool):
        try:
            self.er = ExchangeRates(resource_find("exchange_rates.json"), __load_er_from_file)
            Clock.schedule_once(lambda x: toast("Successfully fetched data from api", duration = 4), 0.5)
        except RuntimeError:
            self.er = ExchangeRates(resource_find("exchange_rates.json"), True)
            self._show_info_about_unable_to_fetch_from_api()

        self.config["sync"]["last-sync-time-unix-seconds"] = str(int(unix_sec()))

    def flag_icon_pressed(self):
        if self.special_formatting_on:
            self.on_typed_string_change(self.ids.main_app_bar.title,things_to_write = "actual stuff")
            self.special_formatting_on = False
            return

        if self.ids.secondary_app_bar.title == '.' or \
            "inf" in self.ids.secondary_app_bar.title or\
            self.ids.secondary_app_bar.title == "CHECK INPUT" or \
            self.config["format numbers' looks"]["flag-button-toggle-action"] == "No toggle action":
            return
        
        if "Auto" != self.config["format numbers' looks"]["flag-action-button-reset-time"]:
            if self.__on_typed_string_change_scheduled_event:
                self.__on_typed_string_change_scheduled_event.cancel()

            self.__on_typed_string_change_scheduled_event = Clock.schedule_once(
                lambda dt: (self.on_typed_string_change(self.ids.main_app_bar.title), setattr(self, 'special_formatting_on', False)),
                float(self.config["format numbers' looks"]["flag-action-button-reset-time"])
            )

        self.on_typed_string_change(string = self.ids.main_app_bar.title,
                                    things_to_write = self.config["format numbers' looks"]["flag-button-toggle-action"] + ' ' + "actual stuff")
        
        self.special_formatting_on = True

    def update_convert_from_currency(self, currency_code_to_change_to:str): #todo fix aspect ration of the icon/flag
        self.ids.secondary_app_bar.left_action_items = [[f"vendor/countries_flag/png/{self.currency_code_to_flag_json_data[currency_code_to_change_to.upper()].lower()}.png", lambda x: self.flag_icon_pressed()]]
        self.config["currencies to include"]["currently-selected-currency"] = currency_code_to_change_to.upper()
        self.config.write()
        self.on_typed_string_change(self.ids.main_app_bar.title)
        print(f"changing to {currency_code_to_change_to}")

    def deal_with_hiding_of_keyboard(self, y_scroll):
        if (y_scroll >= self.scroll_view_previous_y_scroll_value) and y_scroll != 0:
            self.input_keyboard.opacity = 1
        else:
            self.input_keyboard.opacity = 0

        self.scroll_view_previous_y_scroll_value = y_scroll

    def _show_info_about_unable_to_fetch_from_api(self):
        self.dialog = MDDialog(
            title = "API Error",
            text = "Unable to fetch data from the API. Please try again later, or report by mailing at aman.proj.rel@gmail.com.",
            buttons = [
                MDRaisedButton(
                    text="RETRY",
                    on_release = lambda x: (
                        self.dialog.dismiss(),
                        toast("Retrying..."),
                        Clock.schedule_once(lambda dt: self.__load_er_data(False), .05),
                    )
                ),
                MDFlatButton(
                    text="CANCEL",
                    on_release = lambda x: (
                        self.dialog.dismiss(),
                        toast("Loading From File..."),
                    )
                ),
                MDFlatButton(
                    text="SEND REPORT",
                    on_release = lambda x: (
                        self.dialog.dismiss(),
                        toast("Opening email client..."),
                        Clock.schedule_once(lambda dt: self.__send_report_about_api(), .05)
                    )
                ),
            ],
        )

        Clock.schedule_once(
            lambda dt: self.dialog.open(),
            .3
        )
    
    def __send_report_about_api(self):
        # Define the email details
        subject = "API Error Report"
        body = f"There was an error while fetching data from the API. URL which was used is \"{self.er.url}\". Last update local data on {self.config["sync"]["last-sync-time-unix-seconds"]}"
        recipient = "aman.proj.rel@gmail.com"
        
        # Open the email client
        webbrowser.open(f"mailto:{recipient}?subject={subject}&body={body}")

    def sort_currencies(self, currencies_list:list, sort_type:str): #todo
        if sort_type == "Ascending":
            currencies_list.sort()
        elif sort_type == "Descending":
            currencies_list.sort(reverse = True)
        elif sort_type == "Random":
            rd_shuffle(currencies_list)
        
        return currencies_list

class IndividualCurrencyItem(MDCard):
    def __init__(self, name:str, icon:str, text_to_show:str, release_callback):
        super(IndividualCurrencyItem, self).__init__()
        
        self.icon = icon
        self.text = text_to_show
        self.name = name

        self.on_release = lambda: release_callback(self.name)
    
    def update_currency_value_to_show(self, text_to_show:str):
        self.ids.currency_text.text = text_to_show
        self.ids.currency_text.font_name = resource_find("assets/fonts/custom/NotoSans (only certain characters).ttf")

class InputKeyboard(MDCard):
    typed_string:str = ''
    buttons_to_add_text = ['7', '8', '9', 'x', '4', '5', '6', '/', '1', '2', '3', '-', '.', '0', '%', '+', '(', "DEL", "AC", ')', 'K', 'M', 'B', '=']
    available_operators = ['x', '/', '-', '%', '+', '(']

    def __init__(self, update_callback, decimal_places_to_show:int, special_buttons:dict, typed_string:str = ''):
        super(InputKeyboard, self).__init__()
        self.update_callback = update_callback
        self.typed_string = typed_string
        self.__decimal_places_to_show = decimal_places_to_show
        self.special_buttons = special_buttons

        self.buttons_to_add_text[-4], self.buttons_to_add_text[-3], self.buttons_to_add_text[-2] = list(self.special_buttons.keys())[:3]

        for btn_text in self.buttons_to_add_text:
            btn = MDRaisedButton(text = btn_text, elevation = 0.5)
            btn.on_release = lambda bt=btn_text: self.button_press(bt)
            self.ids.buttons_grid.add_widget(btn)
        
    def button_press(self, button_text:str):
        if button_text == "AC":
            self.typed_string = ''
        elif button_text == "DEL":
            self.typed_string = '' if len(self.typed_string) == 0 else self.typed_string[:-1] 
        elif button_text == '=':
            self.typed_string = str(round(float(InputKeyboard.evaluate_expression(self.typed_string)), self.__decimal_places_to_show))
        elif button_text == '.':
            if self.typed_string[-1] == '.':
                return
            else:
                try:
                    InputKeyboard.evaluate_expression((self.typed_string + '.' + '0') if (self.typed_string.count('(') == self.typed_string.count(')')) else (self.typed_string.split('(')[-1] + '.' + '0'))
                    self.typed_string += '.'
                except:
                    return
        elif button_text == '(':
            if self.typed_string[-1] not in self.available_operators:
                self.typed_string += "x("
            else:
                self.typed_string += '('
        elif button_text in "0123456789" and (self.typed_string[-1] == ')' if len(self.typed_string) != 0 else False):
            self.typed_string += 'x' + button_text
        elif button_text in self.special_buttons.keys():
            for btn_name in self.special_buttons:
                if button_text == btn_name:
                    if (self.typed_string[-1] if  len(self.typed_string) != 0 else 'x') not in self.available_operators:
                        self.typed_string += f"x{self.special_buttons[btn_name]}"
                    else:
                        self.typed_string += self.special_buttons[btn_name]
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
