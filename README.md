# Notification Service

Notification Service - это сервис для управления рассылками уведомлений с использованием Django, Celery, PostgreSQL и Redis.

## Установка

### Зависимости

Убедитесь, что у вас установлены следующие инструменты:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Шаги установки

1. Склонируйте репозиторий:

```shell
git clone https://github.com/yourusername/notification-service.git
cd notification-service
```

2. Скопируйте файл .env.example в корне проекта и заполните переменные окружения.
3. Запустите приложение с помощью Docker Compose:
```shell
docker-compose up -d --build
```
Эта команда создаст и запустит контейнеры для Django, PostgreSQL, Redis, Celery Worker и Celery Beat.

4. Примените миграции:
```shell
docker-compose exec web python manage.py migrate
```
5. Создайте суперпользователя (если нужно):
```shell
docker-compose exec web python manage.py createsuperuser
```

# Использование
## Админ-панель Django
1. Перейдите по адресу http://localhost:8000/admin/.
2. Войдите с использованием учетных данных суперпользователя, которые вы создали ранее.
3. Используйте админ-панель для управления клиентами, рассылками и сообщениями.

# API
Вы можете использовать SwaggerUI, доступный по адресу http://localhost:8000/docs/, для документации API и тестирования запросов.

# Завершение работы
Чтобы остановить все контейнеры, выполните следующую команду:
```shell
docker-compose down
```