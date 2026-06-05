---
description: "Use when writing API tests for Flask routes in the wine app. Covers Flask test client setup, testing HTTP responses, status codes, redirects, and form submissions without a live server."
applyTo: "tests/test_*.py"
---
# API Test Standards

## What Are API Tests Here
- Tests that call Flask routes via the built-in test client
- No live server needed — use `app.test_client()` instead
- Cover HTTP status codes, response body content, redirects, and session state

## Test Client Setup
Always use a pytest fixture for the client:
```python
import pytest
from wine import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
```

## Test Structure
- Group tests by route in a class (e.g., `class LoginAPITests`, `class RegisterAPITests`)
- Use descriptive method names: `test_<route>_<condition>` (e.g., `test_login_invalid_credentials_returns_200`)

## Common Patterns
```python
# GET request
response = client.get('/health')
assert response.status_code == 200

# POST form submission
response = client.post('/login', data={'username': 'user', 'password': 'pass'})
assert b"Logged in successfully!" in response.data

# Redirect check
response = client.get('/logout')
assert response.status_code == 302
```

## Routes to Test
| Route | Methods | Notes |
|-------|---------|-------|
| `/health` | GET | Should return 200 |
| `/login` | GET, POST | POST with valid/invalid credentials |
| `/logout` | GET | Should redirect to `/login` |
| `/register` | GET, POST | POST validates email, username uniqueness |
| `/profile` | GET | Requires session — redirect if not logged in |
| `/predict` | POST | Submits 13 wine features, returns prediction |

## Database
- Mock `sqlite3.connect` with `unittest.mock.patch` — never mutate `wineusers.db` in tests
- For login tests that need a real DB lookup, use a fixture that inserts/removes a test account

## Assertions
- `assert response.status_code == 200` — success
- `assert response.status_code == 302` — redirect
- `assert b"some text" in response.data` — body content
