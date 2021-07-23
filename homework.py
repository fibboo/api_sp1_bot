import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv


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


def parse_homework_status(homework):
    homework_name = homework['lesson_name']
    status = homework['status']
    reviewer_comment = homework['reviewer_comment']
    log.debug(f'homework_name: {status}')
    if status == 'rejected':
        verdict = 'К сожалению, в работе нашлись ошибки.'
    elif status == 'reviewing':
        message = (f'Lesson name: {homework_name}\n'
                   f'Status: {status}\n'
                   f'Reviewer comment: {reviewer_comment}')
        send_message(message)
    else:
        verdict = 'Ревьюеру всё понравилось, работа зачтена!'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homeworks(current_timestamp):
    url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    payload = {'from_date': current_timestamp}
    homework_status = requests.get(
        url, headers=headers, params=payload
    )
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
            homeworks = homeworks_statuses['homeworks']
            current_timestamp = homeworks_statuses['current_date']
            log.debug(f'last homeworks: {homeworks}')
            if len(homeworks) > 0:
                last_homework = homeworks[0]
                message = parse_homework_status(last_homework)
                send_message(message)
            time.sleep(5 * 60)

        except Exception as e:
            message = f'Бот упал с ошибкой: {e}'
            log.error(message)
            send_message(message)
            time.sleep(5)


if __name__ == '__main__':
    main()
