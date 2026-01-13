# Диаграммы архитектуры системы

## 1. Общая архитектура системы

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  (HTML Templates + Bootstrap 4 + jQuery + AJAX)        │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Requests/Responses
┌────────────────────▼────────────────────────────────────┐
│                     View Layer                           │
│  (Django Views: Class-based & Function-based)           │
│  - Authentication Views                                  │
│  - Order Management Views                                │
│  - Portfolio Views                                       │
│  - Review Views                                          │
│  - Notification Views                                    │
└────────────────────┬────────────────────────────────────┘
                     │ Business Logic Calls
┌────────────────────▼────────────────────────────────────┐
│                   Business Logic Layer                   │
│  (Models, Forms, Validators, Services, Signals)         │
│  - User Management                                       │
│  - Order Processing                                      │
│  - Rating Calculations                                   │
│  - Notification Generation                               │
└────────────────────┬────────────────────────────────────┘
                     │ ORM Queries
┌────────────────────▼────────────────────────────────────┐
│                    Data Layer                            │
│  (SQLite Database + Django ORM)                         │
│  - User Tables                                           │
│  - Order Tables                                          │
│  - Portfolio Tables                                      │
│  - Review Tables                                         │
└─────────────────────────────────────────────────────────┘
```

## 2. Модульная архитектура Django

```
masters_platform/
├── accounts/           ┌─────────────────────┐
│   ├── models.py      │   User Management   │
│   ├── views.py       │   - CustomUser      │
│   ├── forms.py       │   - Profile         │
│   └── urls.py        │   - ExecutorProfile │
│                       └─────────────────────┘
├── orders/             ┌─────────────────────┐
│   ├── models.py      │  Order Management   │
│   ├── views.py       │   - Order           │
│   ├── forms.py       │   - Response        │
│   └── urls.py        │   - Category        │
│                       └─────────────────────┘
├── portfolio/          ┌─────────────────────┐
│   ├── models.py      │    Portfolio        │
│   ├── views.py       │   - PortfolioItem   │
│   ├── forms.py       │   - PortfolioImage  │
│   └── urls.py        └─────────────────────┘
│
├── reviews/            ┌─────────────────────┐
│   ├── models.py      │      Reviews        │
│   ├── views.py       │   - Review          │
│   ├── forms.py       │   - Rating Calc     │
│   └── urls.py        └─────────────────────┘
│
├── notifications/      ┌─────────────────────┐
│   ├── models.py      │   Notifications     │
│   ├── views.py       │   - Notification    │
│   └── urls.py        │   - Alert System    │
│                       └─────────────────────┘
└── core/               ┌─────────────────────┐
    ├── utils.py        │   Shared Utils      │
    └── mixins.py       │   - Permissions     │
                        │   - Utilities       │
                        └─────────────────────┘
```

## 3. Схема базы данных

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CustomUser    │    │    Profile      │    │ ExecutorProfile │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │◄──►│ id (PK)         │    │ id (PK)         │
│ username        │    │ user_id (FK)    │    │ user_id (FK)    │◄──┐
│ email           │    │ phone           │    │ experience_years│   │
│ user_type       │    │ avatar          │    │ hourly_rate     │   │
│ is_verified     │    │ bio             │    │ average_rating  │   │
│ created_at      │    │ city            │    │ total_reviews   │   │
└─────────────────┘    └─────────────────┘    └─────────────────┘   │
         │                                                           │
         │              ┌─────────────────┐    ┌─────────────────┐   │
         │              │    Category     │    │     Order       │   │
         │              ├─────────────────┤    ├─────────────────┤   │
         │              │ id (PK)         │◄──►│ id (PK)         │   │
         │              │ name            │    │ customer_id (FK)│◄──┘
         │              │ slug            │    │ category_id (FK)│
         │              │ description     │    │ title           │
         │              └─────────────────┘    │ description     │
         │                                     │ budget_min      │
         │                                     │ budget_max      │
         │                                     │ status          │
         │                                     │ created_at      │
         │                                     └─────────────────┘
         │                                              │
         │              ┌─────────────────┐             │
         │              │    Response     │             │
         │              ├─────────────────┤             │
         │              │ id (PK)         │             │
         └─────────────►│ executor_id (FK)│             │
                        │ order_id (FK)   │◄────────────┘
                        │ message         │
                        │ proposed_price  │
                        │ status          │
                        │ created_at      │
                        └─────────────────┘
                                 │
         ┌─────────────────┐     │     ┌─────────────────┐
         │     Review      │     │     │ PortfolioItem   │
         ├─────────────────┤     │     ├─────────────────┤
         │ id (PK)         │     │     │ id (PK)         │
         │ order_id (FK)   │◄────┘  ┌─►│ executor_id (FK)│
         │ customer_id (FK)│        │  │ title           │
         │ executor_id (FK)│────────┘  │ description     │
         │ rating          │           │ category_id (FK)│
         │ comment         │           │ created_at      │
         │ executor_response│          └─────────────────┘
         │ created_at      │                   │
         └─────────────────┘                   │
                                    ┌─────────────────┐
         ┌─────────────────┐        │ PortfolioImage  │
         │  Notification   │        ├─────────────────┤
         ├─────────────────┤        │ id (PK)         │
         │ id (PK)         │        │ portfolio_item  │◄┘
         │ user_id (FK)    │        │ image           │
         │ type            │        │ caption         │
         │ title           │        └─────────────────┘
         │ message         │
         │ related_obj_id  │
         │ is_read         │
         │ created_at      │
         └─────────────────┘
```

