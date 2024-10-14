#!/usr/bin/env python
# == tail_to_google_sheet.py Author: Zuinige Rijder ===========================
# Simple Python3 script to follow a file with tail -f like command
# and update google sheet with same basename
#
# reused python-tail implementation with slight adaptations from:
# Author - Kasun Herath <kasunh01 at gmail.com>
# Source - https://github.com/kasun/python-tail
#
# python-tail source adapted by Zuinige Rijder with the following changes:
# - added encoding="utf-8" in open file
# - do not go to the end of file, but also callback from the beginning
# - call the callback when follow() wants to go to sleep, so callback can flush a buffer
#   but only when there was content in-between
#
# Source - https://github.com/zuinigerijder/tail2GoogleSheet

# pylint: disable=broad-except,global-statement

# ========================== python-tail ======================================
"""
Python-Tail - Unix tail follow implementation in Python.

python-tail can be used to monitor changes to a file.

Example:
    import tail

    # Create a tail instance
    t = tail.Tail('file-to-be-followed')

    # Register a callback function to be called when a new line is found
    # in the followed file.
    # If no callback function is registered, new lines would be printed to standard out.
    t.register_callback(callback_function)

    # Follow the file with 5 seconds as sleep time between iterations.
    # If sleep time is not provided 1 second is used as the default time.
    t.follow(s=5) """

import os
import sys
import time

# extra imports for tail_to_google_sheet.py
from collections import deque
import traceback
from datetime import datetime
import typing
import gspread  # external dependency, pip install gspread>=5.6.2


class Tail(object):
    """Represents a tail command."""

    def __init__(self, tailed_file):
        """Initiate a Tail instance.
        Check for file validity, assigns callback function to standard out.
        Arguments:
            tailed_file - File to be followed.
        """

        self.check_file_validity(tailed_file)
        self.tailed_file = tailed_file
        self.callback = sys.stdout.write

    def follow(self, s=1):
        """
        Do a tail follow. If a callback function is registered it is called
        with every new line.
        Else printed to standard out.

        Arguments:
            s - Number of seconds to wait between each iteration; Defaults to 1.
        """

        with open(self.tailed_file, encoding="utf-8") as file_:
            # Go to the end of file
            # Zuinige Rijder: commented next line, existing content wanted too
            # file_.seek(0, 2)
            content_after_sleep = False
            while True:
                curr_position = file_.tell()
                line = file_.readline()
                if not line:
                    file_.seek(curr_position)
                    # Zuinige Rijder:
                    # possibility for callback to write buffer before sleep
                    # but only when there was content in-between
                    if content_after_sleep:
                        content_after_sleep = False
                        self.callback(line)
                    time.sleep(s)
                else:
                    content_after_sleep = True
                    self.callback(line)

    def register_callback(self, func):
        """Overrides default callback function to provided function."""
        self.callback = func

    def check_file_validity(self, file_):
        """Check whether the a given file exists, readable and is a file"""
        if not os.access(file_, os.F_OK):
            raise TailError(f"File '{file_}' does not exist")
        if not os.access(file_, os.R_OK):
            raise TailError(f"File '{file_}' not readable")
        if os.path.isdir(file_):
            raise TailError(f"File '{file_}' is a directory")


class TailError(Exception):
    """TailError"""

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


# ========================== python-tail ======================================


# ========================== tail_to_google_sheet.py ==========================
def log(msg: str) -> None:
    """log a message prefixed with a date/time format yyyymmdd hh:mm:ss"""
    print(datetime.now().strftime("%Y%m%d %H:%M:%S") + ": " + msg)


def usage(msg: str):
    """usage"""
    if msg != "":
        log(f"ERROR: {msg}")
    print(
        """
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
"""
    )
    sys.exit(-1)


# Options
BUFFER_MAX_LEN = 100
FOLLOW = False
INPUT_FILENAME = ""


def get_options():
    """get options"""
    buffer_max_len = 100
    follow = False
    input_filename = ""
    for i in range(1, len(sys.argv)):
        if sys.argv[i].lower() == "-f":
            follow = True
        elif sys.argv[i].startswith("-"):
            splitted = sys.argv[i].split("-")
            if len(splitted) != 2:
                usage(f"Invalid option: {sys.argv[i]}")
            n = splitted[1]
            if not n.isdigit():
                usage(f"Expected integer: {sys.argv[i]}")
            buffer_max_len = int(n)
            if buffer_max_len > 1000:
                usage("Maximum -n option is 1000")
        else:
            if input_filename != "":
                usage("Only one filename expected")
            input_filename = sys.argv[i].strip()

    if input_filename == "":
        usage("No FILE specified")

    if not os.access(input_filename, os.R_OK):
        usage(f"File {input_filename} is not readable or does not exist")

    return buffer_max_len, follow, input_filename


BUFFER_MAX_LEN, FOLLOW, INPUT_FILENAME = get_options()
SHEET: typing.Any = None
LINENO = 1
BUFFER: deque[str] = deque(maxlen=BUFFER_MAX_LEN)


def batch_update_array(array: list) -> None:
    """batch_update_array"""
    if len(array) > 0:
        retries = 5
        while retries > 0:
            try:
                SHEET.batch_update(array)
                retries = 0
            except Exception as ex:
                log("Exception: " + str(ex))
                traceback.print_exc()
                retries -= 1
                time.sleep(60)


def output_queue_to_sheet() -> None:
    """output queue to sheet"""
    array = []
    row = 1
    SHEET.clear()
    for line in BUFFER:
        splitted = line.split(":", 1)  # split line in lineno and line
        array.append(
            {
                "range": f"A{row}:B{row}",
                "values": [[splitted[0], splitted[1]]],
            }
        )
        row += 1

    batch_update_array(array)


def handle_line(line):
    """handle line"""
    global LINENO
    if not line:  # no new data
        output_queue_to_sheet()
        if not FOLLOW:
            sys.exit(0)  # exit program, no -f specified
        return

    line = line.rstrip()  # remove trailing spaces and newlines
    if len(BUFFER) >= BUFFER_MAX_LEN:
        BUFFER.popleft()

    BUFFER.append(f"{LINENO}: {line}")  # prefix with linenumber
    LINENO += 1


def tail_setup():
    """tail setup"""
    tail = Tail(INPUT_FILENAME)
    tail.register_callback(handle_line)
    tail.follow(s=60)  # check every minute


def sheet_setup() -> None:
    """sheet_setup"""
    global SHEET

    client = gspread.service_account()

    spreadsheet_name = os.path.basename(INPUT_FILENAME)
    retries = 5
    while retries > 0:
        try:
            spreadsheet = client.open(spreadsheet_name)
            SHEET = spreadsheet.sheet1
            SHEET.clear()
            SHEET.resize(rows=BUFFER_MAX_LEN, cols=2)
            retries = 0
        except Exception as ex:
            log("Exception: " + str(ex))
            traceback.print_exc()
            retries -= 1
            time.sleep(60)


sheet_setup()
tail_setup()
# ========================== tail_to_google_sheet.py ==========================
