# Implementation Plan

- [ ] 1. Инициализация проекта и базовая настройка
  - Создать Django проект с именем `masters_platform`
  - Настроить виртуальное окружение и установить зависимости (Django 3.1.4, Hypothesis, pytest-django, factory_boy, Faker, Pillow)
  - Настроить структуру приложений: accounts, orders, portfolio, reviews, notifications, core
  - Настроить settings.py (SECRET_KEY, DATABASES, INSTALLED_APPS, MIDDLEWARE)
  - Создать базовые шаблоны и статические файлы (Bootstrap 4, jQuery)
  - Настроить pytest и pytest-django для тестирования
  - _Requirements: 3.1.3.4, 3.1.3.5_

- [ ] 2. Реализация модуля Accounts (Пользователи и аутентификация)
- [ ] 2.1 Создать модели пользователей
  - Реализовать CustomUser модель с полями: email, user_type, is_verified, created_at
  - Реализовать Profile модель с полями: phone, avatar, bio, city
  - Реализовать ExecutorProfile модель с полями: specialization, experience_years, hourly_rate, average_rating, total_reviews
  - Создать и применить миграции
  - _Requirements: 1.1, 1.2, 2.1, 2.2_

- [ ]* 2.2 Написать property-based тест для регистрации пользователя
  - **Property 1: User registration creates account**
  - **Validates: Requirements 1.1**

- [ ]* 2.3 Написать property-based тест для аутентификации
  - **Property 2: Authentication with valid credentials succeeds**
  - **Validates: Requirements 1.2**

- [ ]* 2.4 Написать property-based тест для назначения роли
  - **Property 3: User role assignment matches selection**
  - **Validates: Requirements 1.3**

- [ ] 2.5 Создать формы регистрации и входа
  - Реализовать RegistrationForm с валидацией email, пароля, user_type
  - Реализовать LoginForm
  - Реализовать PasswordResetForm
  - Добавить валидацию на стороне сервера
  - _Requirements: 1.1, 1.4_

- [ ] 2.6 Создать представления для аутентификации
  - Реализовать RegisterView (создание пользователя, отправка email)
  - Реализовать LoginView (аутентификация)
  - Реализовать LogoutView
  - Реализовать PasswordResetView
  - Настроить URL маршруты
  - _Requirements: 1.1, 1.2, 1.4, 1.5_

- [ ] 2.7 Создать представления для управления профилем
  - Реализовать ProfileView (просмотр и редактирование)
  - Реализовать ProfileUpdateView
  - Реализовать ExecutorProfileView
  - Добавить загрузку аватара с валидацией
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ]* 2.8 Написать property-based тест для round-trip профиля
  - **Property 4: Profile data round-trip consistency**
  - **Validates: Requirements 2.1, 2.4**

- [ ]* 2.9 Написать property-based тест для специализации
  - **Property 5: Specialization persistence**
  - **Validates: Requirements 2.2**

- [ ]* 2.10 Написать property-based тест для загрузки изображений
  - **Property 6: Image upload round-trip**
  - **Validates: Requirements 2.3**

- [ ] 2.11 Создать шаблоны для аутентификации и профиля
  - Создать register.html
  - Создать login.html
  - Создать profile.html
  - Создать profile_edit.html
  - Добавить Bootstrap стили
  - _Requirements: 1.1, 1.2, 2.1_

- [ ] 3. Реализация модуля Orders (Заказы)
- [ ] 3.1 Создать модели заказов
  - Реализовать Category модель с полями: name, slug, description
  - Реализовать Order модель с полями: customer, category, title, description, budget_min, budget_max, status, created_at, updated_at
  - Реализовать Response модель с полями: order, executor, message, proposed_price, status, created_at
  - Создать и применить миграции
  - _Requirements: 3.1, 3.2, 5.1, 10.1_

- [ ]* 3.2 Написать property-based тест для создания заказа
  - **Property 7: Order creation and publication**
  - **Validates: Requirements 3.1, 3.5**

