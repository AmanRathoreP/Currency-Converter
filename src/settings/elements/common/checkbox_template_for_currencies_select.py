from src.settings.elements.common.checkbox_template import customCheckBox

from kivymd.app import MDApp

class customCheckBoxForCurrency(customCheckBox):
    def on_box_clicked(self):
        
        try:
            currently_active_non_custom_currencies = str(self.config[self.section_name]["active-non-custom-currencies"]).replace('\'', '').replace(' ', '')[1:-1].split(',')
        except:
            print("\"active-non-custom-currencies\" not found in app settings ini file!")
            return
        
        if self.ids.boolean.state == "down":
            #* include currency
            if self.setting_name in currently_active_non_custom_currencies:
                return
            else:
                currently_active_non_custom_currencies.append(self.setting_name)
        else:
            #* exclude currency
            if self.setting_name in currently_active_non_custom_currencies:
                currently_active_non_custom_currencies.remove(self.setting_name)
            else:
                return

        
        self.config[self.section_name]["active-non-custom-currencies"] = str(currently_active_non_custom_currencies)
        self.config.write()
        MDApp.get_running_app().apply_settings_to_app()
    
    @property
    def previous_boolean_state_of_check_box(self):
        try:
            currently_active_non_custom_currencies = str(self.config[self.section_name]["active-non-custom-currencies"]).replace('\'', '').replace(' ', '')[1:-1].split(',')
        except:
            print("\"active-non-custom-currencies\" not found in app settings ini file!")
            return
        
        if self.setting_name in currently_active_non_custom_currencies:
            return "True"
        return "False"
        