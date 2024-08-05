from src.settings.elements.common.sub_settings_template import subSettingsTemplate
from src.settings.settings_screen import settingsDefaultScreen
from src.settings.elements.sub_settings.currencies_to_include import Currency

from kivy.config import ConfigParser
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition.transition import MDSwapTransition

class settingsScreen(MDScreen):
    settings_ready_to_use:bool = False

    def show_settings_screen(self):
        self.screen_manager.current = "default_settings_screen"
    
    def show_settings_screen_instantly(self):
        self.screen_manager.transition = MDSwapTransition(duration = 0.01)
        self.screen_manager.current = "default_settings_screen"
        self.screen_manager.transition = MDSwapTransition(duration = .36)
    
    def add_individual_settings_screen(self, setting_section_name_in_config_file):
        self.screen_manager.add_widget(subSettingsTemplate(self.config, setting_section_name = setting_section_name_in_config_file))
        
    def __init__(self, config: ConfigParser, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.screen_manager = MDScreenManager()
        self.screen_manager.transition = MDSwapTransition(duration = .36)
        default_settings_screen = settingsDefaultScreen(config, name = "default_settings_screen")
        self.screen_manager.add_widget(default_settings_screen)

        default_settings_screen.show_loading_screen()

        self.add_widget(self.screen_manager)

        self.create_settings()

    def navigate_to_setting(self, setting_section_name, setting_name = None):
        # screen name is same as section name
        
        self.screen_manager.current = setting_section_name

        if setting_section_name == "currencies to include":
            self.currency_screen.render_pool_data()
        
        if setting_name == None:
            return
        for setting_screen in self.screen_manager.children:
            if setting_screen.name == setting_section_name:
                if "!alternate_search_string_of_sub_setting!" == setting_name[:len("!alternate_search_string_of_sub_setting!")] and setting_screen.name == setting_section_name:
                    setting_screen.highlight_setting(setting_section_name, setting_name[len("!alternate_search_string_of_sub_setting!"):])
                else:
                    setting_screen.highlight_setting(setting_section_name, setting_name)

    def create_settings(self):
        '''
        Creation of settings stuff takes time. That's why one will call this function in a side thread rather than main thread.
        '''
        
        if self.settings_ready_to_use:
            return
        
        self.currency_screen = Currency(self.config)
        self.screen_manager.add_widget(self.currency_screen)
        self.screen_manager.add_widget(subSettingsTemplate(self.config, setting_section_name = "format numbers' looks").add_all_possible_settings()[0])
        self.screen_manager.add_widget(subSettingsTemplate(self.config, setting_section_name = "look and feel").add_all_possible_settings()[0])
        self.screen_manager.add_widget(subSettingsTemplate(self.config, setting_section_name = "sync").add_all_possible_settings()[0])
        self.screen_manager.add_widget(subSettingsTemplate(self.config, setting_section_name = "about").add_all_possible_settings()[0])

        self.screen_manager.get_screen("default_settings_screen").show_loading_screen(False)

        self.settings_ready_to_use = True
