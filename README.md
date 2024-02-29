# Nure Timetable in Google Calendar
This is a simple Python script that allows you to import your NURE timetable into Google Calendar.

## Install
1. Install Python 3.8 or higher from the [official website](https://www.python.org/downloads/)
2. Clone the repository
```bash
git clone github.com/neor-it/google-calendar-nure-timetable.git
```
3. Go to the project directory
```bash
cd google-calendar-nure-timetable
```
4. Install the required packages
```bash
pip install -r requirements.txt
```
5. Create a new project in the [Google Cloud Console](https://console.cloud.google.com/)
6. Enable the Google Calendar API
7. Create a new Service Account and give it the `Editor` role in the project 
8. Download the client secret JSON file and save it as `credentials.json` in the project directory
9. Create a new calendar in Google Calendar and save its ID in the `CALENDAR` variable in the `config.ini` file.
10. Add your Service Account Email to 'Share with specific people' in Google Calendar and set permission to 'Make changes'.
11. Run the script
```bash
python main.py
```

## Usage
1. Run the script
2. Enter group (e.g. `КІУКІ-22-2`, `КІУКІ 22 2`, `кіукі 22 2`)
3. Enter the months for which you want to save the schedule in Google Calendar (e.g. `9 10 11 12` or `September October November December`. Enter `all` to save the entire schedule).

**⚠️ ATTENTION!** In current version the script will delete all events from the calendar (only for the calendar you created).
Your other calendars won't be affected.

## Contact

Responsible Ruslan Yakymenko.
The primary contact for this project is [t.me/RulanYakymenko](t.me/RulanYakymenko)
