# Скрипт для загрузки картинок из интернета в Телеграм канал

Скрипт скачивает с сайта NASA [картинку дня](https://api.nasa.gov/#apod) и [эпическую картинку](https://api.nasa.gov/#epic). Затем загружает случайную картинку в телеграм канал.

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
- Запустите утилиту командой 
```bash
python3 main.py
```
