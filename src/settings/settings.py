from src.settings.elements.common.sub_settings_template import subSettingsTemplate
from src.settings.elements.sub_settings.look_and_feel import lookAndFeel
from src.settings.settings_screen import settingsDefaultScreen

from kivy.config import ConfigParser
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition.transition import MDSwapTransition

class settingsScreen(MDScreen):
    def show_settings_screen(self):
        self.screen_manager.current = "default_settings_screen"
    
    def show_settings_screen_instantly(self):
        self.screen_manager.transition = MDSwapTransition(duration = 0.01)
        self.screen_manager.current = "default_settings_screen"
        self.screen_manager.transition = MDSwapTransition(duration = .36)
    
    def add_individual_settings_screen(self, title, name):
        setting_screen = subSettingsTemplate(self.config, title = title, name = name)
        self.screen_manager.add_widget(setting_screen)
        
    def __init__(self, config: ConfigParser, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.screen_manager = MDScreenManager()
        self.screen_manager.transition = MDSwapTransition(duration = .36)
        default_settings_screen = settingsDefaultScreen(config, name = "default_settings_screen")
        self.screen_manager.add_widget(default_settings_screen)

        self.add_individual_settings_screen("Currency", "Currency")
        self.add_individual_settings_screen("Format Currency Values", "Format Currency Values")
        self.screen_manager.add_widget(lookAndFeel(self.config, "Look & Feel", name = "Look & Feel"))
        self.add_individual_settings_screen("Synchronisation", "Synchronisation")
        self.add_individual_settings_screen("About", "About")

        self.add_widget(self.screen_manager)

    def navigate_to_setting(self, settings_screen_name, setting_section_name = None, setting_name = None):
        self.screen_manager.current = settings_screen_name
        if (setting_section_name == None) or (setting_name == None):
            return
        for setting_screen in self.screen_manager.children:
            if setting_screen.name == settings_screen_name:
                setting_screen.highlight_setting(setting_section_name, setting_name)
