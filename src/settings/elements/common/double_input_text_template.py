from src.settings.elements.common.individual_setting_template import individualSettingBaseClass

import os
import ast

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivymd.app import MDApp


kivy_design_files = ["double_input_text_template"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.dirname(os.path.realpath( __file__ )), kv_file + ".kv"))

class doubleInputText(individualSettingBaseClass):
    # todo text validator
    def __init__(
            self,
            config: ConfigParser, section_name, setting_name,
            title, left_text_box_title:str, right_text_box_title:str,
            **kwargs
        ):
        __allowed_kwargs = ["max left chars", "max right chars", "left type", "right type"]
        self.filtered_kwargs = {k: v for k, v in kwargs.items() if k in __allowed_kwargs}
        self.unexpected_kwargs = {k: v for k, v in kwargs.items() if k not in __allowed_kwargs}

        individualSettingBaseClass.__init__(self, config, section_name, setting_name, title, **(self.unexpected_kwargs))

        self.left_text_box_title = left_text_box_title
        self.right_text_box_title = right_text_box_title

        self.build()
    
    def build(self):
        self.ids.title.text = self.title
        self.ids.left_text_input.hint_text = self.left_text_box_title
        self.ids.right_text_input.hint_text = self.right_text_box_title
        self.ids.left_text_input.max_text_length = self.filtered_kwargs["max left chars"]
        self.ids.right_text_input.max_text_length = self.filtered_kwargs["max right chars"]

        self.ids.left_text_input.text = ast.literal_eval(self.config[self.section_name][self.setting_name])[0]
        self.ids.right_text_input.text = ast.literal_eval(self.config[self.section_name][self.setting_name])[1]

    def on_text_change(self, text_input:str, is_left_input:bool):
        if self.ids.left_text_input.text == "-1" or self.ids.right_text_input.text == "-1":
            # config text is not loaded
            return

        try:
            self.ids.right_text_input.text = self.ids.right_text_input.text[:self.filtered_kwargs["max right chars"]]
        except:
            pass
        try:
            self.ids.left_text_input.text = self.ids.left_text_input.text[:self.filtered_kwargs["max left chars"]]
        except:
            pass

        if not doubleInputText.validation_by_conversion(self.ids.right_text_input.text, self.filtered_kwargs["right type"]):
            self.ids.right_text_input.text = self.ids.right_text_input.text[0:-1]
        if not doubleInputText.validation_by_conversion(self.ids.left_text_input.text, self.filtered_kwargs["left type"]):
            self.ids.left_text_input.text = self.ids.left_text_input.text[0:-1]
        
        self.config[self.section_name][self.setting_name] = str([self.ids.left_text_input.text, self.ids.right_text_input.text])
        self.config.write()
        MDApp.get_running_app().apply_settings_to_app()

    @staticmethod
    def validation_by_conversion(input_str:str, expected_type:str):
        """
        Converts the input string to the specified type and returns it as a string representation.
        
        Args:
        - input_str (str): The input string to be converted.
        - expected_type (str): Specifies the type to which input_str should be converted.
        Valid options are "int", "float", or "string".
        
        Returns:
        - str: String representation of the converted value if successful.
        - bool: False if conversion fails due to ValueError.
        
        Examples:
        >>> print(validation_by_conversion("17", "int"))       # Output: "17"
        >>> print(validation_by_conversion("17.54", "float"))  # Output: "17.54"
        >>> print(validation_by_conversion("hello", "string"))    # Output: "hello"
        >>> print(validation_by_conversion("17hello", "int"))  # Output: False
        >>> print(validation_by_conversion("17.54", "int"))    # Output: False
        """
        try:
            if expected_type.lower() == "int":
                return str(int(input_str))
            elif expected_type.lower() == "float":
                return str(float(input_str))
            elif expected_type.lower() == "string":
                return input_str
        except ValueError:
            return False