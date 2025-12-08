# Быстрый старт

## За 5 минут до запуска

### 1. Установка (Windows)

```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/masters-platform.git
cd masters-platform

# Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Создать БД и загрузить данные
python manage.py migrate
python manage.py loaddata fixtures/categories.json

# Создать админа
python manage.py createsuperuser

# Запустить сервер
python manage.py runserver
```

### 2. Открыть в браузере

- **Главная**: http://127.0.0.1:8000/
- **Админка**: http://127.0.0.1:8000/admin/

## Что дальше?

### Для изучения проекта:
1. Прочитайте `README.md` - общее описание
2. Изучите `.kiro/specs/masters-platform/requirements.md` - требования
3. Посмотрите `.kiro/specs/masters-platform/design.md` - архитектура

### Для разработки:
1. Прочитайте `SPEC_GUIDE.md` - работа со спецификацией
2. Следуйте `.kiro/specs/masters-platform/tasks.md` - план реализации
3. Изучите `CONTRIBUTING.md` - стандарты кодирования

### Для тестирования:
```bash
pytest                    # Все тесты
pytest -m property        # Property-based тесты
pytest --cov=.           # С покрытием
```

## Основные URL

| URL | Описание |
|-----|----------|
| `/` | Главная страница |
| `/accounts/register/` | Регистрация |
| `/accounts/login/` | Вход |
| `/accounts/profile/` | Профиль |
| `/orders/` | Список заказов |
| `/orders/create/` | Создать заказ |
| `/portfolio/<user_id>/` | Портфолио исполнителя |
| `/reviews/<executor_id>/` | Отзывы исполнителя |
| `/notifications/` | Уведомления |
| `/admin/` | Админ-панель |

## Тестовые данные

### Создать заказчика:
- Username: customer1
- Email: customer@example.com
- Password: testpass123
- Type: Заказчик

### Создать исполнителя:
- Username: executor1
- Email: executor@example.com
- Password: testpass123
- Type: Исполнитель

## Структура проекта

```
masters-platform/
├── .kiro/specs/          # Спецификации (требования, дизайн, задачи)
├── accounts/             # Пользователи
├── orders/               # Заказы
├── portfolio/            # Портфолио
├── reviews/              # Отзывы
├── notifications/        # Уведомления
├── templates/            # HTML шаблоны
├── static/               # CSS, JS, изображения
└── masters_platform/     # Настройки Django
```

## Полезные команды

```bash
# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Запустить тесты
pytest

# Собрать статику
python manage.py collectstatic

# Запустить shell
python manage.py shell
```

## Помощь

- **Документация**: см. `README.md`
- **Спецификация**: см. `SPEC_GUIDE.md`
- **Установка**: см. `INSTALL.md`
- **Разработка**: см. `CONTRIBUTING.md`
- **Issues**: https://github.com/yourusername/masters-platform/issues

Удачи! 🚀
