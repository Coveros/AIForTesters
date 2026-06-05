---
description: "Use when writing UI or browser tests using SeleniumBase for the wine app. Covers page interactions, assertions, login/logout helpers, and test structure."
---
# UI Test Standards (SeleniumBase)

## Framework
- Import: `from seleniumbase import BaseCase`
- All UI test classes extend `BaseCase`
- Run with: `python -m pytest tests/ -v --browser=chrome`
- The Flask dev server must be running at `http://127.0.0.1:5000` before running tests

## Test Structure
- Group tests by feature in a class (e.g., `class LoginTests(BaseCase)`)
- Use descriptive method names: `test_<action>_<condition>`
- Add inline comments for each logical step: open page → interact → assert

## Navigation & Interactions
```python
self.open("http://127.0.0.1:5000/login")   # navigate to page
self.type("#username", "value")             # type into input by CSS selector
self.click('button[type="submit"]')         # click element
self.click_link("Logout")                  # click a link by visible text
```

## Assertions
```python
self.assert_text("Logged in successfully!")     # text appears anywhere on page
self.assert_element("#username")                # element is present in DOM
self.wait_for_text("Logged in successfully!")   # wait then assert
```

## Login/Logout Helpers
When a test requires an authenticated session, define reusable `login()` and `logout()` helpers in the class:
```python
def login(self):
    self.open("http://127.0.0.1:5000/login")
    self.type("#username", "jefferyepayne")
    self.type("#password", "TestTest")
    self.click('button[type="submit"]')
    self.wait_for_text("Logged in successfully!")
    self.assert_text("Logged in successfully!")

def logout(self):
    self.click_link("Logout")
    self.assert_element("#username")
```
- Call `self.login()` at the start and `self.logout()` at the end of any test that needs authentication
- Do NOT duplicate login logic inline — always use the helper methods

## Selectors
- Prefer `#id` selectors for form fields (e.g., `#username`, `#password`, `#email`)
- Use `button[type="submit"]` for submit buttons
- Use `self.click_link("text")` for navigation links

## Routes Under Test
| Route | Purpose |
|-------|---------|
| `/login` | Login form — `#username`, `#password` |
| `/register` | Registration form — `#username`, `#password`, `#confirmpw`, `#email` |
| `/profile` | Change password — `#current_password`, `#new_password`, `#confirm_password` |
| `/predict` | Wine classifier form — 13 numeric feature inputs |
| `/logout` | Clears session, redirects to login |
