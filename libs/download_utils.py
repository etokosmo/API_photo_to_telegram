import os
import re

import requests

PATTERN_DATE_APOD = r'[\d-]+'


def download_img(img_url: str, path_to_download: str) -> None:
    """Download <img_url> in ./images/<path>"""
    response = requests.get(img_url)
    response.raise_for_status()

    with open(path_to_download, 'wb') as file:
        file.write(response.content)


def get_file_extension(url: str) -> str:
    """Return file extension from URL"""
    filename, file_extension = os.path.splitext(url)
    return file_extension


def get_caption_text(photo):
    if 'epic' in photo.name:
        return 'Earth Polychromatic Imaging Camera from NASA'
    elif 'apod' in photo.name:
        match_date = re.search(f'{PATTERN_DATE_APOD}', f'{photo.name}')
        date_apod = match_date[0] if match_date else ''
        return f'Astronomy Picture of the Day {date_apod} from NASA'
    elif 'spacex' in photo.name:
        return 'Photos from last SpaceX launch'


def download_one_apod_img(nasa_apod: dict, path: str) -> None:
    """Download One Astronomy Picture of the Day from NASA"""
    nasa_apod_img_url = nasa_apod.get("hdurl", nasa_apod.get("url"))
    nasa_apod_date = nasa_apod.get("date")
    file_extension = get_file_extension(nasa_apod_img_url)
    download_img(nasa_apod_img_url, f'{path}/apod_nasa_{nasa_apod_date}{file_extension}')