- [ ]* 3.3 Написать property-based тест для обновления заказа
  - **Property 8: Order update persistence**
  - **Validates: Requirements 3.2**

- [ ]* 3.4 Написать property-based тест для удаления заказа
  - **Property 9: Order deletion changes status and visibility**
  - **Validates: Requirements 3.3**

- [ ]* 3.5 Написать property-based тест для списка заказов пользователя
  - **Property 10: User orders completeness**
  - **Validates: Requirements 3.4**

- [ ] 3.6 Создать формы для заказов
  - Реализовать OrderCreateForm с валидацией обязательных полей
  - Реализовать OrderUpdateForm
  - Реализовать ResponseForm
  - _Requirements: 3.1, 3.2, 5.1_

- [ ] 3.7 Создать представления для заказов
  - Реализовать OrderListView с пагинацией
  - Реализовать OrderDetailView
  - Реализовать OrderCreateView
  - Реализовать OrderUpdateView
  - Реализовать OrderDeleteView
  - Настроить URL маршруты
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 3.8 Реализовать поиск и фильтрацию заказов
  - Добавить поиск по ключевым словам (title, description)
  - Добавить фильтр по категории
  - Добавить фильтр по бюджету (min-max range)
  - Добавить сортировку по дате
  - Реализовать сброс фильтров
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ]* 3.9 Написать property-based тесты для поиска и фильтрации
  - **Property 11: Search results contain keywords**
  - **Validates: Requirements 4.1**

- [ ]* 3.10 Написать property-based тест для фильтра по категории
  - **Property 12: Category filter correctness**
  - **Validates: Requirements 4.2, 10.3**

- [ ]* 3.11 Написать property-based тест для фильтра по бюджету
  - **Property 13: Budget filter range compliance**
  - **Validates: Requirements 4.3**

- [ ]* 3.12 Написать property-based тест для сортировки по дате
  - **Property 14: Date sorting monotonicity**
  - **Validates: Requirements 4.4**

- [ ]* 3.13 Написать property-based тест для сброса фильтров
  - **Property 15: Filter reset returns full list**
  - **Validates: Requirements 4.5**

- [ ] 3.14 Создать представления для откликов
  - Реализовать ResponseCreateView
  - Реализовать ResponseListView (для заказчика)
  - Реализовать ResponseAcceptView
  - Реализовать ResponseRejectView
  - Реализовать ResponseCancelView
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ]* 3.15 Написать property-based тесты для откликов
  - **Property 16: Response creation triggers notification**
  - **Validates: Requirements 5.1, 8.1**

- [ ]* 3.16 Написать property-based тест для списка откликов
  - **Property 17: Response list completeness**
  - **Validates: Requirements 5.2**

- [ ]* 3.17 Написать property-based тест для принятия отклика
  - **Property 18: Accepting response updates order status**
  - **Validates: Requirements 5.3, 8.2**

- [ ]* 3.18 Написать property-based тест для отклонения отклика
  - **Property 19: Rejecting response updates response status**
  - **Validates: Requirements 5.4**

- [ ]* 3.19 Написать property-based тест для отмены отклика
  - **Property 20: Response cancellation removes from list**
  - **Validates: Requirements 5.5**

- [ ] 3.20 Создать шаблоны для заказов
  - Создать order_list.html с фильтрами
  - Создать order_detail.html
  - Создать order_form.html
  - Создать response_list.html
  - Добавить AJAX для динамической фильтрации
  - _Requirements: 3.1, 3.4, 4.1, 5.2_

- [ ] 4. Checkpoint - Проверка базовой функциональности
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Реализация модуля Portfolio (Портфолио)
- [ ] 5.1 Создать модели портфолио
  - Реализовать PortfolioItem модель с полями: executor, title, description, category, created_at
  - Реализовать PortfolioImage модель с полями: portfolio_item, image, caption
  - Создать и применить миграции
  - _Requirements: 6.1, 6.2, 6.3_

