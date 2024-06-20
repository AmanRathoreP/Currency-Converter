if __name__ == "__main__":
    from sys import argv as cli_args
    print(cli_args)

    if len(cli_args) == 2 and (cli_args[1] == "--help" or cli_args[1] == "-h"):
        from sys import exit
        #* show help to user
        print("""Below are some valid available cli options
--hide-console/-hc To force no creation of an standalone exe instead forcing creation of multiple files along with an exe, in order for user to run app. This is useful for fast loading of app and efficient updating of app but it's downside is it's large size as compared to standalone exe.
--hide-console/-hc To disable console while running the executable.
--reset-config/-rc To make sure that config file has only and only defaults which are available in "available_options_for_each_setting".json file.
--help/-h To display docs for cli args of the spec file generator.
              """)
        exit()

import os
from PIL import Image
from datetime import datetime
import json

print("Converting PNG to ico for app icon...")
Image.open(os.path.join("assets", "icons", "work-in-progress.png")).save(os.path.join("assets", "icons", "work-in-progress.ico"))
print("Conversion of app icon from  PNG to ico is successful!")

app_name = "Currency Converter"
app_icon_file_path = os.path.join("assets", "icons", "work-in-progress.ico")

spec_template = f"""# -*- mode: python ; coding: utf-8 -*-

# This spec file is auto generated for currency converter app to build exe on {datetime.now()}!

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path

a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=__datas_here__,
    hiddenimports=[],
    hookspath=[kivymd_hooks_path],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=\"{app_name}\",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[\"{app_icon_file_path}\"],
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    hide_console=None,
)
"""

def get_files_name_with_particular_extensions(directory, extensions, search_subdirs = True):
    """
    Get files with particular extensions from a directory and its subdirectories.
    
    Args:
    - directory (list or str): Path(s) to the directory/directories.
    - extensions (list): List of extensions to filter for (without the dot).
    - search_subdirs (bool): Whether to search in subdirectories or not. Default is True.
    
    Returns:
    - filtered_files (list): List of file names with the specified extensions in the directory and its subdirectories.
    """
    if not isinstance(directory, list):
        directory = [directory]

    filtered_files = []
    for dir in directory:
        for root, dirs, files in os.walk(dir):
            if not search_subdirs and root != dir:
                break  # Skip subdirectories if search_subdirs is False
            for file_name in files:
                if any(file_name.endswith('.' + ext) for ext in extensions):
                    filtered_files.append(os.path.join(root, file_name))
    
    return filtered_files

if __name__ == "__main__":
    from sys import argv as cli_args

    for cli_arg in cli_args:
        if cli_arg == "--hide-console" or cli_arg == "-hc":
            print("Setting hide_console to hide-early")
            spec_template = spec_template.replace("hide_console=None,", "hide_console=\'hide-early\',")
       
        elif cli_arg == "--reset-config" or cli_arg == "-rc":
            print("Resetting app settings to default settings")

            #* another workaround is to delete the currency.ini file, as application will automatically create it
            with open("available_options_for_each_setting.json", 'r') as json_file:
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

            with open("currency.ini", 'w') as config_file:
                for section, defaults in defaults_data_json.items():
                    config_file.write('[' + section + ']' + '\n')
                    for sub_setting_name, default_value in defaults.items():
                        config_file.write(sub_setting_name + " = " + default_value + '\n')
                    config_file.write('\n')

        elif cli_arg == "--onedir" or cli_arg == "-od":
            print("Creating one directory exe")
            spec_template = spec_template.replace("    a.binaries,\n    a.datas,\n    [],", "\t[],\t\n\texclude_binaries=True,")
            spec_template = spec_template.replace("    upx_exclude=[],\n    runtime_tmpdir=None,\n", '')
            spec_template +=f"""\ncoll = COLLECT(
\texe,
\ta.binaries,
\ta.datas,
\tstrip=False,
\tupx=True,
\tupx_exclude=[],
\tname=\"{app_name}\",
)"""

    datas = []
    files = get_files_name_with_particular_extensions([os.path.join('.', "src")], ["kv"])
    files.extend(get_files_name_with_particular_extensions([os.path.join('.', "assets")], ["png", "jpg", "svg", "jpeg", "bmp"]))
    files.extend(get_files_name_with_particular_extensions([os.path.join('.')], ["json"], search_subdirs = False))
    files.extend(get_files_name_with_particular_extensions([os.path.join('.')], ["ini"], search_subdirs = False)) # app settings file
    for file_name in files:
        datas.append((file_name, os.path.dirname(file_name)))

    with open("exe_build.spec", 'w') as spec_file:
        spec_file.write(spec_template.replace("datas=__datas_here__,", f"datas={str(datas).replace("\'), (\'", "\'),\n\t\t(\'")},"))
