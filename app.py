from kivy import require as kivy_require
kivy_require("2.3.0")
from kivy.config import Config
sizes = {
	"16x9":[16,9],
	# "android":[1080,2408],
	"android":[4,9],
	"dev":[10,6],
		 }
size_multiplier = 108
current_size = "dev"
Config.set('graphics', 'width', str(int(sizes[current_size][0]*size_multiplier)))
Config.set('graphics', 'height', str(int(sizes[current_size][1]*size_multiplier)))

if __name__ == '__main__':
	import os, sys
	from kivy.resources import resource_add_path
	if hasattr(sys, '_MEIPASS'):
		resource_add_path(os.path.join(sys._MEIPASS))

from src.home.home import homeScreen
from src.settings.settings import settingsScreen

import json

from kivy.uix.screenmanager import ScreenManager
from kivy.resources import resource_find
from kivymd.app import MDApp

class currencyApp(MDApp):
	def apply_settings_to_app(self):
		self.theme_cls.primary_palette = self.config.get("look and feel", "primary-palette")
		self.theme_cls.accent_palette = self.config.get("look and feel", "accent-palette")
		self.theme_cls.theme_style = self.config.get("look and feel", "theme")

	def on_start(self):
		self.title = "Currency Converter"
		self.icon = resource_find("assets/icons/work-in-progress.png")
		self.apply_settings_to_app()

	def build(self):
		self.screen_manager = ScreenManager()
		self.home = homeScreen(self.config, name = "home")
		self.settings = settingsScreen(self.config, name = "settings")
		self.screen_manager.add_widget(self.home)
		self.screen_manager.add_widget(self.settings)
		return self.screen_manager
	
	def build_config(self, config):
		# loading app's default
		with open(resource_find("available_options_for_each_setting.json"), 'r') as json_file:
			json_data = json.load(json_file)
			defaults_data_json = {}
			for setting in json_data:
				__setting_default_data_dict = {}
				for sub_setting in json_data[setting]["data"]:
					try:
						__setting_default_data_dict[sub_setting] = json_data[setting]["data"][sub_setting]["default"]
					except:
						print(f"No default(s) for \"{setting}\" -> \"{sub_setting}\" found.")
				defaults_data_json[setting] = __setting_default_data_dict

		for section, defaults in defaults_data_json.items():
			config.setdefaults(section, defaults)

	def navigate_to_settings(self):
		self.settings.show_settings_screen_instantly()
		self.screen_manager.transition.direction = "left"
		self.screen_manager.current = "settings"
		self.settings.create_settings() #todo run it parallel so that user can see loading stuff

	def navigate_to_home(self):
		self.screen_manager.transition.direction = "right"
		self.screen_manager.current = "home"


if __name__ == "__main__":
	currencyApp().run()
