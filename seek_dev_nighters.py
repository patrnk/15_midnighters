from datetime import datetime

import requests
import pytz


def load_attempts():
    solution_attempts_url = 'https://devman.org/api/challenges/solution_attempts/'
    params = {'page': 1}
    first_page = requests.get(solution_attempts_url, params).json()
    page_number_limit = first_page['number_of_pages'] + 1
    yield first_page['records']
    for page_number in range(2, page_number_limit):
        params['page'] = page_number
        page = requests.get(solution_attempts_url, params).json()
        yield page['records']


def is_midnighter(unix_timestamp, timezone_name):
    nighttime_hours = (0, 6)
    utc_datetime = datetime.utcfromtimestamp(unix_timestamp).replace(tzinfo=pytz.utc)
    user_timezone = pytz.timezone(timezone_name)
    user_time = utc_datetime.astimezone(user_timezone)
    return nighttime_hours[0] <= user_time.hour <= nighttime_hours[1]


def get_midnighter_usernames(attempts):
    usernames = []
    for attempt in attempts:
        timestamp = attempt['timestamp']
        timezone = attempt['timezone']
        if timestamp and timezone and is_midnighter(timestamp, timezone):
            usernames.append(attempt['username'])
    return usernames


if __name__ == '__main__':
    attempt_batches = load_attempts()
    for batch in attempt_batches:
        midnighters = get_midnighter_usernames(batch)
        for username in midnighters:
            print(username)
