from src.settings.elements.common.sub_settings_template import subSettingsTemplate

from kivy.config import ConfigParser

class lookAndFeel(subSettingsTemplate):
    def __init__(self, config: ConfigParser, **kwargs):
        super(lookAndFeel, self).__init__(config, "look and feel", **kwargs)
        
        self.clear_all_available_settings()
        
        self.add_combo_box("primary-palette")
        self.add_combo_box("accent-palette")
        self.add_combo_box("theme")
