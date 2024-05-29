from src.settings.elements.common.search_backend import searchBackend

import os

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors import ButtonBehavior

kivy_design_files = ["setting_item"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", "elements", kv_file + ".kv"))

class SettingsItem(MDCard, ButtonBehavior, searchBackend):
    def __init__(self, icon: str, text: str, setting_info: str, settings_section_name: str, alternate_searchable_string: list[str] = []):
        super(SettingsItem, self).__init__()
        searchBackend.__init__(self, settings_section_name, alternate_searchable_string)
        
        self.icon = icon
        self.text = text
        self.setting_info = setting_info
        #! self.toggle_search_view(["d234", "234d"]*2)
        self.toggle_search_view()

    def toggle_search_view(self, string_to_show:list[str] = None):
        self.ids.setting_infos.clear_widgets()

        if string_to_show == None:
            # Make non search view as current view 
            self.ids.setting_infos_layout.height = dp(20) #20 for setting info
            self.height = dp(20+40+20) # 20 for spacing, 40 for setting name, and 20 for setting info
            self.ids.setting_infos.add_widget(MDLabel(text = self.setting_info, font_style = "Body1"))

            return
        
        self.ids.setting_infos_layout.height = dp(15 * len(string_to_show))
        self.height = dp(20 + 40 + (15 * len(string_to_show))) # 20 for spacing, 40 for setting name and 15 for each search info
        for res in string_to_show:
            self.ids.setting_infos.add_widget(MDLabel(text = res, font_style = "Body2"))
