# Design Document: Платформа для поиска мастеров

## Overview

Платформа для поиска мастеров - это веб-приложение на Django, которое соединяет заказчиков с исполнителями различных услуг. Архитектура следует паттерну MVT (Model-View-Template), стандартному для Django, с четким разделением бизнес-логики, представления данных и пользовательского интерфейса.

Ключевые особенности:
- Двухролевая система (заказчики и исполнители)
- Система заказов с откликами
- Портфолио и рейтинги исполнителей
- Система уведомлений в реальном времени
- Административная панель для модерации

## Architecture

### Общая архитектура

Приложение построено на Django 3.1.4 (Python 3.8) и использует следующую архитектуру:

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  (Templates: Bootstrap 4, jQuery, AJAX)                 │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                     View Layer                           │
│  (Django Views: Class-based & Function-based)           │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                   Business Logic Layer                   │
│  (Models, Forms, Validators, Services)                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    Data Layer                            │
│  (SQLite Database, Django ORM)                          │
└─────────────────────────────────────────────────────────┘
```

### Модульная структура

Приложение разделено на следующие Django-приложения:

1. **accounts** - управление пользователями и аутентификацией
2. **orders** - управление заказами и откликами
3. **portfolio** - управление портфолио исполнителей
4. **reviews** - система рейтингов и отзывов
5. **notifications** - система уведомлений
6. **core** - общие утилиты и базовые модели

## Components and Interfaces

### 1. Accounts (Пользователи)

**Модели:**
- `CustomUser` - расширенная модель пользователя Django
- `Profile` - профиль пользователя с дополнительной информацией
- `ExecutorProfile` - профиль исполнителя со специализацией

**Основные представления:**
- `RegisterView` - регистрация нового пользователя
- `LoginView` - аутентификация пользователя
- `ProfileView` - просмотр и редактирование профиля
- `PasswordResetView` - восстановление пароля

**API endpoints:**
- `POST /accounts/register/` - регистрация
- `POST /accounts/login/` - вход
- `GET/PUT /accounts/profile/` - профиль
- `POST /accounts/password-reset/` - сброс пароля

### 2. Orders (Заказы)

**Модели:**
- `Category` - категория услуг
- `Order` - заказ от заказчика
- `Response` - отклик исполнителя на заказ
- `OrderStatus` - статусы заказа (активен, в работе, завершен, удален)

**Основные представления:**
- `OrderListView` - список заказов с фильтрацией
- `OrderDetailView` - детальная информация о заказе
- `OrderCreateView` - создание заказа
- `OrderUpdateView` - редактирование заказа
- `ResponseCreateView` - создание отклика

**API endpoints:**
- `GET /orders/` - список заказов (с фильтрами)
- `POST /orders/` - создание заказа
- `GET /orders/<id>/` - детали заказа
- `PUT /orders/<id>/` - обновление заказа
- `DELETE /orders/<id>/` - удаление заказа
- `POST /orders/<id>/responses/` - создание отклика

### 3. Portfolio (Портфолио)

**Модели:**
- `PortfolioItem` - работа в портфолио
- `PortfolioImage` - изображение работы

**Основные представления:**
- `PortfolioListView` - список работ исполнителя
- `PortfolioCreateView` - добавление работы
- `PortfolioUpdateView` - редактирование работы
- `PortfolioDeleteView` - удаление работы

**API endpoints:**
- `GET /portfolio/<user_id>/` - портфолио исполнителя
- `POST /portfolio/` - добавление работы
- `PUT /portfolio/<id>/` - обновление работы
- `DELETE /portfolio/<id>/` - удаление работы

### 4. Reviews (Отзывы)

**Модели:**
- `Review` - отзыв о работе исполнителя
- `Rating` - рейтинг (1-5 звезд)

**Основные представления:**
- `ReviewCreateView` - создание отзыва
- `ReviewListView` - список отзывов исполнителя
- `ReviewUpdateView` - редактирование отзыва

**API endpoints:**
- `GET /reviews/<executor_id>/` - отзывы исполнителя
- `POST /reviews/` - создание отзыва
- `PUT /reviews/<id>/` - обновление отзыва

### 5. Notifications (Уведомления)

**Модели:**
- `Notification` - уведомление пользователя

**Основные представления:**
- `NotificationListView` - список уведомлений
- `NotificationMarkReadView` - отметка как прочитанное

**API endpoints:**
- `GET /notifications/` - список уведомлений
- `PUT /notifications/<id>/read/` - отметить прочитанным

## Data Models

### User & Profile Models

```python
class CustomUser(AbstractUser):
    email = EmailField(unique=True)
    user_type = CharField(choices=[('customer', 'Заказчик'), ('executor', 'Исполнитель')])
    is_verified = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

