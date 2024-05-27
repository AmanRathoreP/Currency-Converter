from src.settings.elements.common.sub_settings_template import subSettingsTemplate

from kivy.config import ConfigParser

class lookAndFeel(subSettingsTemplate):
    def __init__(self, config: ConfigParser, title = "No title provided", **kwargs):
        super(lookAndFeel, self).__init__(config, title, **kwargs)
        self.add_combo_box("section_name", "setting_name", "options", "title")
        self.add_combo_box("section_name", "setting_name", "options", "title")
