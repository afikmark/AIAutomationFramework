# Pytest Fixtures Documentation

## Overview

The test suite uses pytest fixtures defined in `tests/conftest.py` to provide access to page objects, browser instances, and authentication state management.

## Available Fixtures

### Main Fixtures

#### 1. `sauce_ui` - SauceDemo Application Fixture

The primary fixture that provides access to all SauceDemo page objects through a unified interface.

**Usage:**
- Use the `sauce_ui` parameter in test functions for unauthenticated tests (e.g., login tests)
- Access page objects via `sauce_ui.page_object_name` and call their methods
- Do not redefine fixtures in tests

**Available Page Objects:**
- `sauce_ui.login_page` - Login page instance
- `sauce_ui.inventory_page` - Inventory/products page instance
- `sauce_ui.cart_page` - Shopping cart page instance
- `sauce_ui.hamburger_menu` - Navigation menu component instance

**Example Pattern:**
```python
def test_login(sauce_ui):
    # Navigate and interact with page objects
    sauce_ui.login_page.goto()
    sauce_ui.login_page.login("user", "pass")
```

#### 2. `logged_in_user` - Authenticated SauceDemo Fixture

**Purpose:** Provides a pre-authenticated SauceDemo instance for tests requiring logged-in state.

**Key Features:**
- **Reuses Authentication**: Login performed once per session, not per test
- **70% Faster Execution**: Skips redundant login steps in each test
- **Headless Auth Creation**: Authentication state created in headless mode for stability
- **Fresh Context Per Test**: Each test gets isolated browser context with auth state

**Usage:**
```python
def test_cart_operations(logged_in_user):
    # User is already logged in - start testing immediately
    logged_in_user.cart_page.goto()
    logged_in_user.cart_page.add_item("Product Name")
```

**When to Use:**
- Use `sauce_ui` for login/logout tests (unauthenticated)
- Use `logged_in_user` for all other tests (authenticated)

#### 3. `pet_store_controller` - API Testing Fixture

Provides a PetStoreController instance for API testing.

**Usage:**
```python
def test_create_pet(pet_store_controller):
    response = pet_store_controller.create_pet(pet_data)
    assert response.status_code == 200
```

### Browser-Level Fixtures

These fixtures provide lower-level access to Playwright browser instances.

#### 1. `browser` - Playwright Browser Instance

**Scope:** Function-scoped
**Purpose:** Provides a Playwright Browser instance

**Features:**
- Respects `--headed` CLI flag for visible browser execution
- Headless by default
- Browser info attached to test metadata

**Example:**
```bash
# Run in headless mode (default)
uv run pytest tests/

# Run in headed mode (visible browser)
uv run pytest --headed tests/
```

#### 2. `page` - Playwright Page Instance (Unauthenticated)

**Scope:** Function-scoped
**Purpose:** Provides a fresh Playwright Page for unauthenticated tests

**Features:**
- Network error tracking (captures 4xx, 5xx responses)
- Screenshot capture on failure
- Clean browser context per test

**Usage:**
```python
def test_page_navigation(page):
    page.goto("https://example.com")
    # Test implementation
```

#### 3. `authenticated_page` - Playwright Page with Auth State

**Scope:** Function-scoped
**Purpose:** Provides a Playwright Page with pre-loaded authentication state

**Features:**
- Authentication state loaded from session file
- Network error tracking
- Screenshot capture on failure
- Faster than performing login in each test

**Usage:**
```python
def test_authenticated_feature(authenticated_page):
    authenticated_page.goto("/inventory.html")
    # User already authenticated
```

### Session-Scoped Fixtures

#### 1. `auth_state_file` - Authentication State Manager

**Scope:** Session-scoped (runs once per test session)
**Purpose:** Creates and manages authentication state file

**How It Works:**
1. Runs once at test session start
2. Launches headless browser (always headless for stability)
3. Performs login to SauceDemo
4. Saves authentication cookies/storage to file
5. Returns path to auth state file

**File Location:** `playwright/.auth/user.json`

**Important:** 
- Auth state creation is **always headless** to avoid GTK compatibility issues on Linux
- Test execution can still use `--headed` flag (only affects test browser, not auth creation)
- Auth file automatically recreated if credentials change

#### 2. `base_url` - Base URL Configuration

