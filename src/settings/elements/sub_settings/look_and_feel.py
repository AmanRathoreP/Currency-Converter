from src.settings.elements.common.sub_settings_template import subSettingsTemplate

import json

from kivy.config import ConfigParser

class lookAndFeel(subSettingsTemplate):
    def __init__(self, config: ConfigParser, title = "No title provided", **kwargs):
        super(lookAndFeel, self).__init__(config, title, **kwargs)

        with open("available_options_for_each_setting.json", 'r') as json_file:
            available_options = json.load(json_file)

        look_and_feel_options  = available_options["look and feel"]
        
        self.clear_all_available_settings()
        
        self.add_combo_box("look and feel", "primary-palette", look_and_feel_options["primary-palette"], "Primary Palette")
        self.add_combo_box("look and feel", "accent-palette", look_and_feel_options["accent-palette"], "Accent Palette")
        self.add_combo_box("look and feel", "theme", look_and_feel_options["theme"], "Theme")
