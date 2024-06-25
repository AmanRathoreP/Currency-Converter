from src.settings.elements.common.sub_settings_template import subSettingsTemplate
from src.settings.elements.sub_settings.currency_converter import ExchangeRates

from kivy.config import ConfigParser

class Currency(subSettingsTemplate):
    def __init__(self, config: ConfigParser, **kwargs):
        super(Currency, self).__init__(config, "currencies to include", **kwargs)
        
        self.clear_all_available_settings()

        self.add_all_possible_settings()
