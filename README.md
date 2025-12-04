# 🧠 Habit Tracker API (Django + DRF + Celery)

> Курсовой проект по книге Джеймса Клира «Атомные привычки».  
> Бэкенд для SPA‑приложения по отслеживанию полезных привычек и напоминаниям в Telegram.

---

## 🇷🇺 Описание проекта

Этот сервис позволяет пользователям:

- создавать и редактировать **полезные и приятные привычки**;
- настраивать **периодичность** и время выполнения;
- получать **напоминания в Telegram** через Celery;
- делиться привычками с другими через **публичный список**;
- работать с API через Swagger / ReDoc документацию.

Проект реализован на **Django REST Framework** с использованием **JWT‑аутентификации**, **Celery + Redis** для фоновых задач и **Telegram Bot API** для рассылки уведомлений.

---

## ✨ Основной функционал

- 👤 **Пользователь и авторизация**
  - Кастомная модель пользователя (email как логин).
  - Регистрация: `POST /api/register/`
  - JWT‑аутентификация: `POST /api/token/`, `POST /api/token/refresh/`.

- 📋 **Привычки**
  - CRUD для привычек через `HabitViewSet`:
    - `GET /api/habit/` — список привычек текущего пользователя (с пагинацией по 5 штук).
    - `POST /api/habit/` — создание привычки.
    - `GET /api/habit/{id}/` — просмотр привычки.
    - `PUT/PATCH /api/habit/{id}/` — обновление.
    - `DELETE /api/habit/{id}/` — удаление.
  - Публичные привычки:
    - `GET /api/habit/public/` — просмотр привычек с флагом `is_published=True` (только чтение).

- ✅ **Бизнес‑правила и валидаторы**
  - Нельзя одновременно указать **вознаграждение** и **связанную приятную привычку**.
  - Время выполнения **не более 120 секунд**.
  - В связанные привычки можно выбирать **только приятные привычки**.
  - У приятной привычки не может быть ни вознаграждения, ни связанной привычки.
  - Периодичность — **не реже 1 раза в 7 дней**.

- 🔔 **Напоминания в Telegram**
  - Привязка Telegram‑аккаунта: `POST /api/tg/link/` (передаём `chat_id`).
  - Периодическая задача Celery проходит по привычкам и отправляет сообщения пользователям в нужное время.
  - Чтобы не спамить, используется кэширование — повторные напоминания за один и тот же период не отправляются.

- 🌍 **Инфраструктура**
  - CORS‑настройки для работы с фронтендом.
  - JWT‑защита всех приватных эндпоинтов.
  - Автогенерируемая документация:
    - Swagger: `GET /api/swagger/`
    - ReDoc: `GET /api/redoc/`

---

## 🧱 Технологический стек

- Python 3.13
- Django 5
- Django REST Framework
- PostgreSQL
- Redis
- Celery + django‑celery‑beat
- Simple JWT
- drf‑yasg (Swagger / ReDoc)
- django‑cors‑headers
- pytest, pytest‑django, pytest‑asyncio
- flake8, black, isort

---

## 🗂 Структура проекта

```text
FinalCoursework/
├─ config/           # Настройки Django, Celery, URLs
├─ habits/           # Модели привычек, сериализаторы, вьюхи, права, пагинация
├─ users/            # Кастомный пользователь, регистрация, JWT‑логика
├─ tg/               # Сервисы и задачи для Telegram‑уведомлений
├─ tests/            # Тесты для привычек и пользователей
├─ pyproject.toml    # Зависимости проекта (Poetry)
└─ .env.sample       # Пример настроек окружения
```

---

## ⚙️ Настройка и запуск

### 1. Клонирование репозитория

```bash
git clone <YOUR_REPO_URL>.git
cd FinalCoursework
```

### 2. Установка зависимостей

Проект использует **Poetry**:

```bash
poetry install
```

### 3. Настройка окружения

Создайте файл `.env` рядом с `manage.py` на основе `.env.sample`:

```env
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_NAME=habits_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/0

TELEGRAM_BOT_TOKEN=123456789:xxxxxxxxxxxxxxxxxxxxxxxxxxxx
CORS_ALLOW_ALL=True
```

### 4. Миграции и суперпользователь

```bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

### 5. Запуск приложения

```bash
# Django
poetry run python manage.py runserver

