# Инструкция по установке и запуску

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/masters-platform.git
cd masters-platform
```

### 2. Создание виртуального окружения

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Создание базы данных

```bash
python manage.py migrate
```

### 5. Загрузка начальных данных

```bash
python manage.py loaddata fixtures/categories.json
```

### 6. Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите:
- Username: admin
- Email: admin@example.com
- Password: (ваш пароль)

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

Откройте браузер и перейдите по адресу: http://127.0.0.1:8000/

## Доступ к админ-панели

URL: http://127.0.0.1:8000/admin/
Логин: admin (или тот, что вы создали)
Пароль: (ваш пароль)

## Тестирование

### Запуск всех тестов:
```bash
pytest
```

### Запуск с покрытием:
```bash
pytest --cov=. --cov-report=html
```

### Просмотр отчета о покрытии:
Откройте файл `htmlcov/index.html` в браузере

## Структура проекта

```
masters-platform/
├── accounts/              # Пользователи и аутентификация
├── orders/                # Заказы и отклики
├── portfolio/             # Портфолио исполнителей
├── reviews/               # Отзывы и рейтинги
├── notifications/         # Уведомления
├── core/                  # Общие утилиты
├── templates/             # HTML шаблоны
├── static/                # Статические файлы
├── media/                 # Загруженные файлы
├── fixtures/              # Начальные данные
└── masters_platform/      # Настройки проекта
```

## Создание тестовых данных

### Создание заказчика:
1. Перейдите на http://127.0.0.1:8000/accounts/register/
2. Заполните форму, выберите тип "Заказчик"
3. Войдите в систему

### Создание исполнителя:
1. Перейдите на http://127.0.0.1:8000/accounts/register/
2. Заполните форму, выберите тип "Исполнитель"
3. Войдите в систему
4. Заполните профиль исполнителя

### Создание заказа:
1. Войдите как заказчик
2. Перейдите на http://127.0.0.1:8000/orders/create/
3. Заполните форму заказа

## Возможные проблемы

### Ошибка "No module named 'PIL'"
```bash
pip install Pillow
```

### Ошибка миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### Ошибка статических файлов
```bash
python manage.py collectstatic
```

## Переменные окружения (Production)

Создайте файл `.env` в корне проекта:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Развертывание на сервере

### С использованием Gunicorn:

```bash
pip install gunicorn
gunicorn masters_platform.wsgi:application --bind 0.0.0.0:8000
```

### С использованием Nginx (пример конфигурации):

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/masters-platform/staticfiles/;
    }

    location /media/ {
        alias /path/to/masters-platform/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Поддержка

Для вопросов и предложений создавайте issue в репозитории GitHub.
