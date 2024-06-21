from src.settings.elements.common.individual_setting_template import individualSettingBaseClass

import os

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivymd.app import MDApp

kivy_design_files = ["checkbox_template"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.dirname(os.path.realpath( __file__ )), kv_file + ".kv"))

class customCheckBox(individualSettingBaseClass):
    """
    Custom CheckBox class for different checkbox types within a settings interface.

    Attributes:
        check_box_type (str): Type of the checkbox, can be "boolean", "multiple-options-select", or "single-option-select".
        options (list): List of options for the checkbox, used for multiple and single option selects.
    """
    check_box_type:str = ""
    options = []

    def __init__(self, config: ConfigParser, section_name, setting_name, title, check_box_type:str, options = None, **kwargs):
        """
        Initialize the customCheckBox instance.

        Args:
            config (ConfigParser): The configuration parser instance of the app to save settings.
            section_name (str): The section name in the config file.
            setting_name (str): The setting name in the config file.
            title (str): The title/name of the checkbox.
            check_box_type (str): The type of checkbox (e.g., "boolean", "multiple-options-select", "single-option-select").
            options (list, optional): The options for the checkbox. Defaults to None.
            **kwargs: Additional keyword arguments for customization that passed to individualSettingBaseClass which inherits MDCard.
        """
        individualSettingBaseClass.__init__(self, config, section_name, setting_name, title, **kwargs)

        self.options = options
        self.check_box_type = check_box_type
        self.ids.label_option_name.text = self.title

        if self.check_box_type == "boolean":
            #todo only show boolean type of check box
            self.ids.boolean.state = "down" if self.config[self.section_name][self.setting_name] == "True" else "normal"
        elif self.check_box_type == "multiple-options-select":
            #todo only show multiple-options-select type of check box
            pass
        elif self.check_box_type == "single-option-select":
            #todo only show single-option-select type of check box
            pass
        else:
            #todo throw exception
            pass

    def on_box_clicked(self):
        if self.check_box_type == "boolean":
            __setting_value_to_write:str = "True" if self.ids.boolean.state == "down" else "False"
        
        self.config[self.section_name][self.setting_name] = __setting_value_to_write
        self.config.write()
        MDApp.get_running_app().apply_settings_to_app()