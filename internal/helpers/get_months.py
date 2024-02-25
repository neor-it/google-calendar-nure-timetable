from internal.config import MONTH_NUMBERS


def get_months(months):
    if months.lower() == 'all':
        return list(range(1, 13))

    months_list = months.split()

    for i in range(len(months_list)):
        if months_list[i].isdigit():
            months_list[i] = int(months_list[i])
            continue

        months_list[i] = MONTH_NUMBERS[months_list[i].lower()]

    return months_list
