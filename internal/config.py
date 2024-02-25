import configparser

config = configparser.ConfigParser()
config.read('config.ini')

CALENDAR = config['NURESCHEDULE']['CALENDAR']

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

MONTH_NUMBERS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
                 'september': 9, 'october': 10, 'november': 11, 'december': 12}
