import os
import re
from pathlib import Path

import requests

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
    else:
        return None
