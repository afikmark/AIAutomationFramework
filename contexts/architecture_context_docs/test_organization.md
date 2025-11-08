# Test Organization (Concise)

## 1) Location
- Place all tests under `tests/`.
- Keep fixtures in `tests/conftest.py`.

## 2) File Naming
- Use `test_<feature_or_component>.py`.
- Choose clear, specific names (avoid generic or numbered files).

## 3) Grouping
- Group tests by feature/page/component in the same file.
- Examples of grouping (by file):
  - Login-related tests → `test_login.py`
  - Inventory page tests → `test_inventory_page.py`

## 4) Directory Structure (example)
```
tests/
├── conftest.py
├── test_login.py
```