- [ ]* 5.2 Написать property-based тест для добавления работы в портфолио
  - **Property 21: Portfolio item persistence**
  - **Validates: Requirements 6.1**

- [ ]* 5.3 Написать property-based тест для обновления портфолио
  - **Property 22: Portfolio update round-trip**
  - **Validates: Requirements 6.2**

- [ ]* 5.4 Написать property-based тест для удаления из портфолио
  - **Property 23: Portfolio deletion removes item and images**
  - **Validates: Requirements 6.3**

- [ ]* 5.5 Написать property-based тест для отображения портфолио
  - **Property 24: Portfolio completeness in profile**
  - **Validates: Requirements 6.4**

- [ ]* 5.6 Написать property-based тест для валидации изображений
  - **Property 25: Image validation enforcement**
  - **Validates: Requirements 6.5**

- [ ] 5.7 Создать формы для портфолио
  - Реализовать PortfolioItemForm с валидацией
  - Добавить валидацию изображений (формат, размер)
  - _Requirements: 6.1, 6.5_

- [ ] 5.8 Создать представления для портфолио
  - Реализовать PortfolioListView
  - Реализовать PortfolioCreateView
  - Реализовать PortfolioUpdateView
  - Реализовать PortfolioDeleteView
  - Настроить URL маршруты
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 5.9 Создать шаблоны для портфолио
  - Создать portfolio_list.html
  - Создать portfolio_form.html
  - Добавить галерею изображений
  - _Requirements: 6.1, 6.4_

- [ ] 6. Реализация модуля Reviews (Отзывы и рейтинги)
- [ ] 6.1 Создать модели отзывов
  - Реализовать Review модель с полями: order, customer, executor, rating, comment, executor_response, created_at, updated_at
  - Добавить валидаторы для rating (1-5)
  - Создать и применить миграции
  - _Requirements: 7.1, 7.2, 7.3_

- [ ]* 6.2 Написать property-based тест для создания отзыва
  - **Property 26: Review creation updates rating**
  - **Validates: Requirements 7.1**

- [ ]* 6.3 Написать property-based тест для расчета среднего рейтинга
  - **Property 27: Average rating calculation correctness**
  - **Validates: Requirements 7.2**

- [ ]* 6.4 Написать property-based тест для отображения отзывов
  - **Property 28: Review display completeness**
  - **Validates: Requirements 7.3**

- [ ]* 6.5 Написать property-based тест для ответа на отзыв
  - **Property 29: Executor response to review persistence**
  - **Validates: Requirements 7.4**

- [ ]* 6.6 Написать property-based тест для редактирования отзыва
  - **Property 30: Review edit updates rating**
  - **Validates: Requirements 7.5**

- [ ] 6.7 Реализовать логику расчета рейтинга
  - Создать метод calculate_average_rating() в ExecutorProfile
  - Добавить сигнал для автоматического пересчета при создании/обновлении отзыва
  - _Requirements: 7.1, 7.2, 7.5_

- [ ] 6.8 Создать формы для отзывов
  - Реализовать ReviewForm с валидацией rating
  - Реализовать ExecutorResponseForm
  - _Requirements: 7.1, 7.4_

- [ ] 6.9 Создать представления для отзывов
  - Реализовать ReviewCreateView
  - Реализовать ReviewListView
  - Реализовать ReviewUpdateView
  - Реализовать ExecutorResponseView
  - Настроить URL маршруты
  - _Requirements: 7.1, 7.3, 7.4, 7.5_

- [ ] 6.10 Создать шаблоны для отзывов
  - Создать review_list.html с отображением рейтинга
  - Создать review_form.html
  - Добавить звездочки для визуализации рейтинга
  - _Requirements: 7.1, 7.3_

- [ ] 7. Реализация модуля Notifications (Уведомления)
- [ ] 7.1 Создать модель уведомлений
  - Реализовать Notification модель с полями: user, notification_type, title, message, related_object_id, is_read, created_at
  - Создать и применить миграции
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ]* 7.2 Написать property-based тест для создания уведомления при отклике
  - **Property 31: Review triggers notification**
  - **Validates: Requirements 8.3**

