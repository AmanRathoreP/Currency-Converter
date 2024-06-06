import json
from rapidfuzz import process, fuzz
if __name__ != "__main__":
    from kivy.resources import resource_find

class searchBackend():
    def __init__(self, settings_section_name: str = None):

        if settings_section_name == None:
            return

        if __name__ != "__main__":
            with open(resource_find("available_options_for_each_setting.json"), 'r') as json_file:
                self.setting_properties = json.load(json_file)[settings_section_name]
        else:
            with open("available_options_for_each_setting.json", 'r') as json_file:
                self.setting_properties = json.load(json_file)[settings_section_name]

        self.settings_section_name = settings_section_name
        self.alternate_searchable_string = self.setting_properties["alternate search strings"]
    
    def get_search_results(self, string_to_search: str, min_matching_percentage: int = 20, take_top_n_only: int = -1):
        results = []
        raw_results = []
        string_to_search = string_to_search.lower()

        for setting_type in self.setting_properties["data"]:
            setting_search_individual_raw_result = []
            search_result_from_options = process.extract(string_to_search, [string.lower() for string in self.setting_properties["data"][setting_type]["options"]], scorer=fuzz.WRatio, limit=len(self.setting_properties["data"][setting_type]["options"]))
            search_result_from_alternatives = process.extract(string_to_search, [string.lower() for string in self.setting_properties["data"][setting_type]["alternate search strings"]], scorer=fuzz.WRatio, limit=len(self.setting_properties["data"][setting_type]["alternate search strings"]))
            for res in search_result_from_options:
                if int(res[1]) > min_matching_percentage:
                    setting_search_individual_raw_result.append((setting_type,
                                                                 self.setting_properties["data"][setting_type]["title"] + " -> " + self.setting_properties["data"][setting_type]["options"][res[2]],
                                                                 int(res[1])))
            
            for res in search_result_from_alternatives:
                if int(res[1]) > min_matching_percentage:
                    setting_search_individual_raw_result.append((f"!alternate_search_string_of_sub_setting!{setting_type}",
                                        f"!alternate_search_string_of_sub_setting!{self.setting_properties["data"][setting_type]["title"]}" + '!' + self.setting_properties["data"][setting_type]["alternate search strings"][res[2]],
                                        int(res[1])))
            
            #* removing duplicate matches of alternate search and options search of same setting
            number_of_res_from_alternate_search_string_found: int = 0
            for res in setting_search_individual_raw_result:
                if str(res[0]).find(f"!alternate_search_string_of_sub_setting!{self.setting_properties["data"][setting_type]["title"]}") != 1:
                    number_of_res_from_alternate_search_string_found += 1
            if number_of_res_from_alternate_search_string_found == len(setting_search_individual_raw_result) and len(setting_search_individual_raw_result) > 0:
                #* all results are from alternate search so we will keep only one
                raw_results.append(setting_search_individual_raw_result[0])
            else:
                #* one or more res are from options so we will delete all the alternate search results
                raw_results.extend([res for res in setting_search_individual_raw_result if res[0].startswith("!alternate_search_string_of_sub_setting!") == -1])
            
        
        search_result = process.extract(string_to_search, [string.lower() for string in self.setting_properties["alternate search strings"]], scorer=fuzz.WRatio, limit=len(self.setting_properties["alternate search strings"]))
        search_result = sorted(search_result, key=lambda x: x[1], reverse=True)
        if search_result[0][1] > min_matching_percentage and len(raw_results) == 0:
            #* adding alternate search result of section only when no result is found inside the section 
            raw_results.append(("!alternate_search_string_of_section!", "!alternate_search_string_of_section!" + '!' + self.setting_properties["alternate search strings"][search_result[0][2]], int(search_result[0][1])))

        results = sorted(raw_results, key=lambda x: x[2], reverse=True)[:take_top_n_only if take_top_n_only > 0 else len(raw_results)]
        return results if len(results)>0 else -1
    
    @staticmethod
    def _filter_search_result_to_show_on_screen(res: str) -> str:
        if res.find("!alternate_search_string_of_section!" + '!') != -1:
            return -1
        elif res.find("!alternate_search_string_of_sub_setting!") != -1:
            return str(res.split('!')[2])
        return res



if __name__ == "__main__":
    sr = searchBackend("look and feel")
    sr_results = sr.get_search_results("pala", 75, 11)
    try:
        for res in sr_results:
            print(res)
            print(searchBackend._filter_search_result_to_show_on_screen(res[1]))
            print("------------------------------------------------------------------------------------------------------------------------------")
    except Exception as e:
        print("no result found")