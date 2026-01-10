# Habit Tracker API

A small Flask REST API to register/login users and manage personal habits with JWT-based authentication.

---

## Project architecture

- `app/`
  - `__init__.py` - application factory, configuration, blueprint registration
  - `db.py` - SQLAlchemy `db` instance
  - `models.py` - ORM models: `User`, `Habit`, `Checkin` (with small serializers)
  - `routes/` - blueprint routes (e.g., `auth.py`, `habits.py`)
  - `utils/` - helpers and middleware (e.g., `auth_middleware.py` for `login_required`)
- `run.py` - development runner script
- `myenv/` - local virtual environment (ignore in VCS)

Design notes:
- Routes are organized with Blueprints (`/auth` and `/habits`).
- Authentication uses JWTs: `POST /auth/login` returns a token which is passed as `Authorization: Bearer <token>` for protected routes.
- Models provide `to_dict()` methods for JSON serialization.

---

## Getting started (development)

### Prerequisites
- Python 3.11+ (use the project's virtual environment)
- Git

### Setup (PowerShell)

```powershell
# create and activate venv (if you don't already have one)
python -m venv myenv
.\myenv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt
# or
pip install Flask Flask-SQLAlchemy PyJWT "passlib[bcrypt]" python-dotenv

# copy environment example
copy .env.example .env
# edit .env to set real values for production
```

### Environment variables (`.env.example`)

```
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=replace_with_flask_secret
JWT_SECRET=replace_with_jwt_secret
DATABASE_URL=sqlite:///dev.db
```

### Run locally

```powershell
flask run
# or
python run.py
```

The factory will create tables in `dev.db` automatically in development.

---

## API reference

All endpoints return JSON. Use the `Authorization` header with `Bearer <token>` for protected endpoints.

### Auth
- `POST /auth/register` — Register a user
  - Body: `{ "email": "you@example.com", "password": "secret" }`
  - Response: `201 Created` with `{ "id": <id>, "email": "you@example.com" }`

- `POST /auth/login` — Login
  - Body: `{ "email": "you@example.com", "password": "secret" }`
  - Response: `200 OK` with `{ "token": "<jwt>" }`

### Habits (protected)
- `GET /habits/` — List current user's habits
- `POST /habits/` — Create habit (body: `{ "title": "Run", "frequency": "daily" }`)
- `GET /habits/<id>` — Get single habit
- `PUT /habits/<id>` — Update habit
- `DELETE /habits/<id>` — Delete habit

---

## Development workflow (recommended)

- Branching: use feature branches (`feature/`, `fix/`, `docs/`) off `master`/`main`.
- Commit messages: short summary, optional longer body. Follow conventional commits if desired.
- Tests: add tests in `tests/` and run before creating PRs.
- Pull requests: include description, link to issue, and testing steps.

---

## Deployment notes

- In production:
  - Use a production WSGI server (Gunicorn / uWSGI) behind a reverse proxy (NGINX).
  - Store `JWT_SECRET` and `SECRET_KEY` in environment variables or a secret manager — never commit them.
  - Use a proper database (Postgres / MySQL) instead of the default SQLite dev DB.
  - Use Flask-Migrate (Alembic) for schema migrations instead of `db.create_all()`.

---

## Troubleshooting & common errors

- `jwt.encode` types: ensure `JWT_SECRET` is present and a string; otherwise `TypeError` occurs.
- `passlib.exc.MissingBackendError`: install `bcrypt` or `passlib[bcrypt]`.
- `ValueError: password cannot be longer than 72 bytes`: bcrypt limitation; use `pbkdf2_sha256` or `bcrypt_sha256` in `passlib` or validate length.

---

## Security considerations

- Rotate `JWT_SECRET` carefully: rotation invalidates existing tokens.
- Use HTTPS in production.
- Enforce password rules and rate-limit login attempts.

---

## Contributing

Please open issues or pull requests. Keep changes small and add tests for new behavior.

---

## License

MIT

