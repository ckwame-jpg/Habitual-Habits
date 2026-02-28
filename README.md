# Habitual Habits

A habit tracking API built with FastAPI. Supports user authentication, full habit CRUD, completion logging, and streak tracking.

## Features

- JWT-based authentication (register and login)
- Create, read, update, and delete habits
- Log daily completions for each habit
- Streak tracking — see how many consecutive days you've completed a habit
- Auto-generated interactive API docs (Swagger UI)

## Tech Stack

- **FastAPI** — Python web framework
- **SQLAlchemy** — ORM for database operations
- **SQLite** — lightweight database
- **Pydantic** — request/response validation
- **python-jose** — JWT token handling
- **bcrypt** — password hashing
- **Docker** — containerized deployment
- **pytest** — test suite

## Quick Start

### Run Locally

```bash
git clone https://github.com/your-username/habit-tracker-api.git
cd habit-tracker-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`):

```env
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./habits.db
```

Start the server:

```bash
uvicorn app.main:app --reload
```

API docs available at: <http://127.0.0.1:8000/docs>

### Run with Docker Compose

```bash
docker compose up --build
```

API docs available at: <http://localhost:8000/docs>

## API Reference

### Authentication

| Method | Endpoint    | Auth | Description             |
|--------|-------------|------|-------------------------|
| POST   | `/register` | No   | Create a new account    |
| POST   | `/login`    | No   | Get a JWT access token  |

### Habits

| Method | Endpoint                   | Auth | Description                |
|--------|----------------------------|------|----------------------------|
| POST   | `/habits/`                 | Yes  | Create a new habit         |
| GET    | `/habits/`                 | Yes  | List all your habits       |
| GET    | `/habits/{id}`             | Yes  | Get a specific habit       |
| PUT    | `/habits/{id}`             | Yes  | Update a habit             |
| DELETE | `/habits/{id}`             | Yes  | Delete a habit             |
| POST   | `/habits/{id}/complete`    | Yes  | Log a completion           |
| GET    | `/habits/{id}/streak`      | Yes  | Get current streak count   |

### Example: Create and Track a Habit

```bash
# Register
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass"}'

# Login
curl -X POST http://localhost:8000/login \
  -d "username=user@example.com&password=securepass"

# Create a habit (use the token from login)
curl -X POST http://localhost:8000/habits/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Exercise", "frequency": "daily"}'

# Log a completion
curl -X POST http://localhost:8000/habits/1/complete \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"date_completed": "2025-01-15"}'

# Check your streak
curl http://localhost:8000/habits/1/streak \
  -H "Authorization: Bearer <token>"
```

## Running Tests

```bash
pip install pytest httpx
pytest -v
```

```text
tests/test_auth.py::test_register               PASSED
tests/test_auth.py::test_register_duplicate      PASSED
tests/test_auth.py::test_login_success           PASSED
tests/test_auth.py::test_login_wrong_password    PASSED
tests/test_auth.py::test_login_nonexistent_user  PASSED
tests/test_habits.py::test_create_habit          PASSED
tests/test_habits.py::test_list_habits           PASSED
tests/test_habits.py::test_get_habit             PASSED
tests/test_habits.py::test_get_habit_not_found   PASSED
tests/test_habits.py::test_update_habit          PASSED
tests/test_habits.py::test_delete_habit          PASSED
tests/test_habits.py::test_unauthenticated       PASSED
tests/test_streaks.py::test_streak_none          PASSED
tests/test_streaks.py::test_streak_one_day       PASSED
tests/test_streaks.py::test_streak_consecutive   PASSED
tests/test_streaks.py::test_streak_with_gap      PASSED
```

## Project Structure

```text
habit-tracker-api/
├── app/
│   ├── routes/
│   │   ├── habits.py        # Habit CRUD + completions + streaks
│   │   └── users.py         # User registration
│   ├── auth.py              # JWT auth, login, password hashing
│   ├── database.py          # SQLAlchemy engine and session
│   ├── models.py            # User, Habit, HabitCompletion models
│   └── schemas.py           # Pydantic request/response schemas
├── tests/
│   ├── conftest.py          # Test fixtures (client, auth, DB)
│   ├── test_auth.py         # Auth endpoint tests
│   ├── test_habits.py       # Habit CRUD tests
│   └── test_streaks.py      # Streak calculation tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Built By

Christopher Prempeh
