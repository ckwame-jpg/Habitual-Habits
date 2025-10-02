# 🧱 Habit Tracker API

A backend API for tracking daily habits, built with FastAPI, locked in with JWT auth, and wrapped up in Docker so it runs anywhere.

---

## 🚀 What It Does

- Sign up and log in with secure token-based auth
- Create habits tied to your user account
- Track when you complete them
- See how long you’ve kept a streak alive
- Swagger docs included for easy testing

---

## 🧰 Tech Stack

- **FastAPI** – lightweight and fast
- **SQLite** – keeping it simple for now
- **SQLAlchemy** – ORM life
- **JWT** – user auth with `python-jose`
- **Docker** – containerized to flex it clean

---

## 🗂 Folder Breakdown

```
habit-tracker-api/
├── app/
│   ├── routes/
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── ...
├── Dockerfile
├── requirements.txt
├── README.md
└── .env.example
```

---

## 🛠 Getting Started

### ▶️ Run it locally

```bash
git clone https://github.com/your-username/habit-tracker-api.git
cd habit-tracker-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 🐳 Run it with Docker

```bash
docker build -t habit-tracker .
docker run -d -p 8000:8000 habit-tracker
```

App should now be live at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Auth Flow

1. `POST /register` – create an account  
2. `POST /login` – get your token  
3. Use `Bearer <token>` in Swagger's Authorize button to hit protected routes

---

## 📌 Endpoints You Can Try

- `GET /habits/` – your habits
- `POST /habits/` – make a new habit
- `POST /habits/{id}/complete` – mark as done
- `GET /habits/{id}/streak` – check your streak

---

## 🧪 Testing (if you're about that)

```bash
pytest
```

---

## Built By

Christopher Prempeh
