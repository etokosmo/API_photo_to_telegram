import os
import time

import telegram
from environs import Env

from fetch_nasa import main as fetch_nasa_main
from fetch_spacex import main as fetch_spacex_main
from libs.download_utils import get_caption_text

SEARCH_ROOT_FOLDER = "images"


def main():
    """Upload photos on telegram using bot"""
    env = Env()
    env.read_env()
    telegram_api_token = env("TELEGRAM_API_TOKEN")
    telegram_chat_id = env("TELEGRAM_CHAT_ID")
    sleep_time = env.int("SLEEP_TIME", 86400)
    fetch_spacex_main()
    fetch_nasa_main()

    while True:
        branches = os.walk(SEARCH_ROOT_FOLDER)
        bot = telegram.Bot(token=telegram_api_token)
        for branch in branches:
            dirpath, dirnames, filenames = branch
            for filename in filenames:
                bot.send_message(chat_id=telegram_chat_id, text="Hello. Today's photos:")
                with open(f'{dirpath}/{filename}', 'rb') as photo:
                    bot.send_photo(chat_id=telegram_chat_id, photo=photo, caption=get_caption_text(photo))
                time.sleep(sleep_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Forced Server Shutdown')