- [ ]* 7.3 Написать property-based тест для отображения непрочитанных уведомлений
  - **Property 32: Unread notifications display**
  - **Validates: Requirements 8.4**

- [ ]* 7.4 Написать property-based тест для отметки как прочитанное
  - **Property 33: Marking notification as read updates status**
  - **Validates: Requirements 8.5**

- [ ] 7.5 Реализовать систему создания уведомлений
  - Создать функцию create_notification()
  - Добавить сигналы для автоматического создания уведомлений при откликах, принятии/отклонении, отзывах
  - _Requirements: 8.1, 8.2, 8.3_

- [ ] 7.6 Создать представления для уведомлений
  - Реализовать NotificationListView
  - Реализовать NotificationMarkReadView
  - Добавить AJAX для отметки прочитанным без перезагрузки
  - Настроить URL маршруты
  - _Requirements: 8.4, 8.5_

- [ ] 7.7 Создать шаблоны для уведомлений
  - Создать notification_list.html
  - Добавить badge с количеством непрочитанных в navbar
  - Добавить dropdown для быстрого просмотра
  - _Requirements: 8.4_

- [ ] 8. Реализация административной панели
- [ ] 8.1 Настроить Django Admin
  - Зарегистрировать все модели в admin.py
  - Настроить list_display, list_filter, search_fields для каждой модели
  - Добавить inline для связанных моделей
  - _Requirements: 9.1_

- [ ]* 8.2 Написать property-based тест для контроля доступа админа
  - **Property 34: Admin access control**
  - **Validates: Requirements 9.1**

- [ ]* 8.3 Написать property-based тест для блокировки пользователя
  - **Property 35: User blocking prevents access**
  - **Validates: Requirements 9.2**

- [ ]* 8.4 Написать property-based тест для удаления контента
  - **Property 36: Content deletion removes from database**
  - **Validates: Requirements 9.3**

- [ ]* 8.5 Написать property-based тест для точности статистики
  - **Property 37: Statistics accuracy**
  - **Validates: Requirements 9.4**

- [ ]* 8.6 Написать property-based тест для модерации отзывов
  - **Property 38: Review moderation hides content**
  - **Validates: Requirements 9.5**

- [ ] 8.7 Создать кастомные admin actions
  - Добавить action для блокировки пользователей
  - Добавить action для удаления контента
  - Добавить action для модерации отзывов
  - _Requirements: 9.2, 9.3, 9.5_

- [ ] 8.8 Создать страницу статистики
  - Реализовать AdminStatsView с подсчетом пользователей, заказов, откликов
  - Добавить графики (опционально)
  - _Requirements: 9.4_

- [ ] 9. Реализация категорий услуг
- [ ] 9.1 Создать фикстуры для категорий
  - Создать fixtures/categories.json с предопределенными категориями: ремонт, обучение, красота, здоровье, IT-услуги, доставка
  - Добавить команду для загрузки фикстур
  - _Requirements: 10.1, 10.5_

- [ ]* 9.2 Написать property-based тест для сохранения специализаций
  - **Property 39: Specialization selection persistence**
  - **Validates: Requirements 10.2**

- [ ]* 9.3 Написать property-based тест для доступности новой категории
  - **Property 40: New category availability**
  - **Validates: Requirements 10.4**

- [ ] 9.4 Создать представления для управления категориями
  - Реализовать CategoryListView
  - Реализовать CategoryCreateView (только для админов)
  - _Requirements: 10.1, 10.4_

- [ ] 10. Реализация безопасности
- [ ] 10.1 Настроить безопасность Django
  - Настроить SECRET_KEY в переменных окружения
  - Включить CSRF protection
  - Включить XSS protection (auto-escaping)
  - Настроить ALLOWED_HOSTS
  - Настроить SESSION_COOKIE_AGE (60 минут)
  - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [ ]* 10.2 Написать property-based тест для хеширования паролей
  - **Property 41: Password hashing enforcement**
  - **Validates: Requirements 11.1**

