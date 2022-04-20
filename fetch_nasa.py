import datetime

import requests
from environs import Env

from libs.download_utils import get_file_extension, download_img


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
    if images_count:
        nasa_apods_json = [nasa_apods_json]
    for nasa_apod in nasa_apods_json:
        nasa_apod_img_url = nasa_apod.get("hdurl", nasa_apod.get("url"))
        nasa_apod_date = nasa_apod.get("date")
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
    """Download images from NASA"""
    env = Env()
    env.read_env()
    nasa_api_token = env("NASA_API_TOKEN")
    get_nasa_apod(nasa_api_token)
    get_nasa_epic(nasa_api_token, 1)


if __name__ == "__main__":
    main()
