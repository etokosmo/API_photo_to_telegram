# Скрипт для загрузки картинок из интернета в Телеграм канал

Скрипт умеет:

* скачивать фото с последнего запуска SpaceX
* скачивать с сайта NASA [фотографию дня](https://api.nasa.gov/#apod) и [эпическую картинку](https://api.nasa.gov/#epic)
* загружать фотографии в телеграм канал.

## Цели проекта

* Автоматизировать сбор фотографий космоса.
* Сделайте скрипт для их публикации в Telegram.

> Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).

## Конфигурации

* Python version: 3.10
* Libraries: requirements.txt

## Запуск

- Скачайте код
- Установите библиотеки командой:

```bash
pip install -r requirements.txt
```

- Запишите переменные окружения в файле `.env`

```bash
NASA_API_TOKEN=... #Токен полученный на https://api.nasa.gov/
TELEGRAM_API_TOKEN=... #Токен полученный на https://telegram.me/BotFather
TELEGRAM_CHAT_ID=... #Chat id канала @someone_chat
SLEEP_TIME=... #Время в секундах через которое запустится код заново
```

- Скачать фотографии с последнего запуска SpaceX (если они есть)

```bash
python3 fetch_spacex.py
```

- Скачать [фотографию дня](https://api.nasa.gov/#apod) и [эпическую картинку](https://api.nasa.gov/#epic) NASA

```bash
python3 fetch_nasa.py
```

- Отправить все фото из папки `images` через телеграм бота

```bash
python3 main.py
```