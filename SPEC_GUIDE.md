# Руководство по спецификации проекта

Этот проект разработан с использованием методологии Spec-Driven Development. Все спецификации находятся в папке `.kiro/specs/masters-platform/`.

## Структура спецификации

### 1. Requirements.md
Содержит 12 основных требований с детальными критериями приемки в формате EARS (Easy Approach to Requirements Syntax):
- Регистрация и аутентификация
- Управление профилем
- Создание и управление заказами
- Поиск и фильтрация
- Система откликов
- Портфолио исполнителей
- Рейтинги и отзывы
- Уведомления
- Административная панель
- Категории услуг
- Безопасность
- Производительность

### 2. Design.md
Содержит полное проектирование системы:
- Архитектура MVT (Model-View-Template)
- Компоненты и интерфейсы
- Модели данных
- **44 Correctness Properties** для property-based testing
- Стратегия тестирования
- Обработка ошибок
- Меры безопасности
- План развертывания

### 3. Tasks.md
Содержит пошаговый план реализации:
- 14 основных задач
- 80+ подзадач
- Все property-based тесты помечены как опциональные (*)
- Каждая задача ссылается на конкретные требования

## Correctness Properties

Проект включает 44 correctness properties, которые должны быть протестированы с использованием Hypothesis (Python PBT library):

### Примеры свойств:

**Property 1: User registration creates account**
- Для любых валидных данных регистрации, создание пользователя должно привести к существованию аккаунта в БД

**Property 7: Order creation and publication**
- Для любых валидных данных заказа, создание должно установить статус "active" и дату создания

**Property 27: Average rating calculation correctness**
- Для любого набора отзывов, средний рейтинг = сумма оценок / количество оценок

## Как использовать спецификацию

### Для разработки:

1. **Изучите requirements.md** - поймите, что должна делать система
2. **Прочитайте design.md** - узнайте, как система спроектирована
3. **Следуйте tasks.md** - выполняйте задачи по порядку

### Для тестирования:

1. Каждое свойство в design.md должно иметь соответствующий property-based тест
2. Формат тега теста: `# Feature: masters-platform, Property {number}: {property_text}`
3. Каждый тест должен выполняться минимум 100 итераций

### Пример property-based теста:

```python
from hypothesis import given, strategies as st
import pytest

@given(
    st.emails(),
    st.text(min_size=8),
    st.sampled_from(['customer', 'executor'])
)
@pytest.mark.property
def test_user_registration_property(email, password, user_type):
    """
    Feature: masters-platform, Property 1: User registration creates account
    Validates: Requirements 1.1
    """
    user = create_user(email, password, user_type)
    assert User.objects.filter(email=email).exists()
    assert user.user_type == user_type
```

## Выполнение задач

### Открытие tasks.md в Kiro:

1. Откройте файл `.kiro/specs/masters-platform/tasks.md`
2. Нажмите "Start task" рядом с задачей
3. Kiro поможет выполнить задачу с учетом requirements и design

### Ручное выполнение:

1. Читайте задачу из tasks.md
2. Обращайтесь к requirements.md для понимания требований
3. Используйте design.md для понимания архитектуры
4. Реализуйте функциональность
5. Напишите тесты (если задача не помечена *)
6. Отметьте задачу как выполненную

## Тестирование свойств

### Запуск property-based тестов:

```bash
pytest -m property
```

### Запуск конкретного свойства:

```bash
pytest -k "test_user_registration_property"
```

### Проверка покрытия:

```bash
pytest --cov=. --cov-report=html
```

## Связь требований, свойств и тестов

Каждое свойство в design.md:
1. Ссылается на конкретное требование (Requirements X.Y)
2. Должно иметь соответствующую задачу в tasks.md
3. Должно быть реализовано как property-based тест

### Пример трассировки:

**Requirement 1.1**: Регистрация пользователя
↓
**Property 1**: User registration creates account
↓
**Task 2.2**: Написать property-based тест для регистрации
↓
**Test**: `test_user_registration_property()`

## Дополнительные ресурсы

- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Django Testing](https://docs.djangoproject.com/en/3.1/topics/testing/)
- [EARS Requirements](https://www.iaria.org/conferences2012/filesICCGI12/Tutorial%20EARS.pdf)

## Вопросы и поддержка

Если у вас возникли вопросы по спецификации:
1. Проверьте requirements.md для понимания требований
2. Изучите design.md для понимания архитектуры
3. Следуйте tasks.md для пошаговой реализации
4. Создайте issue в репозитории для обсуждения