class Profile:
    user = OneToOneField(CustomUser)
    phone = CharField(max_length=20)
    avatar = ImageField(upload_to='avatars/')
    bio = TextField()
    city = CharField(max_length=100)

class ExecutorProfile:
    user = OneToOneField(CustomUser)
    specialization = ManyToManyField(Category)
    experience_years = IntegerField()
    hourly_rate = DecimalField()
    average_rating = DecimalField(default=0)
    total_reviews = IntegerField(default=0)
```

### Order Models

```python
class Category:
    name = CharField(max_length=100)
    slug = SlugField(unique=True)
    description = TextField()

class Order:
    customer = ForeignKey(CustomUser)
    category = ForeignKey(Category)
    title = CharField(max_length=200)
    description = TextField()
    budget_min = DecimalField()
    budget_max = DecimalField()
    status = CharField(choices=ORDER_STATUS_CHOICES)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

class Response:
    order = ForeignKey(Order)
    executor = ForeignKey(CustomUser)
    message = TextField()
    proposed_price = DecimalField()
    status = CharField(choices=RESPONSE_STATUS_CHOICES)
    created_at = DateTimeField(auto_now_add=True)
```

### Portfolio Models

```python
class PortfolioItem:
    executor = ForeignKey(CustomUser)
    title = CharField(max_length=200)
    description = TextField()
    category = ForeignKey(Category)
    created_at = DateTimeField(auto_now_add=True)

class PortfolioImage:
    portfolio_item = ForeignKey(PortfolioItem)
    image = ImageField(upload_to='portfolio/')
    caption = CharField(max_length=200)
```

### Review Models

```python
class Review:
    order = ForeignKey(Order)
    customer = ForeignKey(CustomUser, related_name='reviews_given')
    executor = ForeignKey(CustomUser, related_name='reviews_received')
    rating = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = TextField()
    executor_response = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

### Notification Models