- [ ]* 10.3 Написать property-based тест для санитизации ввода
  - **Property 42: Input sanitization prevents injection**
  - **Validates: Requirements 11.3**

- [ ]* 10.4 Написать property-based тест для CSRF защиты
  - **Property 43: CSRF protection enforcement**
  - **Validates: Requirements 11.4**

- [ ]* 10.5 Написать property-based тест для контроля доступа
  - **Property 44: Access control enforcement**
  - **Validates: Requirements 11.5**

- [ ] 10.6 Реализовать валидацию и санитизацию ввода
  - Добавить валидаторы для всех форм
  - Добавить санитизацию HTML в текстовых полях
  - Добавить проверку на SQL injection в поисковых запросах
  - _Requirements: 11.3_

- [ ] 10.7 Настроить права доступа
  - Создать permission mixins для проверки владельца объекта
  - Добавить декораторы @login_required где необходимо
  - Реализовать проверку прав в представлениях
  - _Requirements: 11.5_

- [ ] 11. Оптимизация производительности
- [ ] 11.1 Оптимизировать запросы к БД
  - Добавить select_related() для ForeignKey
  - Добавить prefetch_related() для ManyToMany
  - Создать индексы на часто запрашиваемых полях (email, category, status)
  - _Requirements: 12.1, 12.2, 12.5_

- [ ] 11.2 Настроить кеширование
  - Настроить кеширование шаблонов
  - Добавить кеширование для списка категорий
  - Настроить кеширование статических файлов
  - _Requirements: 12.1_

- [ ] 11.3 Оптимизировать загрузку изображений
  - Добавить сжатие изображений при загрузке
  - Реализовать создание thumbnails
  - Добавить lazy loading для изображений
  - _Requirements: 12.3_

- [ ] 12. Создание UI и шаблонов
- [ ] 12.1 Создать базовый шаблон
  - Создать base.html с Bootstrap 4
  - Добавить navbar с навигацией
  - Добавить footer
  - Подключить jQuery и AJAX
  - _Requirements: 3.1.3.4_

- [ ] 12.2 Создать главную страницу
  - Создать home.html с описанием платформы
  - Добавить поиск заказов на главной
  - Добавить категории услуг
  - _Requirements: 3.1.3.4_

- [ ] 12.3 Улучшить UX с помощью AJAX
  - Добавить AJAX для фильтрации заказов без перезагрузки
  - Добавить AJAX для отметки уведомлений
  - Добавить AJAX для лайков/избранного (опционально)
  - _Requirements: 3.1.3.4_

- [ ] 13. Финальное тестирование и документация
- [ ]* 13.1 Запустить все unit tests
  - Проверить покрытие кода (минимум 80%)
  - Исправить failing tests

- [ ]* 13.2 Запустить все property-based tests
  - Убедиться, что все 44 свойства проходят тесты
  - Проверить, что каждый тест выполняется минимум 100 итераций

- [ ] 13.3 Создать README.md
  - Описать проект и его функциональность
  - Добавить инструкции по установке
  - Добавить инструкции по запуску
  - Добавить информацию о тестировании
  - Добавить скриншоты (опционально)

- [ ] 13.4 Создать requirements.txt
  - Зафиксировать все зависимости с версиями
  - Добавить комментарии для каждой зависимости

- [ ] 13.5 Создать .gitignore
  - Добавить стандартные исключения для Python/Django
  - Исключить виртуальное окружение, __pycache__, db.sqlite3, media files

- [ ] 13.6 Создать документацию API (опционально)
  - Документировать все endpoints
  - Добавить примеры запросов и ответов

- [ ] 14. Final Checkpoint - Финальная проверка
  - Ensure all tests pass, ask the user if questions arise.
