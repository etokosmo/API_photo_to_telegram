from pathlib import Path

import requests

from libs.download_utils import get_file_extension, download_img

DOWNLOAD_PATH = "./images/spacex"


def fetch_spacex_last_launch(path: str) -> None:
    """Download photos from last launch of SpaceX"""
    spacex_url = "https://api.spacexdata.com/v4/launches/latest"

    response = requests.get(spacex_url)
    response.raise_for_status()

    spacex_photos = response.json()['links']['flickr']['original']

    for number, img_url in enumerate(spacex_photos, start=1):
        file_extension = get_file_extension(img_url)
        download_img(img_url, f'{path}/spacex{number}{file_extension}')


def main():
    """Download images from SpaceX"""

    Path(f"{DOWNLOAD_PATH}").mkdir(parents=True, exist_ok=True)
    fetch_spacex_last_launch(DOWNLOAD_PATH)


if __name__ == "__main__":
    main()
