from src.settings.elements.individual_settings_screen import settingsIndividualScreen
from src.settings.settings_screen import settingsDefaultScreen

from kivy.config import ConfigParser
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition.transition import MDSwapTransition

class settingsScreen(MDScreen):
    def show_settings_screen(self, instance):
        self.screen_manager.current = "default_settings_screen"
    
    def add_individual_settings_screen(self, title, name):
        setting_screen = settingsIndividualScreen(self.config, title = title, name = name)
        setting_screen.ids.button_back.bind(on_press = self.show_settings_screen)
        self.screen_manager.add_widget(setting_screen)
        
    def __init__(self, config: ConfigParser, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.screen_manager = MDScreenManager()
        self.screen_manager.transition = MDSwapTransition()
        default_settings_screen = settingsDefaultScreen(config, name = "default_settings_screen")
        self.screen_manager.add_widget(default_settings_screen)

        self.add_individual_settings_screen("Currency", "Currency")
        self.add_individual_settings_screen("Format Currency Values", "Format Currency Values")
        self.add_individual_settings_screen("Look & Feel", "Look & Feel")
        self.add_individual_settings_screen("Synchronisation", "Synchronisation")
        self.add_individual_settings_screen("About", "About")
        self.add_individual_settings_screen("Currency", "Currency")

        self.add_widget(self.screen_manager)





"""


SettingsItem:
    icon: "cash-sync"
    text: "Currency"
    subtext: "todo"
SettingsItem:
    icon: "format-text"
    text: "Format Currency Values"
    subtext: "todo"
SettingsItem:
    icon: "invert-colors"
    text: "Look & Feel"
    subtext: "todo"
SettingsItem:
    icon: "sync"
    text: "Synchronisation"
    subtext: "todo"
SettingsItem:
    icon: "information-variant-circle"
    text: "About"
    subtext: "todo"


"""