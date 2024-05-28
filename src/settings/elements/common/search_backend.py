import json
from rapidfuzz import process, fuzz

class searchBackend():
    def __init__(self, settings_section_name: str = None, alternate_searchable_string: list[str] = []):
        with open("available_options_for_each_setting.json", 'r') as json_file:
            available_options = json.load(json_file)

        try:
            self.options = available_options[settings_section_name]
        except:
            self.options = []

        self.alternate_searchable_string = alternate_searchable_string
    
    def get_search_results(self, string_to_search: str, min_matching_percentage: int = 20, take_top_n_only: int = -1):
        results = []
        raw_results = []
        string_to_search = string_to_search.lower()

        for setting_type in self.options:
            search_result = process.extract(string_to_search, [string.lower() for string in self.options[setting_type]], scorer=fuzz.WRatio, limit=len(self.options[setting_type]))
            for res in search_result:
                if int(res[1]) > min_matching_percentage:
                    raw_results.append((setting_type, self.options[setting_type][res[2]], int(res[1])))
        
        search_result = process.extract(string_to_search, [string.lower() for string in self.alternate_searchable_string], scorer=fuzz.WRatio, limit=len(self.alternate_searchable_string))
        for res in search_result:
            if int(res[1]) > min_matching_percentage:
                raw_results.append(("!alternate_search_string!", self.alternate_searchable_string[res[2]], int(res[1])))

        results = sorted(raw_results, key=lambda x: x[2], reverse=True)[:take_top_n_only if take_top_n_only > 0 else len(raw_results)]
        return results if len(results)>0 else -1

if __name__ == "__main__":
    sr = searchBackend("look and feel", ["456sdf", "green"])
    sr_results = sr.get_search_results("green", 50, 11)
    try:
        for res in sr_results:
            print(res)
    except:
        print("no result found")