import datetime
import os
from pathlib import Path

import requests
from environs import Env


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
        download_img(nasa_apod_img_url, f'nasa/apod/nasa_apod_{nasa_apod_date}{file_extension}')


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

        download_img(response_img.url, f'nasa/epic/{image}.png')


def main():
    env = Env()
    env.read_env()
    nasa_api_token = env("NASA_API_TOKEN")
    fetch_spacex_last_launch()
    get_nasa_apod(nasa_api_token)
    get_nasa_epic(nasa_api_token, 1)


if __name__ == "__main__":
    main()
