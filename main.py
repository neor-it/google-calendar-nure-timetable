from colorama import Fore, init
from internal.schedule.get_schedule import Schedule
from internal.google_calendar.google_calendar import GoogleCalendar
from internal.helpers.get_event_time import get_event_time
from internal.helpers.get_months import get_months
from internal.config import MONTH_NUMBERS

# Initialize colorama
init(autoreset=True)


def main():
    calendar = GoogleCalendar()

    group = input(f'{Fore.LIGHTCYAN_EX}Enter group (e.g. "КІУКІ-22-2, кіукі 22 2, etc"): ')
    months = input(f'{Fore.CYAN}Enter the months for which you want to save the schedule in Google Calendar (e.g. '
                   '"9 10 11 12" or "September October November December". Enter "all" to save the entire schedule): ')
    months = get_months(months)

    month_names = {v: k.capitalize() for k, v in MONTH_NUMBERS.items()}
    month_names_list = [month_names[month] for month in months]
    month_names_str = ', '.join(month_names_list)

    print(f"{Fore.LIGHTYELLOW_EX}Please wait while the schedule for the group '{group}' "
          "for the months {month_names_str} is being parsed and added to the Google Calendar...")

    schedule_instance = Schedule(group, months)
    schedule = schedule_instance.get_schedule()

    if len(schedule) == 0:
        raise ValueError('No schedule found for the specified group and months')

    print(f"{Fore.YELLOW}Schedule for the group '{group}' for the months {month_names_str} "
          "has been successfully parsed!\nSaving the schedule to the Google Calendar...")

    for item in schedule:
        start, end = get_event_time(item)

        calendar.add_event_to_calendar(f"{item['subject']} ({item['type']})",
                                       f"Auditorium: {item['auditorium']}",
                                       start,
                                       end
                                       )
        print(f"{Fore.GREEN}Event '{item['subject']} ({item['type']})' added to the calendar successfully!\n"
              f"Start: {start}\nEnd: {end}\n")

    print(f"{Fore.LIGHTGREEN_EX}Schedule successfully added to the Google Calendar!")


if __name__ == '__main__':
    main()
