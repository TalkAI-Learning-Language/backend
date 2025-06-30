# Talki Ai Backend

> **AI-powered Language Learning App — Backend Server**
>
> 🚀 Built with FastAPI (Python)

---

## Overview

**Talki Ai** is a mobile-first language learning platform with friendly AI teacher avatars, personalized lessons, free trial onboarding, and voice chat.  
This repository is the backend server powering the mobile app.

**Features:**
- User onboarding flows (video intro, personalization)
- Multilingual support
- Teacher avatar selection
- Free trial & plan management
- Lesson content APIs (vocabulary, grammar, listening, conversation)
- Voice/chat endpoints for speaking practice
- User progress tracking
- Authentication (email, Google, social)
- Payment hooks for plan upgrades

---

## Tech Stack

- **Python 3.10+**
- **FastAPI** (REST API framework)
- **Uvicorn** (ASGI server)
- **SQLAlchemy** (database ORM)
- **Alembic** (migrations)
- **PostgreSQL** (recommended)
- **OAuth2** (Google/social login)
- **Pydantic** (data validation)
- **Docker** (deployment)
- **Pytest** (testing)

---

## Getting Started

### 1. Clone the Repo

```sh
git clone https://github.com/your-org/talki-ai-backend.git
cd talki-ai-backend
```

### 2. Setup Environment

- Recommended: use [virtualenv](https://virtualenv.pypa.io/) or [Poetry](https://python-poetry.org/).

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Copy `.env.example` to `.env` and fill in secrets (DB, JWT, OAuth keys).

### 3. Run Database

- Recommended: PostgreSQL (local or Docker/Postgres)

```sh
docker-compose up db
```

### 4. Run FastAPI Server

```sh
uvicorn app.main:app --reload
```

- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Structure

### Auth & User

- `POST /auth/signup` — Email signup
- `POST /auth/login` — Email login
- `POST /auth/google` — Google OAuth
- `POST /auth/social` — Social login

### Onboarding

- `POST /onboarding/name` — Save user name
- `POST /onboarding/language` — Set native language
- `POST /onboarding/goal` — Set learning goal
- `POST /onboarding/schedule` — Set study schedule

### Teacher & Trial

- `GET /teachers` — List available teachers
- `POST /trial/start` — Start free trial
- `POST /trial/lesson` — Start lesson in trial
- `POST /trial/complete` — Complete trial

### Lessons

- `GET /lessons/vocabulary`
- `GET /lessons/grammar`
- `GET /lessons/listening`
- `POST /lessons/conversation`

### Voice & Feedback

- `POST /voice/recognize` — Voice to text
- `POST /voice/feedback` — Pronunciation feedback

### Progress & Profile

- `GET /user/progress`
- `PUT /user/profile`
- `POST /feedback` — User suggestions

### Payments

- `POST /payment/upgrade`
- `GET /payment/plans`

---

## Folder Structure

```
app/
 ├── main.py        # FastAPI app
 ├── models/        # SQLAlchemy models
 ├── schemas/       # Pydantic schemas
 ├── routers/       # API endpoints
 ├── services/      # Business logic
 ├── db/            # DB session, migrations
 └── utils/         # Helpers, JWT, etc.
```

---

## Development

- **Lint:** `flake8 app/`
- **Test:** `pytest`
- **Run:** `uvicorn app.main:app --reload`
- **Format:** `black app/`

---

## Deployment

- Docker-ready (`Dockerfile` and `docker-compose.yml` included).
- Deploy to: Heroku, Render, AWS, GCP, etc.

---

## Contributing

Pull requests are welcome!  
Please open issues for bugs or feature requests.

---

## License

MIT

---

## Contact

- [denysbakin@gmail.com](mailto:yourname@yourdomain.com)
- [@denysbakin](https://github.com/denysbakin)

---

**Talki Ai** — *Learn fast, speak with confidence!* 🚀