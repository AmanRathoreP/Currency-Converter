import os

from kivy.lang import Builder
from kivy.config import ConfigParser
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp

kivy_design_files = ["combobox_template"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.abspath(os.getcwd()), "src", "settings", "elements", "common", kv_file + ".kv"))

class comboBox(MDCard):
    drop_item_menu: MDDropdownMenu = None

    def __init__(self, config: ConfigParser, section_name, setting_name, options, title, **kwargs):
        MDCard.__init__(self, **kwargs)
        self.config = config
        self.section_name = section_name
        self.setting_name = setting_name
        self.options = options
        self.title = title

        self.ids.label_option_name.text = self.title
        self.ids.button_select.text = self.config.get(section_name, setting_name)

    def open_drop_item_menu(self, item):
        menu_items = [
            {
                "text": f"{self.options[i]}",
                "on_release": lambda x=f"{self.options[i]}": self.menu_button_clicked(x),
            }
            for i in range(len(self.options))
        ]

        if not self.drop_item_menu:
            self.drop_item_menu = MDDropdownMenu(caller=item, items=menu_items, position="center")
        
        self.drop_item_menu.open()

    def menu_button_clicked(self, item_text):
        self.ids.button_select.text = item_text
        self.drop_item_menu.dismiss()
        self.config[self.section_name][self.setting_name] = item_text
        self.config.write()
        MDApp.get_running_app().apply_settings_to_app()
