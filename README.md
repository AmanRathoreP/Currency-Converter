<div align="center">
  <h1>Currency Converter</h1>
</div>

<p align="center">
  This is a free open-source cross-platform app that assist users in currency conversion
</p>


# Features

* Currency Conversion
* Cryptocurrency Support
* Auto Update Currency Value
* Custom Currencies
* No Ads
* Modern UI
* Customisable look-and-feel
* ...

# Platforms

* Windows
* Android
* ...

# Quick start

## Pre-Compiled download
...

## Self-Build

### Windows(exe)

Run the below commands one by one

* Cloning the repository
  ```
  git clone https://github.com/AmanRathoreP/Currency-Converter.git
  ```
* Navigating to the project's directory
  ```
  cd "Currency-Converter"
  ```
* Creating python's virtual environment
  ```
  python -m venv python_virtual_environment_for_app
  ```
* Activating `python_virtual_environment_for_app` virtual environment
  ```
  python_virtual_environment_for_app\Scripts\activate
  ```
* Adding/Downloading necessary packages
  ```
  pip install -r requirements.txt
  ```
* Generate `.spec` using below command
  ```
  python generate_spec_for_exe.py --onedir --reset-config
  ```
  > Note that you can also use command line args like `--onedir`/`-od`, `--hide-console`/`-hc`.
    * `--help`/`-h` To display available cli args for `generate_spec_for_exe.py` along with their use(s).
    * `--onedir`/`-od` means that instead of an standalone exe user will be required to have bunch of file in order to run the app.
    * `--hide-console`/`-hc` means that no console will be displayed to the user after exe is created.
    * `--reset-config`/`-rc` make sure that config file has only and only defaults set by user in `available_options_for_each_setting.json` file.
* Build exe using below command
  ```
  python -m PyInstaller exe_build.spec
  ```

# Contributing [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](issues.md)

Thank you for considering contributing to Computer Based Test Emulator

First note we have a code of conduct, please follow it in all your interactions with the program files.

We welcome any type of contribution, _not only code_. You can help with:
- **QA**: File bug reports, the more details you can give the better (e.g. images or videos)
- **New Features**: You can suggest an modifications or just ask for advancements in the old features of application.
- **Code**: Take a look at the [open issues](issues.md). Even if you can't write the code yourself, you can comment on them, showing that you care about a given issue matters. It helps us to handel them.

# Demo

...

# Author

- [@Aman](https://www.github.com/AmanRathoreP)
   - [GitHub](https://www.github.com/AmanRathoreP)
   - [Telegram](https://t.me/aman0864)
   - Email -> *aman.proj.rel@gmail.com*

# Facts
* ...

# Thanks to
* For icons
  * <a href="https://www.flaticon.com/free-icons/under-construction" title="under construction icons">Under construction icons created by Freepik - Flaticon</a>
  * <a href="https://www.flaticon.com/free-icons/settings" title="settings icons">Settings icons created by dmitri13 - Flaticon</a>


# License

[GNU Affero General Public License v3.0](https://choosealicense.com/licenses/agpl-3.0/) | [LICENSE](LICENSE/)

Copyright (c) 2024, Aman Rathore
