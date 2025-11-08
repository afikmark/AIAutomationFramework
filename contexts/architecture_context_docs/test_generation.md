# Test Generation Guidelines (Concise)

## Pre-Test Generation Checklist

Before writing tests:
1. ☐ Page object class exists
2. ☐ All required methods implemented
3. ☐ Properties for state queries defined
4. ☐ No locators exposed to test layer

Then write tests using page object API only.

## Fundamentals

- Function-based tests only (no classes).
- One scenario per test, minimal steps.

## 1) Function Naming (abstract)

```python
def test_action_under_condition(sauce_ui):
    ...
```

## 2) Docstring (abstract)

```python
"""
What is verified, how it’s exercised, expected outcome.
Args: sauce_ui – fixture providing page objects
Steps: 1) navigate 2) act 3) assert
"""
```

## 3) Fixture Usage

- Use `sauce_ui` from `tests/conftest.py`.
- Access page objects via `sauce_ui.<page>.<method_or_property>`.

## 4) Assertion with Message (abstract)

```python
assert condition, "descriptive failure message"
```

## 5) Parametrization (abstract)

```python
import pytest

@pytest.mark.parametrize("input_value, expected", [
    (..., ...),
    (..., ...),
])
def test_scenario(sauce_ui, input_value, expected):
    ...
    assert result == expected, "message"
```

## 6) `sauce_ui` Fixture Usage

- Primary entry to page objects and their APIs.
- Do not import page classes; call existing methods/properties via `sauce_ui`.
- Every page object has a 'goto' method, use it when needed.

## WHEN

- Parametrization: use when a single flow repeats with different arguments.
- Imports: only when needed (e.g., `pytest` for parametrization/marks).

## DONT

- Don’t create multiple test functions for the same flow (use parametrization).
- Don’t import pages or methods; use the `sauce_ui` fixture to access them.
- Don’t add imports when not needed.
- Don’t call methods/properties that do not exist.
- Don’t use try/except in tests.
- Don’t use page locators directly; page objects provide the required APIs.
- Don't create comments, keep the test clean and readable.

BAD❌:
```python
    # Try to access inventory page directly without logging in
    sauce_ui.page.goto(f"{sauce_ui.base_url}/inventory.html")
```
GOOD✅:
```PYTHON
    sauce_ui.page.goto(f"{sauce_ui.base_url}/inventory.html")
```
