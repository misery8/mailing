# Сервис рассылки уведомлений

Сервис, который по заданным правилам запускает рассылку по списку клиентов. Отправка осуществляется
на сторонний сервис по средствам API.

Проект можно запустить как с использованием Docker, так и настроить полностью в ручную.

Взаимодействие с сервисом реализовано через API интерфейс. Описание методов API можно найти по адресу /docs/.

# Технологии
- Docker
- Redis
- Celery
- PostgreSQL
- Python 3.11
- Django 4.2
- DRF
- nginx

# Начало работы

Docker:

1. Клонируйте проект к себе на компьютер с помощью команды:
```shell
git clone https://github.com:misery8/mailing.git
```

2. Перейдите в проект и скопируйте .env.example дав название .env,
и заполните все значения в файле .env:
```shell
cp .env.example .env
```
3. Необходимо выполнить сборку проекта, а затем запустить (возможно понадобится использование sudo):
```shell
docker-compose build && docker-compose up
```
4. Создать и применить миграции для таблиц:
```shell
docker-compose run mailing python manage.py makemigratins && docker-compose run mailing python manage.py migrate
```

Ручное:
1. Выполнить вышеописанный п.1 и п.2.
2. Установить все зависимости в файле requirements.txt.
```shell
pip install -r requirements.txt
```

3. Установить и настроить PostgreSQL, Redis, nginx последнее является не обязательным для работы внутри сети.
4. Создать и применить миграции для таблиц:
```shell
python manage.py makemigrations && python manage.py migrate
```

5. Также необходимо создать пользователя БД для входа в админ-панель:
```shell
python manage.py createsuperuser
```

Запуск сервера:
```shell
python manage.py runserver 0.0.0.0:8000
```
Запуск Celery для выполнения фоновых заданий:
```shell
celery -A mailing beat -i info
```