## 4. Поток данных пользователя

### Регистрация и аутентификация
```
User Input → Registration Form → CustomUser Model → Profile Creation → Login
     ↓              ↓                    ↓               ↓            ↓
  Validation → Form Processing → Database Save → Signal Handler → Session
```

### Создание заказа
```
Customer → Order Form → Order Model → Database → Notification → Executors
    ↓          ↓           ↓           ↓            ↓           ↓
 Fill Form → Validate → Save Order → Store → Alert System → View Orders
```

### Система откликов
```
Executor → Response Form → Response Model → Notification → Customer
    ↓           ↓              ↓              ↓           ↓
View Order → Submit → Save Response → Alert Customer → Review Response
```

### Система отзывов
```
Customer → Review Form → Review Model → Rating Calc → Executor Profile
    ↓          ↓            ↓             ↓              ↓
Rate Work → Submit → Save Review → Update Rating → Display Rating
```

## 5. Архитектура безопасности

```
┌─────────────────────────────────────────────────────────┐
│                 Security Layers                          │
├─────────────────────────────────────────────────────────┤
│ 1. Input Validation                                     │
│    - Form Validation                                    │
│    - File Type/Size Checks                             │
│    - SQL Injection Prevention (ORM)                    │
├─────────────────────────────────────────────────────────┤
│ 2. Authentication & Authorization                       │
│    - User Authentication                                │
│    - Role-based Access Control                         │
│    - Object-level Permissions                          │
├─────────────────────────────────────────────────────────┤
│ 3. Session Security                                     │
│    - CSRF Protection                                    │
│    - Session Timeout (60 min)                          │
│    - Secure Cookies                                     │
├─────────────────────────────────────────────────────────┤
│ 4. Data Protection                                      │
│    - Password Hashing (PBKDF2)                         │
│    - XSS Prevention (Auto-escaping)                    │
│    - Sensitive Data Encryption                         │
└─────────────────────────────────────────────────────────┘
```

## 6. Архитектура развертывания

### Development Environment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Developer     │    │  Django Dev     │    │    SQLite       │
│   Machine       │───►│    Server       │───►│   Database      │
│                 │    │  (Port 8000)    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Production Environment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │    Gunicorn     │    │   PostgreSQL    │
│  Reverse Proxy  │───►│   WSGI Server   │───►│    Database     │
│   (Port 80/443) │    │   (Port 8000)   │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │  Static Files   │              │
         └─────────────►│    (Nginx)      │              │
                        └─────────────────┘              │
                                 │                       │
                        ┌─────────────────┐              │
                        │  Media Files    │              │
                        │   (Uploads)     │◄─────────────┘
                        └─────────────────┘
```

## 7. API Architecture (Future)

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer                             │
├─────────────────────────────────────────────────────────┤
│ REST API Endpoints                                      │
│ ├── /api/v1/auth/          (Authentication)            │
│ ├── /api/v1/orders/        (Order Management)          │
│ ├── /api/v1/portfolio/     (Portfolio CRUD)            │
│ ├── /api/v1/reviews/       (Review System)             │
│ └── /api/v1/notifications/ (Notification System)       │
├─────────────────────────────────────────────────────────┤
│ API Documentation                                       │
│ ├── OpenAPI/Swagger Spec                               │
│ ├── Interactive Documentation                           │
│ └── API Testing Interface                               │
└─────────────────────────────────────────────────────────┘
```

## 8. Мониторинг и логирование

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Application   │    │    Logging      │    │   Monitoring    │
│     Logs        │───►│     System      │───►│    Dashboard    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │  Error Tracking │              │
         └─────────────►│   (Sentry)      │              │
                        └─────────────────┘              │
                                 │                       │
                        ┌─────────────────┐              │
                        │  Performance    │              │
                        │   Monitoring    │◄─────────────┘
                        └─────────────────┘
```

Эти диаграммы показывают различные аспекты архитектуры системы и могут быть использованы для понимания структуры и взаимодействий компонентов платформы.