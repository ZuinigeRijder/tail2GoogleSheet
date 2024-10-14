@echo on
cd /d C:\Users\Rick\git\tail2GoogleSheet
mypy tail_to_google_sheet.py | egrep -v "^Found|gspread|: note:"

pause