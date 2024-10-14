#!/bin/bash
# ---------------------------------------------------------------
# Example script to tail run_monitor_infinite.log
# if still running, do not start new one
# Add to your crontab to run once per hour to restart after crashes or reboot, e.g.
# 8 * * * * ~/tail2GoogleSheet/tail_run_monitor_infinite.log.sh >> ~/tail2GoogleSheet/crontab_tail_run_monitor_infinite.log 2>&1
# @reboot sleep 125 && ~/tail2GoogleSheet/tail_run_monitor_infinite.log.sh >> ~/tail2GoogleSheet/crontab_tail_run_monitor_infinite.log 2>&1
#
# Notes:
# Make sure to make tail_run_monitor_infinite.log.sh executable (chmod +x)
# Make sure to create once a Google Spreadsheet with name run_monitor_infinite.log:
# - In Google Spreadsheet, create an empty Google Spreadsheet with the name: run_monitor_infinite.log
# - Go to your spreadsheet and share it with the client_email inside ~/.config/gspread/service_account.json
# ---------------------------------------------------------------
script_name=$(basename -- "$0")

now=$(date)
if pidof -x "$script_name" -o $$ >/dev/null
then
    echo "$now: $script_name still running"
else
    echo "$now: starting $script_name"
    /usr/bin/python ~/tail2GoogleSheet/tail_to_google_sheet.py -f -50 ~/hyundai_kia_connect_monitor/run_monitor_infinite.log
fi
