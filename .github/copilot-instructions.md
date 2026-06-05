# AIForTesters Project Guidelines

## Stack
- Python Flask web application with Jinja2 HTML templates
- SQLite database (`wineusers.db`) for user accounts
- scikit-learn ML model loaded from `model.pkl`
- UI tests use SeleniumBase (`from seleniumbase import BaseCase`)
- Unit and API tests use pytest
- Flask dev server runs on `http://127.0.0.1:5000`

## Project Structure
- `wine.py` — Flask app entry point (routes: `/`, `/login`, `/logout`, `/register`, `/profile`, `/predict`, `/health`)
- `tests/` — all test files, named `test_*.py`
- `templates/` — Jinja2 HTML templates
- `static/` — static assets

## Testing Standards
- All tests live in `tests/`, named `test_*.py`
- Run tests with: `python -m pytest tests/ -v --browser=chrome`
- The Flask server must be running before executing UI or API tests
- Use the `/health` endpoint to confirm the server is up before tests
- Tests are organized into classes that group related scenarios

## Code Style
- Follow PEP 8
- Use SQLite parameterized queries — never string-format SQL (prevent injection)
- Route handlers validate session before rendering protected pages
