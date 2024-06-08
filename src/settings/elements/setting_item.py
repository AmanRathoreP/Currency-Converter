from src.settings.elements.common.search_backend import searchBackend

import os

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.uix.behaviors import ButtonBehavior

kivy_design_files = ["setting_item"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.dirname(os.path.realpath( __file__ )), kv_file + ".kv"))

class SettingsItem(MDCard, ButtonBehavior, searchBackend):
    radius_for_the_search_result_card = dp(10)
    def __init__(self, settings_section_name: str):
        super(SettingsItem, self).__init__()
        searchBackend.__init__(self, settings_section_name)
        
        self.icon = self.setting_properties["icon"]
        self.text = self.setting_properties["title"]
        self.setting_info = self.setting_properties["description"]
        self.name = settings_section_name
        #! self.toggle_search_view(["d234", "234d"]*2)
        self.toggle_search_view()

    def toggle_search_view(self, string_to_show:list[str] = None, string_is_of_which_setting:str = None):
        self.ids.setting_infos.clear_widgets()

        if string_to_show == None:
            # Make non search view as current view 
            self.ids.setting_infos_layout.height = dp(20) #20 for setting info
            self.height = dp(20+40+20) # 20 for spacing, 40 for setting name, and 20 for setting info
            self.ids.setting_infos.add_widget(MDLabel(text = self.setting_info, font_style = "Body1"))

            return
        
        self.ids.setting_infos_layout.height = dp(15 * len(string_to_show))
        self.height = dp(20 + 40 + (15 * len(string_to_show))) # 20 for spacing, 40 for setting name and 15 for each search info
        
        current_index_of_string_to_show:int = 0
        max_string_size = 1
        for res in string_to_show:
            res = SettingsItem._filter_search_result_to_show_on_screen(res)
            res = '' if res == -1 else res
            max_string_size = len(res) if len(res)>max_string_size else max_string_size
        
        for res in string_to_show:
            res = SettingsItem._filter_search_result_to_show_on_screen(res)
            if res == -1:
                # returning if the search result is from alternate search string of sub-setting
                self.toggle_search_view()
                return

            search_info_card = MDCard()
            search_info_label = MDLabel(text = res, font_style = "Body2")
            search_info_label.padding = [dp(20), 0, 0, 0]
            search_info_card.size_hint = (None, None)  # Disable size_hint
            search_info_card.width = dp((max_string_size*8) + 120)
            search_info_card.height = dp(15)  # Ensure the card has a height
            search_info_card.ripple_behavior = True
            search_info_card.radius = dp(0)
            running_app = MDApp.get_running_app()
            search_info_card.on_release = lambda: running_app.settings.navigate_to_setting(self.settings_section_name, string_is_of_which_setting)
            search_info_card.md_bg_color = (*running_app.theme_cls.accent_color[:3], 0.3 * 2)
            search_info_card.ripple_color = (*running_app.theme_cls.primary_color[:3], 0.25 * 2)

            if current_index_of_string_to_show == 0:
                search_info_card.radius = [self.radius_for_the_search_result_card, self.radius_for_the_search_result_card, dp(0), dp(0)]
            elif current_index_of_string_to_show == len(string_to_show)-1:
                search_info_card.radius = [dp(0), dp(0), self.radius_for_the_search_result_card, self.radius_for_the_search_result_card]
            if len(string_to_show) == 1:
                search_info_card.radius = [self.radius_for_the_search_result_card]*4


            search_info_card.add_widget(search_info_label)
            self.ids.setting_infos.add_widget(search_info_card)

            current_index_of_string_to_show += 1
