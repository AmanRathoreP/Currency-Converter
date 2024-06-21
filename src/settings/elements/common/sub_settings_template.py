from src.settings.elements.common.combobox_template import comboBox
from src.settings.elements.common.info_label_template import infoLabel
from src.settings.elements.common.checkbox_template import customCheckBox

import os
import json

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivy.resources import resource_find
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout

kivy_design_files = ["sub_settings_template"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.dirname(os.path.realpath( __file__ )), kv_file + ".kv"))

class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""
    id:str = None
    def __init__(self, id:str, **kwargs):
        self.id = id
        super(Tab, self).__init__(**kwargs)

class subSettingsTemplate(MDScreen):
    sub_settings_list = []
    show_tabs_view = False
    tabs_info_dict = {}
    tabs_instances = []

    def __init__(self, config: ConfigParser, setting_section_name:str, **kwargs):
        MDScreen.__init__(self, **kwargs)
        self.config = config
        self.setting_section_name = setting_section_name
        self.name = setting_section_name

        with open(resource_find("available_options_for_each_setting.json"), 'r') as json_file:
            self.setting_properties = json.load(json_file)[setting_section_name]
    
        self.ids.top_bar.title = self.setting_properties["title"]

        number_of_sub_settings_with_tabs = 0
        for sub_setting_data_key in self.setting_properties["data"].keys():
            if "tab" in self.setting_properties["data"][sub_setting_data_key]:
                number_of_sub_settings_with_tabs += 1
                if self.setting_properties["data"][sub_setting_data_key]["tab"]["id"] not in self.tabs_info_dict.keys():
                    self.tabs_info_dict[self.setting_properties["data"][sub_setting_data_key]["tab"]["id"]] = self.setting_properties["data"][sub_setting_data_key]["tab"]
        if len(self.setting_properties["data"]) == number_of_sub_settings_with_tabs and 0 != number_of_sub_settings_with_tabs:
            self.show_tabs_view = True
        elif len(self.setting_properties["data"]) != number_of_sub_settings_with_tabs and 0 != number_of_sub_settings_with_tabs:
            #! all sub-settings doesn't have tab names
            raise AttributeError(f"\"tab\" is assigned to only some members of the setting {self.ids.top_bar.title}.\nNumber of tabs are {number_of_sub_settings_with_tabs}.\nNumber of sub-settings are {len(self.setting_properties["data"])}.")
        
        if self.show_tabs_view:
            #* create tabs
            self.remove_widget(self.ids.scroll_view_for_settings)
            for tab in self.tabs_info_dict.values():
                tab_elements = tab.keys()
                if "icon" in tab_elements and "name" not in tab_elements:
                    self.tabs_instances.append(Tab(id = tab["id"],icon = tab["icon"]))
                    self.ids.tabs.add_widget(self.tabs_instances[-1])
                elif "icon" in tab_elements and "name" in tab_elements:
                    self.tabs_instances.append(Tab(id = tab["id"],icon = tab["icon"], title = tab["name"]))
                    self.ids.tabs.add_widget(self.tabs_instances[-1])
                elif "icon" not in tab_elements and "name" in tab_elements:
                    self.tabs_instances.append(Tab(id = tab["id"],title = tab["name"]))
                    self.ids.tabs.add_widget(self.tabs_instances[-1])

        else:
            self.tabs_info_dict = []
            self.remove_widget(self.ids.tabs)

    def clear_all_available_settings(self):
        if self.show_tabs_view:
            for tab in self.tabs_instances:
                tab.ids.sub_settings.clear_widgets()
            return self
        
        self.ids.sub_settings.clear_widgets()
        return self
    
    def add_combo_box(self, setting_name_in_settings_properties_json_file, **kwargs):
        combo_box = comboBox(self.config,
                             self.setting_section_name,
                             self.setting_properties["data"][setting_name_in_settings_properties_json_file]["config file's setting name"],
                             self.setting_properties["data"][setting_name_in_settings_properties_json_file]["options"],
                             self.setting_properties["data"][setting_name_in_settings_properties_json_file]["title"],
                             **kwargs)

        self.add_element_to_settings_screen(combo_box,
                                            self.setting_properties["data"][setting_name_in_settings_properties_json_file]["tab"]["id"] if "tab" in self.setting_properties["data"][setting_name_in_settings_properties_json_file].keys() else None)

        return self

    def highlight_setting(self, section_name: str, setting_name: str):
        if self.show_tabs_view:
            for tab in self.tabs_instances:
                if self.setting_properties["data"][setting_name]["tab"]["id"] == tab.id:
                    self.ids.tabs.carousel.load_slide(tab)
        for sub_setting in self.sub_settings_list:
            if (sub_setting.section_name == section_name) and (sub_setting.setting_name == setting_name):
                sub_setting.animate_for_easy_navigation()

    def add_info_label(self, setting_name_in_settings_properties_json_file, **kwargs):
        info_label = infoLabel(None,
                             self.setting_section_name, #* used to highlight the setting/info after search for setting
                             setting_name_in_settings_properties_json_file, #* used to highlight the setting/info after search for setting
                             self.setting_properties["data"][setting_name_in_settings_properties_json_file]["title"],
                             self.setting_properties["data"][setting_name_in_settings_properties_json_file]["description"],
                             **kwargs)

        self.add_element_to_settings_screen(info_label,
                                            self.setting_properties["data"][setting_name_in_settings_properties_json_file]["tab"]["id"] if "tab" in self.setting_properties["data"][setting_name_in_settings_properties_json_file].keys() else None)

        return self

    def add_all_possible_settings(self, clear_all_the_available_settings=True, **kwargs) -> tuple:
        """
        Adds all the settings which are available in the JSON `self.setting_properties["data"]`,
        and whose template is also available.

        Args:
        - clear_all_the_available_settings (bool): Clears previous setting(s) before adding any setting(s). Default is True.
        - **kwargs: Additional keyword arguments passed to individual setting addition methods.

        Returns:
        - Tuple containing (self, settings_not_added):
            - self: The instance of the class.
            - settings_not_added (list): List of setting names which could not be added due to unsupported types or other issues.
        """
        
        if clear_all_the_available_settings:
            self.clear_all_available_settings()

        settings_not_added = []

        for setting_name_in_settings_properties_json_file in self.setting_properties["data"]:
            if self.setting_properties["data"][setting_name_in_settings_properties_json_file]["type"] == "combo box":
                self.add_combo_box(setting_name_in_settings_properties_json_file, **kwargs)
            elif self.setting_properties["data"][setting_name_in_settings_properties_json_file]["type"] == "info label":
                self.add_info_label(setting_name_in_settings_properties_json_file, **kwargs)
            elif self.setting_properties["data"][setting_name_in_settings_properties_json_file]["type"] == "checkbox-boolean":
                self.add_checkbox(setting_name_in_settings_properties_json_file, check_box_type = "boolean", **kwargs)
            elif self.setting_properties["data"][setting_name_in_settings_properties_json_file]["type"] == "checkbox-multiple-options-select":
                self.add_checkbox(setting_name_in_settings_properties_json_file, check_box_type = "multiple-options-select", **kwargs)
            elif self.setting_properties["data"][setting_name_in_settings_properties_json_file]["type"] == "checkbox-single-option-select":
                self.add_checkbox(setting_name_in_settings_properties_json_file, check_box_type = "single-option-select", **kwargs)
            else:
                settings_not_added.append(setting_name_in_settings_properties_json_file)
        
        return self, settings_not_added

    def add_element_to_settings_screen(self, element, tab_id = None):
        self.sub_settings_list.append(element)
        if not self.show_tabs_view:
            self.ids.sub_settings.add_widget(element)
        else:
            for tab in self.tabs_instances:
                if tab.id == tab_id:
                    tab.ids.sub_settings.add_widget(element)

    def add_checkbox(self, setting_name_in_settings_properties_json_file, check_box_type:str, **kwargs):
        check_box = customCheckBox(
            self.config,
            self.setting_section_name,
            self.setting_properties["data"][setting_name_in_settings_properties_json_file]["config file's setting name"],
            self.setting_properties["data"][setting_name_in_settings_properties_json_file]["title"],
            check_box_type,
            **kwargs
            )
        
        self.add_element_to_settings_screen(
            check_box,
            self.setting_properties["data"][setting_name_in_settings_properties_json_file]["tab"]["id"] if "tab" in self.setting_properties["data"][setting_name_in_settings_properties_json_file].keys() else None)
        
        return self