# Celery worker
poetry run celery -A config worker -l info

# Celery beat (периодические задачи)
poetry run celery -A config beat -l info
```

---

## 🤖 Интеграция с Telegram

1. Создайте бота через **@BotFather** и получите токен.
2. Укажите токен в переменной окружения `TELEGRAM_BOT_TOKEN`.
3. В Telegram отправьте вашему боту любое сообщение и получите `chat_id`
   (через логирование или вспомогательный метод в проекте).
4. Вызовите эндпоинт:

```http
POST /api/tg/link/
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "chat_id": "123456789"
}
```

После этого Celery‑таски начнут отправлять напоминания о привычках в личные сообщения.

---

## 🧪 Тесты и качество кода

- Тесты запускаются командой:

```bash
poetry run pytest
```

- Покрытие тестами ≥ 80% (модели, сериализаторы, вьюхи, валидаторы).
- Статический анализ и стиль:

```bash
poetry run flake8
poetry run black .
poetry run isort .
```

---

## 👨‍💻 Автор

**Ayan Kharitonov (Haohanmaiyami)**  
Учебный проект в рамках программы Skypro (Python‑разработчик).

---

# 🇬🇧 Habit Tracker API (EN)

> Final coursework project inspired by James Clear’s book *Atomic Habits*.  
> Backend for a SPA application that helps users build and keep good habits with Telegram reminders.

## 🔍 Project overview

The service allows users to:

- create and manage **useful** and **pleasant** habits;
- configure **schedule and time** for each habit;
- receive **Telegram notifications** via Celery;
- share habits via a **public habits list**;
- explore the API via **Swagger / ReDoc** documentation.

The backend is built with **Django REST Framework**, uses **JWT authentication**, **Celery + Redis** for background jobs and **Telegram Bot API** for sending reminders.

---

## ✨ Key features

- 👤 **User & auth**
  - Custom user model with email as a login field.
  - Registration: `POST /api/register/`
  - JWT auth: `POST /api/token/`, `POST /api/token/refresh/`.

- 📋 **Habits**
  - Full CRUD via `HabitViewSet`:
    - `GET /api/habit/` — list of current user’s habits (paginated, 5 per page);
    - `POST /api/habit/` — create a habit;
    - `GET /api/habit/{id}/` — retrieve a habit;
    - `PUT/PATCH /api/habit/{id}/` — update;
    - `DELETE /api/habit/{id}/` — delete.
  - Public habits:
    - `GET /api/habit/public/` — list of habits with `is_published=True` (read‑only).

- ✅ **Business rules & validation**
  - You **cannot** set both *reward* and *linked pleasant habit* at the same time.
  - Execution time must be **≤ 120 seconds**.
  - Only habits marked as pleasant can be used as *linked habits*.
  - Pleasant habits cannot have reward or linked habit fields filled.
  - Frequency must be **at least once every 7 days**.

- 🔔 **Telegram notifications**
  - Link Telegram account: `POST /api/tg/link/` (provide `chat_id`).
  - A periodic Celery task scans habits and sends reminders at the appropriate time.
  - Caching is used to avoid sending duplicate notifications.

- 🌍 **Infrastructure**
  - CORS configured for frontend integration.
  - JWT protection for all private endpoints.
  - Auto‑generated API docs:
    - Swagger: `GET /api/swagger/`
    - ReDoc: `GET /api/redoc/`

---

## 🧱 Tech stack

- Python 3.13
- Django 5
- Django REST Framework
- PostgreSQL
- Redis
- Celery + django‑celery‑beat
- Simple JWT
- drf‑yasg (Swagger / ReDoc)
- django‑cors‑headers
- pytest, pytest‑django, pytest‑asyncio
- flake8, black, isort

---

## ⚙️ Setup

```bash
git clone <YOUR_REPO_URL>.git
cd FinalCoursework
poetry install
cp .env.sample .env   # and fill in your values
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
poetry run celery -A config worker -l info
poetry run celery -A config beat -l info
```

Run tests:

```bash
poetry run pytest
```

---

## 💡 Notes

- This project is a **training backend** and can be extended with a real frontend or mobile client.
- The architecture, validation rules and async notifications are designed to demonstrate production‑like patterns in a compact educational project.
