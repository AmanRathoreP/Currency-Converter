import json
from rapidfuzz import process, fuzz

class searchBackend():
    def __init__(self, settings_section_name: str = None):

        if settings_section_name == None:
            return

        with open("available_options_for_each_setting.json", 'r') as json_file:
            self.setting_properties = json.load(json_file)[settings_section_name]

        self.settings_section_name = settings_section_name
        self.alternate_searchable_string = self.setting_properties["alternate search strings"]
    
    def get_search_results(self, string_to_search: str, min_matching_percentage: int = 20, take_top_n_only: int = -1):
        results = []
        raw_results = []
        string_to_search = string_to_search.lower()

        for setting_type in self.setting_properties["data"]:
            search_result_from_options = process.extract(string_to_search, [string.lower() for string in self.setting_properties["data"][setting_type]["options"]], scorer=fuzz.WRatio, limit=len(self.setting_properties["data"][setting_type]["options"]))
            search_result_from_alternatives = process.extract(string_to_search, [string.lower() for string in self.setting_properties["data"][setting_type]["alternate search strings"]], scorer=fuzz.WRatio, limit=len(self.setting_properties["data"][setting_type]["alternate search strings"]))
            for res in search_result_from_options:
                if int(res[1]) > min_matching_percentage:
                    raw_results.append((setting_type, self.setting_properties["data"][setting_type]["options"][res[2]], int(res[1])))
            
            for res in search_result_from_alternatives:
                if int(res[1]) > min_matching_percentage:
                    raw_results.append((f"!alternate_search_string_of_sub_setting!{setting_type}", self.setting_properties["data"][setting_type]["alternate search strings"][res[2]], int(res[1])))
            
        
        search_result = process.extract(string_to_search, [string.lower() for string in self.setting_properties["alternate search strings"]], scorer=fuzz.WRatio, limit=len(self.setting_properties["alternate search strings"]))
        for res in search_result:
            if int(res[1]) > min_matching_percentage:
                raw_results.append(("!alternate_search_string_of_section!", self.setting_properties["alternate search strings"][res[2]], int(res[1])))

        results = sorted(raw_results, key=lambda x: x[2], reverse=True)[:take_top_n_only if take_top_n_only > 0 else len(raw_results)]
        return results if len(results)>0 else -1

if __name__ == "__main__":
    sr = searchBackend("look and feel")
    sr_results = sr.get_search_results("Look & fee", 50, 11)
    try:
        for res in sr_results:
            print(res)
    except:
        print("no result found")