from kivy.config import ConfigParser
from kivy.animation import Animation
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp


class individualSettingBaseClass(MDCard):
    drop_item_menu: MDDropdownMenu = None

    def __init__(self, config: ConfigParser, section_name, setting_name, title, **kwargs):
        MDCard.__init__(self, **kwargs)
        self.config = config
        self.section_name = section_name
        self.setting_name = setting_name
        self.title = title

    def animate_for_easy_navigation(self):
        # todo bring setting in current display if there are too many settings 
        running_app = MDApp.get_running_app()
        opacity = .84
        each_color_transition_duration: float = .2
        anim = Animation(md_bg_color = (*running_app.theme_cls.accent_color[:3], opacity), t='in_quad', duration = each_color_transition_duration)
        for i in range(2):
            anim += Animation(md_bg_color = (*running_app.theme_cls.primary_color[:3], opacity), t='in_quad', duration = each_color_transition_duration)
            anim += Animation(md_bg_color = (*running_app.theme_cls.accent_color[:3], opacity), t='in_quad', duration = each_color_transition_duration)
        anim += Animation(md_bg_color = self.md_bg_color, t='in_quad', duration = each_color_transition_duration*1.2)
        anim.start(self)
        print(f"Animating...\nself.section_name -> {self.section_name}\nself.setting_name -> {self.setting_name}")
