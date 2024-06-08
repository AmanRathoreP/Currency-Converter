from src.settings.elements.common.individual_setting_template import individualSettingBaseClass

import os

from kivy.lang import Builder
from kivy.config import ConfigParser

kivy_design_files = ["info_label_template"]
for kv_file in kivy_design_files:
    Builder.load_file(os.path.join(os.path.dirname(os.path.realpath( __file__ )), kv_file + ".kv"))

class infoLabel(individualSettingBaseClass):
    def __init__(self, config: ConfigParser, section_name, setting_name, title, description, **kwargs):
        individualSettingBaseClass.__init__(self, config, section_name, setting_name, title, **kwargs)

        self.ids.title.text = self.title
        self.ids.description.text = description
