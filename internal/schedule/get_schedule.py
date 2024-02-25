from internal.schedule.get_groups import Groups
from bs4 import BeautifulSoup
import requests
import urllib.request
from datetime import datetime, timedelta
import internal.config as config
import calendar


class Schedule:
    def __init__(self, group_name, months):
        self.group_instance = Groups()
        self.groups = self.group_instance.get_all_groups()
        self.group_id = self.__get_group_id(group_name)
        self.weeks = self.__get_weeks(months)
        self.schedule = {}

    def get_schedule(self):
        """Returns a list of dictionaries with the schedule for the current weeks"""
        schedule = []

        for week in self.weeks:
            monday = week[0].strftime("%d.%m.%Y")
            saturday = week[-1].strftime("%d.%m.%Y")

            url = (f'https://cist.nure.ua/ias/app/tt/f?p=778:201:1737924905226049:::201:'
                   f'P201_FIRST_DATE,P201_LAST_DATE,P201_GROUP,P201_POTOK:{monday},{saturday},{self.group_id},0:')

            response = requests.get(url, headers=config.HEADERS, proxies=urllib.request.getproxies())
            soup = BeautifulSoup(response.content, 'html.parser')

            table_schedule = soup.findAll('table', class_='MainTT')

            if len(table_schedule) == 0:
                raise ValueError('No schedule found for the given group')

            items = table_schedule[0].findAll('tr')

            day, date = None, None

            for item in items:
                if item.find('td', class_='date'):
                    day = item.find('td', class_='date').text
                    date = item.find_all('td')[-1].text
                elif item.find('td', class_='left'):
                    number = item.find('td', class_='left').text
                    time = item.find('td', class_='left').find_next_sibling().text

                    if '*' in item.find_all('td')[-1].find('a').text:
                        subjects = item.find_all('td')[-1].text.split()

                        for i in range(0, len(subjects), 4):
                            subject = subjects[i]
                            subject_type = subjects[i + 1]
                            auditorium = subjects[i + 2] + ' ' + subjects[i + 3]
                            entry = {
                                'number_pair': number,
                                'date': date,
                                'day': day,
                                'time': time,
                                'subject': subject.replace('*', ''),
                                'type': subject_type,
                                'auditorium': auditorium.replace(';', '').strip()
                            }
                            schedule.append(entry)
                        continue

                    subject = item.find_all('td')[-1].find('a').text.replace('\n', '').split()[0]
                    subject_type = item.find_all('td')[-1].find('a').text.replace('\n', '').split()[-1]
                    auditorium = item.find_all('td')[-1].text.split()[-1]

                    entry = {
                        'number_pair': number,
                        'date': date,
                        'day': day,
                        'time': time,
                        'subject': subject,
                        'type': subject_type,
                        'auditorium': auditorium
                    }

                    schedule.append(entry)

        return schedule

    @staticmethod
    def __get_weeks(months):
        weeks = []
        for month in months:
            year = datetime.now().year
            _, num_days = calendar.monthrange(year, month)
            first_day = datetime(year, month, 1).date()
            last_day = datetime(year, month, num_days).date()

            # If the first day of the month is not a Sunday, go back to the previous Sunday
            if first_day.weekday() != 6:
                first_day -= timedelta(days=(first_day.weekday() + 1))

            # Calculate the number of weeks in the month
            num_weeks = (last_day - first_day).days // 7 + 1

            for i in range(num_weeks):
                start_day = first_day + timedelta(days=i * 7)
                week = [start_day + timedelta(days=j) for j in range(7)]
                if week not in weeks:
                    weeks.append(week)

        return weeks

    def __get_group_id(self, group_name):
        return self.groups.get(group_name.upper().replace(' ', '-'), None)
