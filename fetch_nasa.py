import datetime
from pathlib import Path

import requests
from environs import Env

from libs.download_utils import download_img, download_one_apod_img


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
                            f'/{image_date.day}/png/{image}.png'

        response_img = requests.get(nasa_epic_img_url, params=payload)
        response_img.raise_for_status()

        download_img(response_img.url, f'{path}/epic_nasa_{image}.png')


def main():
    """Download images from NASA"""
    env = Env()
    env.read_env()
    download_path = "./images/nasa"
    Path(f"{download_path}").mkdir(parents=True, exist_ok=True)
    nasa_api_token = env("NASA_API_TOKEN")
    get_nasa_apod(nasa_api_token, download_path, 5)
    get_nasa_epic(nasa_api_token, download_path, 1)


if __name__ == "__main__":
    main()