```python
class Notification:
    user = ForeignKey(CustomUser)
    notification_type = CharField(choices=NOTIFICATION_TYPE_CHOICES)
    title = CharField(max_length=200)
    message = TextField()
    related_object_id = IntegerField()
    is_read = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: User registration creates account
*For any* valid registration data (email, password, user_type), creating a new user account should result in a user existing in the database with a verification email sent
**Validates: Requirements 1.1**

### Property 2: Authentication with valid credentials succeeds
*For any* registered user, authenticating with correct credentials should grant access to the user's dashboard
**Validates: Requirements 1.2**

### Property 3: User role assignment matches selection
*For any* user registration, the assigned role should match the selected user_type (customer or executor)
**Validates: Requirements 1.3**

### Property 4: Profile data round-trip consistency
*For any* valid profile data, saving profile changes and then loading the profile should return the same data
**Validates: Requirements 2.1, 2.4**

### Property 5: Specialization persistence
*For any* executor and set of specializations, adding specializations and then loading the profile should show all added specializations
**Validates: Requirements 2.2**

### Property 6: Image upload round-trip
*For any* valid image file, uploading it to a profile and then retrieving the profile should provide access to the uploaded image
**Validates: Requirements 2.3**

### Property 7: Order creation and publication
*For any* valid order data with required fields, creating an order should result in the order existing in the database with status "active" and a creation timestamp
**Validates: Requirements 3.1, 3.5**

### Property 8: Order update persistence
*For any* existing order and valid update data, updating the order and then loading it should reflect all changes
**Validates: Requirements 3.2**

### Property 9: Order deletion changes status and visibility
*For any* order, deleting it should set its status to "deleted" AND remove it from the active orders list
**Validates: Requirements 3.3**

### Property 10: User orders completeness
*For any* user, viewing their orders list should display all orders belonging to that user with current statuses
**Validates: Requirements 3.4**

### Property 11: Search results contain keywords
*For any* search query with keywords, all returned orders should contain the keywords in either the title OR description
**Validates: Requirements 4.1**

### Property 12: Category filter correctness
*For any* selected category, all filtered orders should belong to that category
**Validates: Requirements 4.2, 10.3**

### Property 13: Budget filter range compliance
*For any* budget range (min, max), all filtered orders should have budget values within that range
**Validates: Requirements 4.3**

### Property 14: Date sorting monotonicity
*For any* list of orders sorted by date, each order's creation date should be less than or equal to the next order's creation date
**Validates: Requirements 4.4**

### Property 15: Filter reset returns full list
*For any* filtered order list, resetting filters should return the complete unfiltered list (idempotent operation)
**Validates: Requirements 4.5**

### Property 16: Response creation triggers notification
*For any* valid response to an order, creating the response should result in both the response existing AND a notification created for the order's customer
**Validates: Requirements 5.1, 8.1**

### Property 17: Response list completeness
*For any* order, viewing its responses should display all responses with complete executor information
**Validates: Requirements 5.2**

### Property 18: Accepting response updates order status
*For any* response, accepting it should change the order status to "in_progress" AND create a notification for the executor
**Validates: Requirements 5.3, 8.2**

### Property 19: Rejecting response updates response status
*For any* response, rejecting it should set the response status to "rejected"
**Validates: Requirements 5.4**

### Property 20: Response cancellation removes from list
*For any* response, canceling it should remove the response from the responses list
**Validates: Requirements 5.5**

### Property 21: Portfolio item persistence
*For any* valid portfolio item with image and description, adding it should result in the item appearing in the executor's portfolio
**Validates: Requirements 6.1**

### Property 22: Portfolio update round-trip
*For any* portfolio item and valid updates, updating the item and then loading it should reflect all changes
**Validates: Requirements 6.2**

### Property 23: Portfolio deletion removes item and images
*For any* portfolio item, deleting it should remove the item from the portfolio AND delete all associated images
**Validates: Requirements 6.3**

### Property 24: Portfolio completeness in profile
*For any* executor, viewing their profile should display all portfolio items belonging to that executor
**Validates: Requirements 6.4**

### Property 25: Image validation enforcement
*For any* uploaded file, valid image files (correct format and size) should be accepted, and invalid files should be rejected
**Validates: Requirements 6.5**

### Property 26: Review creation updates rating
*For any* valid review with rating, creating the review should result in the review existing AND the executor's average rating being recalculated
**Validates: Requirements 7.1**

### Property 27: Average rating calculation correctness
*For any* set of reviews for an executor, the average rating should equal the sum of all ratings divided by the count of ratings
**Validates: Requirements 7.2**

### Property 28: Review display completeness
*For any* executor profile, viewing it should display the correct average rating AND all reviews for that executor
**Validates: Requirements 7.3**

### Property 29: Executor response to review persistence
*For any* review and executor response, adding the response should result in it appearing under the review
**Validates: Requirements 7.4**

### Property 30: Review edit updates rating
*For any* review, editing its rating should update the review text AND recalculate the executor's average rating correctly
**Validates: Requirements 7.5**

### Property 31: Review triggers notification
*For any* review, creating it should generate a notification for the executor
**Validates: Requirements 8.3**

### Property 32: Unread notifications display
*For any* user, logging in should display all notifications where is_read is False
**Validates: Requirements 8.4**

### Property 33: Marking notification as read updates status
*For any* notification, marking it as read should set is_read to True
**Validates: Requirements 8.5**

### Property 34: Admin access control
*For any* user, administrators should have access to the admin panel, and non-administrators should be denied access
**Validates: Requirements 9.1**

### Property 35: User blocking prevents access
*For any* user, blocking them should prevent successful authentication attempts
**Validates: Requirements 9.2**

### Property 36: Content deletion removes from database
*For any* content item, deleting it should result in the item not existing in the database
**Validates: Requirements 9.3**

### Property 37: Statistics accuracy
*For any* point in time, displayed statistics should match the actual counts in the database (users, orders, responses)
**Validates: Requirements 9.4**

### Property 38: Review moderation hides content
*For any* review, hiding or deleting it should prevent it from being displayed to regular users
**Validates: Requirements 9.5**

### Property 39: Specialization selection persistence
*For any* executor and selected categories, saving the specializations should result in all selected categories being stored
**Validates: Requirements 10.2**

### Property 40: New category availability
*For any* new category added by admin, it should immediately become available in category selection for all users
**Validates: Requirements 10.4**

### Property 41: Password hashing enforcement
*For any* password, it should be stored in the database as a hash, never as plain text
**Validates: Requirements 11.1**

### Property 42: Input sanitization prevents injection
*For any* user input containing malicious code (XSS, SQL injection), the system should sanitize or reject the input
**Validates: Requirements 11.3**

### Property 43: CSRF protection enforcement
*For any* state-changing operation, requests without valid CSRF tokens should be rejected
**Validates: Requirements 11.4**

### Property 44: Access control enforcement
*For any* request to access another user's private data, the system should deny access if the requester lacks proper permissions
**Validates: Requirements 11.5**

## Error Handling

### Validation Errors
- All form inputs must be validated on both client and server side
- Invalid data should return clear error messages to the user
- HTTP 400 Bad Request for validation failures

### Authentication Errors
- Failed login attempts should return generic error messages to prevent user enumeration
- HTTP 401 Unauthorized for authentication failures
- HTTP 403 Forbidden for authorization failures

### Not Found Errors
- HTTP 404 for non-existent resources
- Graceful handling with user-friendly error pages

### Server Errors
- HTTP 500 for unexpected server errors
- Errors should be logged with full stack traces
- Users should see generic error messages (no sensitive information)

### Database Errors
- Transaction rollback on failures
- Retry logic for transient failures
- Connection pooling to handle connection errors

### File Upload Errors
- File size validation (max 5MB for images)
- File type validation (only jpg, png, gif)
- Clear error messages for rejected uploads

## Testing Strategy

### Unit Testing

Unit tests will verify specific functionality and edge cases:

**Accounts App:**
- User registration with valid/invalid data
- Password hashing verification
- Email validation
- User type assignment

**Orders App:**
- Order creation with required fields
- Order status transitions
- Filter logic for search
- Budget range validation

**Portfolio App:**
- Portfolio item creation
- Image upload validation
- Item deletion cascades

**Reviews App:**
- Rating calculation logic
- Review creation and updates
- Average rating computation

**Notifications App:**
- Notification creation triggers
- Read/unread status management

### Property-Based Testing

Property-based tests will verify universal properties across all inputs using **Hypothesis** (Python PBT library):

**Configuration:**
- Each property test should run a minimum of 100 iterations
- Each test must be tagged with a comment referencing the design document property
- Tag format: `# Feature: masters-platform, Property {number}: {property_text}`

