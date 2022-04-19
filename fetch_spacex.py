import requests

from module.module import get_file_extension, download_img


def fetch_spacex_last_launch() -> None:
    """Download photos from last launch of SpaceX"""
    spacex_url = "https://api.spacexdata.com/v4/launches/latest"

    response = requests.get(spacex_url)
    response.raise_for_status()

    spacex_photos = response.json()['links']['flickr']['original']

    for number, img_url in enumerate(spacex_photos):
        file_extension = get_file_extension(img_url)
        download_img(img_url, f'spacex/spacex{number + 1}{file_extension}')


def main():
    """Download images from SpaceX"""
    fetch_spacex_last_launch()


if __name__ == "__main__":
    main()
