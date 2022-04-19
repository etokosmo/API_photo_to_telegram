import datetime
import os
import random
import re
import time
from pathlib import Path

import requests
import telegram
from environs import Env

IMG_DIR = 'images/nasa/'
PATTERN_DATE_APOD = r'[\d-]+'


def download_img(img_url: str, path_to_download: str) -> None:
    """Download <img_url> in ./images/<path>"""
    try:
        path, name = path_to_download.rsplit('/', 1)
        path += '/'
    except ValueError:
        path = ''
        name = path_to_download
    Path(f"./images/{path}").mkdir(parents=True, exist_ok=True)
    filename = f'./images/{path}{name}'

    response = requests.get(img_url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch() -> None:
    """Download photos from last launch of SpaceX"""
    spacex_url = "https://api.spacexdata.com/v4/launches/latest"

    response = requests.get(spacex_url)
    response.raise_for_status()

    spacex_photos = response.json()['links']['flickr']['original']

    for number, img_url in enumerate(spacex_photos):
        file_extension = get_file_extension(img_url)
        download_img(img_url, f'spacex/spacex{number + 1}{file_extension}')


def get_file_extension(url: str) -> str:
    """Return file extension from URL"""
    filename, file_extension = os.path.splitext(url)
    return file_extension


def get_nasa_apod(token: str, images_count: int | None = None) -> None:
    """Download Astronomy Picture of the Day from NASA"""
    nasa_apod_url = f'https://api.nasa.gov/planetary/apod'

    payload = {
        "api_key": token,
        "count": images_count
    }

    response = requests.get(nasa_apod_url, params=payload)
    response.raise_for_status()

    nasa_apods_json = response.json()
    if images_count is None:
        nasa_apods_json = [nasa_apods_json]
    for nasa_apod in nasa_apods_json:
        try:
            nasa_apod_img_url, nasa_apod_date = nasa_apod["hdurl"], nasa_apod["date"]
        except KeyError:
            nasa_apod_img_url, nasa_apod_date = nasa_apod["url"], nasa_apod["date"]
        file_extension = get_file_extension(nasa_apod_img_url)
        download_img(nasa_apod_img_url, f'nasa/apod_nasa_{nasa_apod_date}{file_extension}')


def get_nasa_epic(token: str, images_count: int) -> None:
    """Download Earth Polychromatic Imaging Camera from NASA"""
    nasa_epic_url = f'https://api.nasa.gov/EPIC/api/natural'

    payload = {
        "api_key": token,
    }

    response = requests.get(nasa_epic_url, params=payload)
    response.raise_for_status()

    for content in response.json()[:images_count]:
        date, image = content['date'], content['image']

        image_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        nasa_epic_img_url = f'https://api.nasa.gov/EPIC/archive/natural/{image_date.year}/{image_date.strftime("%m")}' \
                            f'/{image_date.day}/png/{image}.png'

        response_img = requests.get(nasa_epic_img_url, params=payload)
        response_img.raise_for_status()

        download_img(response_img.url, f'nasa/epic_nasa_{image}.png')


def main():
    """Download images and upload them on telegram using bot"""
    env = Env()
    env.read_env()
    nasa_api_token = env("NASA_API_TOKEN")
    telegram_api_token = env("TELEGRAM_API_TOKEN")
    telegram_chat_id = env("TELEGRAM_CHAT_ID")
    sleep_time = env("SLEEP_TIME", 86400)
    while True:
        get_nasa_apod(nasa_api_token)
        get_nasa_epic(nasa_api_token, 1)

        photo = open(os.path.join(IMG_DIR, random.choice(os.listdir(IMG_DIR))), 'rb')
        if 'epic' in photo.name:
            caption_text = 'Earth Polychromatic Imaging Camera from NASA'
        elif 'apod' in photo.name:
            match_date = re.search(f'{PATTERN_DATE_APOD}', f'{photo.name}')
            date_apod = match_date[0] if match_date else ''
            caption_text = f'Astronomy Picture of the Day {date_apod} from NASA'
        else:
            caption_text = None
        bot = telegram.Bot(token=telegram_api_token)
        bot.send_message(chat_id=telegram_chat_id, text="Hello. Today's photo of the day")
        bot.send_photo(chat_id=telegram_chat_id, photo=photo, caption=caption_text)
        time.sleep(float(sleep_time))


if __name__ == "__main__":
    main()
