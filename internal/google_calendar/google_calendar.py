from google.oauth2 import service_account
from googleapiclient.discovery import build
import internal.config as config


class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = 'credentials.json'

    def __init__(self):
        self.calendar = config.CALENDAR

        self.credentials = service_account.Credentials.from_service_account_file(
            filename=self.SERVICE_ACCOUNT_FILE,
            scopes=self.SCOPES
        )
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self):
        """
        Adds a calendar to the list of calendars. Calendar must be added only once before adding events.
        Example of calendar_id: '32c60sb3704d24e333e11c843861934ce9cv2d949b2cc0ce0e5ceb2821bf386d@group.calendar.google.com'
        """
        calendar_entry = {
            'id': self.calendar,
        }

        return self.service.calendarList().insert(body=calendar_entry).execute()

    def add_event_to_calendar(self, summary, description, start, end):
        """
        Adds an event to the specified calendar. Example of required parameters:
        summary: 'My event'
        description: 'My description'
        start: '2024-02-23T07:45:00+02:00'
        end: '2024-02-23T09:30:00+02:00'
        """
        event_body = self.__create_body(summary, description, start, end)
        return self.__add_event(event_body)

    def __add_event(self, body):
        return self.service.events().insert(calendarId=self.calendar, body=body).execute()

    @staticmethod
    def __create_body(summary, description, start, end):
        return {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start,  # example: 2024-02-23T07:45:00+02:00
            },
            'end': {
                'dateTime': end,  # example: 2024-02-23T09:30:00+02:00
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 24 hours before
                    {'method': 'popup', 'minutes': 10},  # 10 minutes before
                ],
            },
        }

    def clear_calendar_events(self):
        """
        Deletes all events from the calendar.

        Returns True on success, False otherwise.
        """
        try:
            events = self.service.events().list(calendarId=self.calendar).execute()

            for event in events.get('items', []):
                event_id = event['id']
                self.service.events().delete(calendarId=self.calendar, eventId=event_id).execute()
            return True

        except Exception as e:
            print(f"An error occurred while clearing calendar events: {e}")
            return False
