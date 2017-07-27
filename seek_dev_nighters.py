import requests


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


def get_midnighter_usernames(attempts):
    #FIXME: implement properly
    return [attempt['username'] for attempt in attempts]


if __name__ == '__main__':
  attempt_batches = load_attempts()
  for batch in attempt_batches:
      midnighters = get_midnighter_usernames(batch)
      for username in midnighters:
          print(username)