**Key Properties to Test:**
- Round-trip properties for data persistence (profiles, orders, portfolio)
- Invariants (rating calculations, status consistency)
- Idempotence (filter resets, logout)
- Access control properties
- Input validation properties

**Example Property Test Structure:**
```python
from hypothesis import given, strategies as st
import hypothesis

@given(st.emails(), st.text(min_size=8), st.sampled_from(['customer', 'executor']))
def test_user_registration_property(email, password, user_type):
    # Feature: masters-platform, Property 1: User registration creates account
    user = create_user(email, password, user_type)
    assert User.objects.filter(email=email).exists()
    assert user.user_type == user_type
    assert verify_email_sent(email)
```

### Integration Testing

Integration tests will verify component interactions:
- User registration flow (form → view → model → email)
- Order creation and response workflow
- Review submission and rating update
- Notification generation on events

### Test Coverage Goals
- Minimum 80% code coverage
- 100% coverage for critical paths (authentication, payments, data validation)
- All correctness properties must have corresponding property tests

## Technology Stack

### Backend
- **Django 3.1.4** - Web framework
- **Python 3.8** - Programming language
- **SQLite** - Database (development), PostgreSQL (production)
- **Django ORM** - Database abstraction
- **Django REST Framework** - API endpoints (if needed)

