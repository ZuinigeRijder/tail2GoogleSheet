[tail2GoogleSheet](#tail2GoogleSheet)
- [Summary](#summary)
- [Quick start](#quick-start)
- [tail\_to\_google\_sheet.py](#tail_to_google_sheetpy)
- [Configuration of gspread for "python tail\_to\_google\_sheet.py"](#configuration-of-gspread-for-python-tail_to_google_sheetpy)
- [Example crontab to run on Raspberry Pi or another linux system](#example-crontab-to-run-on-raspberry-pi-or-another-linux-system)

---
# Summary

Pyton script to tail content of file and optionally follow subsequent updates and send them to a Google Sheet with the same filename (without directory part). Great to be able to look at the last -n lines of a log-file or any other file on your smartphone, tablet or computer without logging in to the server.

````
Usage: python tail_to_google_sheet.py [OPTION]... FILE
   -f            output appended data as the file grows
   -n            output the last N lines. Default is 100, maximum is 1000

Example: python tail_to_google_sheet.py -f -200 test.log
````

---
# Quick start

- Make sure you have installed Python 3.9 or higher. [Here is more information about installing Python](https://realpython.com/installing-python/)
- see [requirements.txt](https://raw.githubusercontent.com/ZuinigeRijder/tail2GoogleSheet/main/requirements.txt) for version numbers of needed packages
- pip install gspread and [configure package gspread once](#configuration-of-gspread-for-python-tail_to_google_sheetpyy)
- create and share a Google Spreadsheet with the same name as the FILE to follow and share it with the client_email inside service_account.json
- run [tail_to_google_sheet.py](#tail_to_google_sheetpy) in the console or via e.g. [crontab](#example-crontab-to-run-on-raspberry-pi-or-another-linux-system)

---
# tail_to_google_sheet.py

```
Usage: python tail_to_google_sheet.py [OPTION]... FILE
   -f            output appended data as the file grows
   -n            output the last N lines. Default is 100, maximum is 1000

Example: python tail_to_google_sheet.py -f -200 test.log

Description: tail file content into a google sheet with same filename:
- filename of FILE (without path) is used as google sheet name
- google sheet will have -n rows and 2 columns and contains last -n rows:
  -- column A is line number in FILE
  -- column B is line
- once per minute the FILE is checked for new content when -f is specified
- you need to configure gspread once (see Configuration of gspread)
- you need to create the google sheet name manually once
  and share it with the service account client_email address in json file, e.g.:
  -- Linux  : ~/.config/gspread/service_account.json
  -- Windows: %APPDATA%/gspread/service_account.json

Configuration of gspread:
For updating a Google Spreadsheet, tail_to_google_sheet.py is using the package gspread.
For Authentication with Google Spreadsheet you have to configure
authentication for gspread. This authentication configuration is described here:
    https://docs.gspread.org/en/latest/oauth2.html

The tail_to_google_sheet.py script uses access to the Google spreadsheets on behalf of
a bot account using Service Account.

Follow the steps in this link above, here is the summary of these steps:

1 Enable API Access for a Project
    - Head to Google Developers Console: https://console.developers.google.com/
        and create a new project (or select the one you already have).
    - In the box labeled "Search for APIs and Services",
        search for "Google Drive API" and enable it.
    - In the box labeled "Search for APIs and Services",
        search for "Google Sheets API" and enable it
2 For Bots: Using Service Account
    - Go to "APIs & Services > Credentials" and choose
        "Create credentials > Service account key".
    - Fill out the form
    - Click "Create" and "Done".
    - Press "Manage service accounts" above Service Accounts.
    - Press on : near recently created service account and select
        "Manage keys" and then click on "ADD KEY > Create new key".
    - Select JSON key type and press "Create".
    - You will automatically download a JSON file with credentials
    - Remember the path to the downloaded credentials json file.
        Also, in the next step you will need the value of client_email from this file.
    - Move the downloaded json file to:
        -- Linux: ~/.config/gspread/service_account.json
        -- Windows: %APPDATA%/gspread/service_account.json
3 Setup a Google Spreasheet with FILE to be tailed:
    - In Google Spreadsheet, create an empty Google Spreadsheet with the FILE name
    - Go to your spreadsheet and share it with the client_email from the step above
        (client_email inside service_account.json)
```

---
# Configuration of gspread for "python tail_to_google_sheet.py"
For updating a Google Spreadsheet, tail_to_google_sheet.py is using the package gspread.
For Authentication with Google Spreadsheet you have to configure authentication for gspread.
This [authentication configuration is described here](https://docs.gspread.org/en/latest/oauth2.html)

The tail_to_google_sheet.py script uses access to the Google spreadsheets on behalf of a bot account using Service Account.

Follow the steps in this link above, here is the summary of these steps:
- Enable API Access for a Project
- - Head to [Google Developers Console](https://console.developers.google.com/) and create a new project (or select the one you already have).
- - In the box labeled "Search for APIs and Services", search for "Google Drive API" and enable it.
- - In the box labeled "Search for APIs and Services", search for "Google Sheets API" and enable it
- For Bots: Using Service Account
- - Go to "APIs & Services > Credentials" and choose "Create credentials > Service account key".
- - Fill out the form
- - Click "Create" and "Done".
- - Press "Manage service accounts" above Service Accounts.
- - Press on : near recently created service account and select "Manage keys" and then click on "ADD KEY > Create new key".
- - Select JSON key type and press "Create".
- - You will automatically download a JSON file with credentials
- - Remember the path to the downloaded credentials json file. Also, in the next step you will need the value of client_email from this file.
- - Move the downloaded json file to ~/.config/gspread/service_account.json. Windows users should put this file to %APPDATA%\gspread\service_account.json.
- Setup a Google Spreadsheet to be updated by tail_to_google_sheet.py (the same filename without path as the file to tail)
- - In Google Spreadsheet, create an empty Google Spreadsheet and give it the same name as the filename to tail (without path)
- - Go to your spreadsheet and share it with the client_email from the step above (inside service_account.json)
- run "python tail_to_google_sheet.py -20 FILE" and if everything is correct, the Sheet will be updated with the -20 lines of content of the FILE you are tailing.
- configure to run "python tail_to_google_sheet.py" automatically or run it in a console on the server.

---
# Example crontab to run on Raspberry Pi or another linux system

Example script [tail_monitor.csv.sh](https://raw.githubusercontent.com/ZuinigeRijder/tail2GoogleSheet/main/examples/tail_monitor.csv.sh) to run tail_to_google_sheet.py ~/hyundai_kia_connect_monitor/monitor.csv on a linux based system. This example is following the monitor.csv file generated by [monitor.py](https://github.com/ZuinigeRijder/hyundai_kia_connect_monitor?tab=readme-ov-file#monitorpy). The same approach can be used for any other file you want to follow, this is just an example to follow monitor.csv.

Steps:
- create a directory tail2GoogleSheet in your home directory
- copy tail_to_google_sheet.py and tail_monitor.csv.sh in this tail2GoogleSheet directory
- chmod + x tail_monitor.csv.sh
- make sure you have created the spreadsheet with name monitor.csv once and shared with the bot account


Add the following lines in your crontab -e to run it once per hour 8 minutes later or 125 seconds after reboot (crontab -e):
```
8 * * * * ~/tail2GoogleSheet/tail_monitor.csv.sh >> ~/tail2GoogleSheet/crontab_tail_monitor.csv.log 2>&1
@reboot sleep 125 && ~/tail2GoogleSheet/tail_monitor.csv.sh >> ~/tail2GoogleSheet/crontab_tail_monitor.csv.log 2>&1
```

This is the content of tail_monitor.csv.sh:
````
#!/bin/bash
# ---------------------------------------------------------------
# Example script to tail monitor.csv
# if still running, do not start new one
# Add to your crontab to run once per hour to restart after crashes or reboot, e.g.
# 8 * * * * ~/tail2GoogleSheet/tail_monitor.csv.sh >> ~/tail2GoogleSheet/crontab_tail_monitor.csv.log 2>&1
# @reboot sleep 125 && ~/tail2GoogleSheet/tail_monitor.csv.sh >> ~/tail2GoogleSheet/crontab_tail_monitor.csv.log 2>&1
#
# Notes:
# Make sure to make tail_monitor.csv.sh executable (chmod +x)
# Make sure to create once a Google Spreadsheet with name monitor.csv:
# - In Google Spreadsheet, create an empty Google Spreadsheet with the name: monitor.csv
# - Go to your spreadsheet and share it with the client_email inside ~/.config/gspread/service_account.json
# ---------------------------------------------------------------
script_name=$(basename -- "$0")

now=$(date)
if pidof -x "$script_name" -o $$ >/dev/null
then
    echo "$now: $script_name still running"
else
    echo "$now: starting $script_name"
    /usr/bin/python ~/tail2GoogleSheet/tail_to_google_sheet.py -f -50 ~/hyundai_kia_connect_monitor/monitor.csv
fi
````

Another example is [tail_run_monitor_infinite.log.sh](https://raw.githubusercontent.com/ZuinigeRijder/tail2GoogleSheet/main/examples/tail_run_monitor_infinite.log.sh) which is following [~/hyundai_kia_connect_monitor/run_monitor_infinite.log](https://github.com/ZuinigeRijder/hyundai_kia_connect_monitor?tab=readme-ov-file#raspberry-pi-configuration)
