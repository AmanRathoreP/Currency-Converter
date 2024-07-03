from src.settings.elements.common.sub_settings_template import subSettingsTemplate
from src.settings.elements.sub_settings.currency_converter import ExchangeRates
from src.settings.elements.common.checkbox_template_for_currencies_select import customCheckBoxForCurrency

from kivy.resources import resource_find
from kivy.config import ConfigParser

class Currency(subSettingsTemplate):
    def __init__(self, config: ConfigParser, **kwargs):
        super(Currency, self).__init__(config, "currencies to include", **kwargs)
        
        self.clear_all_available_settings()
        self.add_all_currencies_to_settings(**kwargs)

    def add_all_currencies_to_settings(self, **kwargs):
        try:
            if resource_find("exchange_rates.json") != None:
                er = ExchangeRates(resource_find("exchange_rates.json"))
            else:
                open("exchange_rates.json", 'a').close()
                er = ExchangeRates(resource_find("exchange_rates.json"))

        except RuntimeError as e:
            # todo show info to user
            print(e)
        
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
                for tab in self.tabs_instances:
                    if tab.id == "available currencies by default":
                        tab.ids.sub_settings.add_widget(check_box)
