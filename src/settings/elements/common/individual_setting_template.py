import os

from kivy.config import ConfigParser
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu


class individualSettingBaseClass(MDCard):
    drop_item_menu: MDDropdownMenu = None

    def __init__(self, config: ConfigParser, section_name, setting_name, options, title, **kwargs):
        MDCard.__init__(self, **kwargs)
        self.config = config
        self.section_name = section_name
        self.setting_name = setting_name
        self.options = options
        self.title = title

    def animate_for_easy_navigation(self):
        print(f"Animating...\nself.section_name -> {self.section_name}\nself.setting_name -> {self.setting_name}")
