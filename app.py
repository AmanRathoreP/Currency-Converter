from kivy import require as kivy_require
kivy_require("2.3.0")
from kivy.config import Config
sizes = {
	"16x9":[16,9],
	# "android":[1080,2408],
	"android":[4,9],
		 }
size_multiplier = 108
current_size = "16x9"
Config.set('graphics', 'width', str(int(sizes[current_size][0]*size_multiplier)))
Config.set('graphics', 'height', str(int(sizes[current_size][1]*size_multiplier)))

from src.home.home import homeScreen

from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp

class currencyApp(MDApp):
	def build(self):
		self.title = "Currency Convertor"
		self.icon = "assets/icons/work-in-progress.png"
        
		self.screen_manager = ScreenManager()
		self.screen_manager.add_widget(homeScreen())
		return self.screen_manager

if __name__ == "__main__":
	currencyApp().run()