### Frontend
- **Bootstrap 4** - CSS framework
- **jQuery 3.x** - JavaScript library
- **AJAX** - Asynchronous requests
- **HTML5/CSS3** - Markup and styling

### Testing
- **pytest** - Test runner
- **pytest-django** - Django integration for pytest
- **Hypothesis** - Property-based testing library
- **factory_boy** - Test data generation
- **Faker** - Fake data generation

### Development Tools
- **PyCharm** - IDE
- **Git** - Version control
- **pip** - Package management
- **virtualenv** - Environment isolation

### Deployment
- **Apache 2.2+** or **Nginx 1.19.0** - Web server
- **Gunicorn** - WSGI server
- **PostgreSQL 9.4+** - Production database

## Security Considerations

### Django Built-in Security Features
- CSRF protection enabled by default
- XSS protection through template auto-escaping
- SQL injection protection through ORM
- Clickjacking protection via X-Frame-Options
- SSL/HTTPS enforcement in production

### Additional Security Measures
- Password hashing using PBKDF2 algorithm
- SECRET_KEY kept in environment variables
- User input validation and sanitization
- File upload restrictions (type, size)
- Rate limiting on authentication endpoints
- Session timeout after 60 minutes of inactivity

### Access Control
- Role-based permissions (customer, executor, admin)
- Object-level permissions for user data
- Admin panel restricted to superusers only

## Performance Optimization

### Database Optimization
- Indexes on frequently queried fields (email, category, status)
- select_related() and prefetch_related() for reducing queries
- Database connection pooling
- Query optimization to avoid N+1 problems

### Caching Strategy
- Template fragment caching for static content
- Cache frequently accessed data (categories, user profiles)
- Redis for session storage (production)

### Frontend Optimization
- Static file compression (CSS, JS)
- Image optimization and lazy loading
- CDN for static assets (production)
- Minification of CSS and JavaScript

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer (Nginx)                 │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐       ┌───────▼────────┐
│  Gunicorn      │       │  Gunicorn      │
│  Worker 1      │       │  Worker 2      │
└───────┬────────┘       └───────┬────────┘
        │                         │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   PostgreSQL Database    │
        └─────────────────────────┘
```

## Future Enhancements

1. **Real-time Chat** - WebSocket-based messaging between customers and executors
2. **Payment Integration** - Stripe/PayPal for secure payments
3. **Mobile App** - React Native mobile application
4. **Advanced Search** - Elasticsearch for full-text search
5. **Geolocation** - Location-based executor search
6. **Calendar Integration** - Booking system with calendar
7. **Multi-language Support** - i18n for multiple languages
8. **Analytics Dashboard** - Business intelligence and reporting
