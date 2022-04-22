import os
import time

import telegram
from environs import Env

from libs.download_utils import get_caption_text


def main():
    """Upload photos on telegram using bot"""
    env = Env()
    env.read_env()
    telegram_api_token = env("TELEGRAM_API_TOKEN")
    telegram_chat_id = env("TELEGRAM_CHAT_ID")
    sleep_time = env("SLEEP_TIME", 86400)

    while True:
        branches = os.walk("images")
        bot = telegram.Bot(token=telegram_api_token)
        for branch in branches:
            dirpath, dirnames, filenames = branch
            for filename in filenames:
                bot.send_message(chat_id=telegram_chat_id, text="Hello. Today's photos:")
                with open(f'{dirpath}/{filename}', 'rb') as photo:
                    bot.send_photo(chat_id=telegram_chat_id, photo=photo, caption=get_caption_text(photo))
                time.sleep(float(sleep_time))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Forced Server Shutdown')
