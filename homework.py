import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv
from requests import RequestException

log = logging.getLogger(__name__)
log.setLevel(level=logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

fh = logging.FileHandler('bot.log')
fh.setLevel(level=logging.DEBUG)
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(level=logging.DEBUG)
ch.setFormatter(formatter)

log.addHandler(fh)
log.addHandler(ch)

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

bot = telegram.Bot(TELEGRAM_TOKEN)

url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
url_2 = 'https://praktiсum.yandex.ru/api/user_api/homework_statuses/'
headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}

sleep_sec = 10 * 60


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    if homework_name is None:
        return None
    status = homework.get('status')
    if status is None:
        return None
    if status == 'rejected':
        verdict = 'К сожалению, в работе нашлись ошибки.'
    elif status == 'reviewing':
        verdict = 'Работа на проверке'
    else:
        verdict = 'Ревьюеру всё понравилось, работа зачтена!'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homeworks(current_timestamp):
    if current_timestamp is None:
        log.debug('current_timestamp is None')
        current_timestamp = int(time.time()) - sleep_sec
    payload = {'from_date': current_timestamp}
    try:
        homework_status = requests.get(
            url, headers=headers, params=payload
        )
    except:
        try:
            homework_status = requests.get(
                url_2, headers=headers, params=payload
            )
        except RequestException as e:
            message = f'API returned exception: {e}'
            log.error(message)
            raise e
    return homework_status.json()


def send_message(message):
    log.info(f'Send message: {message}')
    return bot.send_message(CHAT_ID, message)


def main():
    current_timestamp = int(time.time())
    log.debug('Start app')

    while True:
        try:
            log.debug(f'current_timestamp: {current_timestamp}')
            homeworks_statuses = get_homeworks(current_timestamp)
            homeworks = homeworks_statuses.get('homeworks', None)
            current_timestamp = homeworks_statuses.get('current_date', None)
            log.debug(f'homeworks: {homeworks}')
            if len(homeworks) > 0 and homeworks is not None:
                last_homework = homeworks[0]
                message = parse_homework_status(last_homework)
                send_message(message)
            time.sleep(sleep_sec)

        except Exception as e:
            message = f'Бот упал с ошибкой: {e}'
            log.error(message)
            send_message(message)
            time.sleep(5)


if __name__ == '__main__':
    main()
