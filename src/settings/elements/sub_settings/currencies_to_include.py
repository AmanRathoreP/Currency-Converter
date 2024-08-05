from src.settings.elements.common.sub_settings_template import subSettingsTemplate
from src.settings.elements.sub_settings.currency_converter import ExchangeRates
from src.settings.elements.common.checkbox_template_for_currencies_select import customCheckBoxForCurrency

from kivy.resources import resource_find
from kivy.config import ConfigParser
from kivy.clock import Clock
from kivymd.toast import toast

class Currency(subSettingsTemplate):
    currencies_added:bool = False

    def __init__(self, config: ConfigParser, **kwargs):
        super(Currency, self).__init__(config, "currencies to include", **kwargs)
        self.kwargs = kwargs
        
        self.clear_all_available_settings()
        self.add_all_possible_settings()

    def add_all_currencies_to_settings(self, **kwargs):
        er = ExchangeRates(resource_find("exchange_rates.json"), True)
        
        curr_list = er.get_lists()
        for type in curr_list:
            for cr in curr_list[type]:
                print(f"{cr.upper()}, {curr_list[type][cr]["name"]}")

                check_box = customCheckBoxForCurrency(
                    self.config,
                    "currencies to include",
                    cr.upper(),
                    f"{cr.upper()}, {curr_list[type][cr]["name"]}",
                    check_box_type  = "boolean",
                    **kwargs
                    )

                self.add_element_to_settings_screen(check_box)
        
        toast("All currencies successfully added", duration = 2.1)

    def render_pool_data(self):
        if not self.currencies_added:
            toast("Loading available currencies...", duration = 1.5)
            Clock.schedule_once(lambda dt: self.add_all_currencies_to_settings(**(self.kwargs)), 1.1)
            self.currencies_added = True

