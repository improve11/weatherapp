# Weather App

Это простое Flask-приложение для отображения погоды в заданном городе с функцией автодополнения и запоминанием последнего введенного города.

## Установка

1. Клонируйте репозиторий:
   
bash
   git clone https://github.com/improve11/weatherapp.git
   cd weather-app
   

2. Создайте виртуальное окружение и активируйте его:
   
bash
   python3 -m venv venv
   source venv/bin/activate
   

3. Установите зависимости:
   
bash
   pip install -r requirements.txt
   

## Запуск

### Запуск без Docker

Запустите Flask-приложение:
bash
flask run

Откройте браузер и перейдите по адресу `http://127.0.0.1:5000`.

### Запуск с Docker

1. Создайте `Dockerfile`:

   
dockerfile
   FROM python:3.8-slim

   WORKDIR /app

   COPY . /app

   RUN pip install --no-cache-dir -r requirements.txt

   CMD "flask", "run", "--host=0.0.0.0"
   

2. Соберите Docker-образ:
   
bash
   docker build -t weather-app .
   

3. Запустите контейнер:
   
bash
   docker run -p 5000:5000 weather-app
   

Откройте браузер и перейдите по адресу `http://127.0.0.1:5000`.

## Функции

- Ввод названия города с автодополнением на основе API GeoNames.
- Отображение текущей погоды для введенного города.
- Предложение последнего просмотренного города при повторном посещении сайта.
