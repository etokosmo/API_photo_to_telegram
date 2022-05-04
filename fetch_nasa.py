import datetime
from pathlib import Path

import requests
from environs import Env

from libs.download_utils import download_img, get_file_extension

COUNT_OF_DOWNLOADED_IMAGES_APOD = None
COUNT_OF_DOWNLOADED_IMAGES_EPIC = 1
DOWNLOAD_PATH = "./images/nasa"


def get_nasa_apod(token: str, path: str, images_count: int | None = None) -> None:
    """Download One or More Astronomy Picture of the Day from NASA"""
    if not isinstance(images_count, int) or images_count < 1:
        images_count = None
    nasa_apod_url = f'https://api.nasa.gov/planetary/apod'

    payload = {
        "api_key": token,
        "count": images_count
    }

    response = requests.get(nasa_apod_url, params=payload)
    response.raise_for_status()

    nasa_apods = response.json()
    if not images_count:
        download_one_apod_img(nasa_apods, path)
    else:
        for nasa_apod in nasa_apods:
            download_one_apod_img(nasa_apod, path)


def get_nasa_epic(token: str, path: str, images_count: int) -> None:
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
                            f'/{image_date.strftime("%d")}/png/{image}.png'

        response_img = requests.get(nasa_epic_img_url, params=payload)
        response_img.raise_for_status()

        download_img(response_img.url, f'{path}/epic_nasa_{image}.png')


def download_one_apod_img(nasa_apod: dict, path: str) -> None:
    """Download One Astronomy Picture of the Day from NASA"""
    nasa_apod_img_url = nasa_apod.get("hdurl", nasa_apod.get("url"))
    nasa_apod_date = nasa_apod.get("date")
    file_extension = get_file_extension(nasa_apod_img_url)
    download_img(nasa_apod_img_url, f'{path}/apod_nasa_{nasa_apod_date}{file_extension}')


def main():
    """Download images from NASA"""
    env = Env()
    env.read_env()
    Path(f"{DOWNLOAD_PATH}").mkdir(parents=True, exist_ok=True)
    nasa_api_token = env("NASA_API_TOKEN")
    get_nasa_apod(nasa_api_token, DOWNLOAD_PATH, images_count=COUNT_OF_DOWNLOADED_IMAGES_APOD)
    get_nasa_epic(nasa_api_token, DOWNLOAD_PATH, images_count=COUNT_OF_DOWNLOADED_IMAGES_EPIC)


if __name__ == "__main__":
    main()