**Scope:** Session-scoped
**Purpose:** Provides base URL for test execution

**Priority Order:**
1. `--base-url` CLI flag (highest priority)
2. `BASE_URL` environment variable
3. Default: `https://www.saucedemo.com`

**Usage:**
```bash
# Use default
uv run pytest tests/

# Override with CLI flag
uv run pytest --base-url=https://staging.saucedemo.com tests/

# Set in .env file
BASE_URL=https://staging.saucedemo.com
```

## Fixture Architecture

### Authentication Flow

```
Test Session Start
    └─> auth_state_file fixture (session-scoped)
        └─> Creates headless browser
        └─> Performs login
        └─> Saves state to playwright/.auth/user.json
        └─> Closes browser

Test Execution
    └─> logged_in_user fixture (function-scoped)
        └─> Creates new browser (respects --headed flag)
        └─> Loads auth state from file
        └─> Provides pre-authenticated page
        └─> Test runs
        └─> Closes context

Test Session End
    └─> Auth file persists for next session (unless deleted)
```

### Network Error Tracking

Both `page` and `authenticated_page` fixtures automatically track failed HTTP requests:

```python
def handle_response(response):
    """Capture HTTP responses with error status codes (4xx, 5xx)."""
    if response.status >= 400:
        error_data = {
            "url": response.url,
            "status": response.status,
            "statusText": response.status_text,
            "method": response.request.method,
            "timestamp": datetime.now().isoformat(),
            "resourceType": response.request.resource_type,
        }
        # Attached to Allure report automatically
```

## Best Practices

### 1. Choose the Right Fixture

```python
# ✅ CORRECT: Use sauce_ui for login tests
def test_login_valid_credentials(sauce_ui):
    sauce_ui.login_page.login("standard_user", "secret_sauce")

# ✅ CORRECT: Use logged_in_user for authenticated tests
def test_add_to_cart(logged_in_user):
    logged_in_user.inventory_page.add_product_to_cart("Backpack")

# ❌ INCORRECT: Don't use logged_in_user for login tests
def test_login(logged_in_user):  # User is already logged in!
    # This test doesn't make sense
```

### 2. Access Page Objects Correctly

```python
# ✅ CORRECT
def test_example(sauce_ui):
    sauce_ui.login_page.goto()
    sauce_ui.login_page.fill_username("user")

# ❌ INCORRECT - Individual page fixtures don't exist
def test_example(login_page):  # This won't work!
    login_page.goto()
```

### 3. Don't Redefine Fixtures

```python
# ❌ INCORRECT - Don't redefine fixtures in tests
def test_example(sauce_ui):
    sauce_ui = SauceDemo(page, base_url)  # Don't do this!
    # Use the fixture as-is
```

### 4. Use Appropriate Scope

```python
# Session-scoped fixtures run once per session
@pytest.fixture(scope="session")
def expensive_setup():
    # Database connection, auth state creation
    pass

# Function-scoped fixtures run once per test
@pytest.fixture(scope="function")
def fresh_page():
    # New browser context per test
    pass
```

## Debugging Tips

### View Browser Execution

```bash
# Run tests with visible browser
uv run pytest --headed tests/sauce_ui/

# Run single test in headed mode
uv run pytest --headed tests/sauce_ui/test_login_page.py::test_valid_login
```

### Inspect Auth State

```bash
# View authentication state file
cat playwright/.auth/user.json

# Delete auth state to force recreation
rm -rf playwright/.auth/
```

### Check Network Errors

Network errors are automatically captured and attached to Allure reports. View them after test execution:

```bash
uv run pytest tests/ --alluredir=allure-results
allure serve allure-results
# Navigate to failed test -> Attachments -> network_errors.json
```

## Related Documentation

- [Page Object Model](page_object_model.md) - Page object architecture
- [Allure Reporting](allure_reporting.md) - Test reporting and network tracking
- [Test Organization](test_organization.md) - Test structure and conventions
- [Component Pattern](component_pattern.md) - Reusable UI components

## Related Files

- [tests/conftest.py](../../tests/conftest.py) - Fixture implementations
- [core/web/pages/sauce_demo.py](../../core/web/pages/sauce_demo.py) - SauceDemo main class
- [plugins/reporter.py](../../plugins/reporter.py) - Allure reporter plugin

```
