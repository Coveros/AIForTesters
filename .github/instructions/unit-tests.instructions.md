---
description: "Use when writing unit tests for Python functions, classes, or the wine classifier model. Covers test structure, naming, fixtures, mocking, and assertions for pure logic tests that do not require a running server."
applyTo: "tests/test_*.py"
---
# Unit Test Standards

## What Are Unit Tests Here
- Tests for pure Python functions and the scikit-learn wine classifier model
- Import directly from `wine.py` — no Flask server required
- Isolate logic from external dependencies (database, file I/O)

## Test Structure
- All tests live in `tests/`, named `test_*.py`
- Group related tests in a class (e.g., `class ClassifierTests`)
- Use descriptive method names: `test_<action>_<condition>` (e.g., `test_predict_returns_valid_variety`)

## Data-Driven Tests
Use `pytest.mark.parametrize` for testing the classifier across multiple inputs:
```python
import pytest

@pytest.mark.parametrize("features,expected", [
    ([14, 1, 10, 15, 125, 2, 2, 0.5, 1, 7, 0.7, 2, 1000], 0),
])
def test_predict_variety(features, expected):
    result = model.predict([features])
    assert result[0] == expected
```

## Mocking
- Mock `sqlite3.connect` with `unittest.mock.patch` to avoid touching `wineusers.db`
- Mock file I/O (e.g., `pickle.load`) when testing model loading logic

## Assertions
- Assert return values directly: `assert result == expected`
- Assert types when relevant: `assert isinstance(result, int)`
- Keep each test focused on one behavior
