# Pytest Fixtures Documentation

## Overview

The test suite uses pytest fixtures defined in `tests/conftest.py` to provide access to page objects and test infrastructure.

## Available Fixtures

### Main Fixture: `fixture_name`

The primary fixture that provides access to all page objects through a unified interface.

Guidance (abstract):
- Use the main fixture parameter in test functions (e.g., `sauce_ui`).
- Access page objects via `fixture.page_object_name` and call their methods.
- Do not redefine fixtures in tests.

**Available Page Objects:**
- `fixture_name.page_object1` - First page object instance
- `fixture_name.page_object2` - Second page object instance  
- `fixture_name.page_object3` - Third page object instance
- `fixture_name.page_object4` - Fourth page object instance

### Low-Level Fixtures

These are typically not used directly in tests but are available if needed:

- `browser` - Playwright Browser instance
- `page` - Playwright Page instance
- `web_driver` - WebDriver wrapper instance
- `db_connector` - Database connector (session-scoped)

## Fixture Structure

All page objects are accessed through the main fixture, which is an instance of the application wrapper class. This class initializes and provides access to all page objects.

Avoid including runnable examples in documentation; prefer describing the pattern:
- Navigate with `<fixture>.<page>.goto()`
- Perform actions with `<fixture>.<page>.<verb>(...)`
- Query state with `<fixture>.<page>.<property>`

## Important Notes

- **Always use the main fixture as the fixture parameter** in test functions
- **Access page objects via `fixture_name.page_object_name`** (e.g., `fixture_name.page_object1`)
- **Do not use individual page fixtures** - they don't exist
- The fixture automatically handles browser setup and teardown
- Each test gets a fresh browser context
