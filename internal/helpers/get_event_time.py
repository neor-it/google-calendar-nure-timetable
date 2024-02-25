from datetime import datetime


def get_event_time(item) -> tuple:
    """
    Takes a dictionary of the form {'date': '19.02.2024', 'time': '07:45 09:20'}
    and returns a tuple of the form (2024-02-23T07:45:00+02:00, 2024-02-23T09:20:00+02:00)
    """

    try:
        if item is None:
            raise ValueError("Item is None")

        if 'time' not in item or 'date' not in item:
            raise KeyError("Field 'time' or 'date' not found in item")

        start_time, end_time = item['time'].split()

        start_date_time_str = f"{item['date']} {start_time}"
        end_date_time_str = f"{item['date']} {end_time}"

        start_date_time_obj = datetime.strptime(start_date_time_str, "%d.%m.%Y %H:%M")
        end_date_time_obj = datetime.strptime(end_date_time_str, "%d.%m.%Y %H:%M")

        formatted_start_date_time = start_date_time_obj.strftime("%Y-%m-%dT%H:%M:%S+02:00")
        formatted_end_date_time = end_date_time_obj.strftime("%Y-%m-%dT%H:%M:%S+02:00")

        return formatted_start_date_time, formatted_end_date_time

    except Exception as e:
        print(f"Error: {e}")
        return None, None


if __name__ == '__main__':
    item = {'date': '19.02.2024', 'time': '07:45 09:20'}
    start, end = get_event_time(item)
    print(start, end)  # Output: 2024-02-19T07:45:00+02:00 2024-02-19T09:20:00+02:00
