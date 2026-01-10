# Allure Reporting Integration

## Overview

The framework integrates Allure Framework for rich, interactive HTML test reports with comprehensive test documentation, screenshots, network request tracking, and detailed test metadata.

## Installation

Allure-pytest plugin is already installed in the project:

```bash
uv add allure-pytest
```

## Configuration

### Pytest Integration

The Allure plugin is automatically configured via the `plugins.reporter` module which is loaded in `tests/conftest.py`:

```python
pytest_plugins = ["plugins.reporter"]
```

### Automatic Metadata Extraction

The framework **automatically** extracts Allure metadata from your test structure using pytest hooks. You don't need to manually add `@allure.feature()` or `@allure.title()` decorators.

**What's Automatic:**
- **Title**: Extracted from test function name (e.g., `test_login_success` → "Login Success")
- **Description**: Extracted from docstring first paragraph
- **Steps**: Extracted from docstring "Steps:" section
- **Suite**: Extracted from `TEST_SUITE_NAME` module constant
- **Tags**: Automatically added based on fixtures (`sauce_ui` → "UI test", `pet_store_controller` → "API test")
- **Severity**: Automatically set based on markers (`@pytest.mark.sanity` → CRITICAL)
- **Jira Links**: Automatically created from `@pytest.mark.test_case_key("DEV-123")` marker

**Example Test Structure:**

```python
from plugins.reporter import reporter

TEST_SUITE_NAME = "SauceDemo Login Page Tests"

@pytest.mark.sanity
@pytest.mark.test_case_key("DEV-67")
def test_login_with_valid_credentials(sauce_ui):
    """Test successful login with valid credentials.
    
    Verifies that user can log in and is redirected to inventory page.
    
    Steps:
        1) Navigate to login page
        2) Enter valid credentials
        3) Click login button
        4) Verify redirect to inventory page
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")
    reporter.assert_that(sauce_ui.page.url).ends_with("/inventory.html")
```

**Result in Allure Report:**
- Title: "Login With Valid Credentials"
- Suite: "SauceDemo Login Page Tests"
- Description: "Test successful login with valid credentials. Verifies that user can log in and is redirected to inventory page."
- Steps: Automatically numbered steps from docstring + assertion step
- Tags: "UI test", "Jira key - DEV-67"
- Severity: CRITICAL (from @pytest.mark.sanity)
- Link: Jira issue DEV-67

## Features

### 1. Automatic Screenshot Capture

Screenshots are automatically captured on test failure via pytest hooks:

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots on test failure."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Capture screenshot if page fixture is available
        if "page" in item.funcargs or "authenticated_page" in item.funcargs:
            page = item.funcargs.get("page") or item.funcargs.get("authenticated_page")
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
```

### 2. Network Request Tracking

Failed HTTP requests (status >= 400) are automatically tracked and attached to test reports:

```python
def handle_response(response):
    """Capture HTTP responses with error status codes (4xx, 5xx)."""
    status = response.status
    
    if status >= 400:
        error_data = {
            "url": response.url,
            "status": status,
            "statusText": response.status_text,
            "method": response.request.method,
            "timestamp": datetime.now().isoformat(),
            "resourceType": response.request.resource_type,
        }
        request.node._network_errors.append(error_data)
```

Network errors are attached to Allure reports via the reporter plugin.

### 3. Test Metadata

The framework automatically captures and attaches:

- **Test Case Keys**: Xray test case identifiers from pytest markers
- **Browser Information**: Browser name, version, and headless mode
- **Environment Details**: Captured via pytest hooks
- **Test Execution Context**: Base URL, timestamp, duration

### 4. Automatic Assertion Steps

The framework provides `reporter.assert_that()` which automatically creates Allure steps for assertions:

```python
from plugins.reporter import reporter

def test_example(logged_in_user):
    # Each assertion creates an Allure step automatically
    reporter.assert_that(logged_in_user.page.url).ends_with("/inventory.html")
    # Step created: "Assert that 'https://www.saucedemo.com/inventory.html' ends with '/inventory.html'"
    
    reporter.assert_that(logged_in_user.cart_page.get_item_count()).is_equal_to(2)
    # Step created: "Assert that 2 is equal to 2"
    
    reporter.assert_that(product_name).contains("Backpack")
    # Step created: "Assert that 'Sauce Labs Backpack' contains 'Backpack'"
```

**Benefits:**
- Automatic Allure step creation for every assertion
- Clear assertion messages in reports
- Uses assertpy under the hood (supports all assertpy assertions)
- Chainable assertions with automatic steps

### 5. Manual Allure Steps (When Needed)

For custom steps not covered by assertions, use `reporter.step()`:

```python
from plugins.reporter import reporter

def test_checkout_flow(logged_in_user):
    with reporter.step("Add multiple items to cart"):
        logged_in_user.inventory_page.add_to_cart("Backpack")
        logged_in_user.inventory_page.add_to_cart("Bike Light")
    
    with reporter.step("Navigate to checkout"):
        logged_in_user.cart_page.goto()
        logged_in_user.cart_page.checkout()
```

### 6. Custom Attachments (Advanced)

For custom data attachments (rarely needed):

```python
import allure

def test_example():
    # Attach text
    allure.attach("Important test data", name="data", attachment_type=allure.attachment_type.TEXT)
    
    # Attach JSON
    allure.attach(json.dumps({"key": "value"}), name="json_data", attachment_type=allure.attachment_type.JSON)
```

## Running Tests with Allure

### Generate Allure Results

Run tests and generate Allure result files:

```bash
# Run all tests and generate results
uv run pytest tests/ --alluredir=allure-results

# Run specific test suite
uv run pytest tests/sauce_ui/ --alluredir=tests/sauce_ui/allure-results

# Run with custom markers
uv run pytest -m sanity --alluredir=allure-results
```

### View Allure Report

Generate and serve the HTML report:

```bash
# Generate and open report (opens browser automatically)
allure serve allure-results

# Generate report to specific directory
allure generate allure-results -o allure-report --clean

# Open existing report
allure open allure-report
```

### CI/CD Integration

For CI/CD pipelines, generate static reports:

```bash
# Generate static HTML report
allure generate allure-results -o allure-report --clean

# Report can be served as static HTML or uploaded to artifact storage
```

## Report Structure

The generated Allure report includes:

### Dashboards
- **Overview**: Total tests, pass/fail rate, duration
- **Categories**: Test failures by category
- **Suites**: Tests organized by test suite
- **Graphs**: Visual representation of test results
- **Timeline**: Test execution timeline
- **Behaviors**: Tests organized by features and stories

### Test Details
Each test includes:
- Test description and title
- Test steps (if using `allure.step`)
- Screenshots on failure
- Network errors (failed requests)
- Browser information
- Execution time and timestamp
- Test case keys (Xray integration)
- Severity level
- Full stack trace on failure

## Best Practices

### 1. Write Descriptive Test Names

Test function names are automatically converted to titles:

```python
# ✅ GOOD: Clear, descriptive test name
def test_cart_displays_correct_item_count_after_adding_products(logged_in_user):
    # Title: "Cart Displays Correct Item Count After Adding Products"
    pass

# ❌ BAD: Vague test name
def test_cart(logged_in_user):
    # Title: "Cart" (not descriptive)
    pass
```

### 2. Use Module-Level TEST_SUITE_NAME

Organize tests into logical suites:

```python
# At the top of test_checkout_page.py
TEST_SUITE_NAME = "SauceDemo Checkout Page Tests"

# All tests in this file will be grouped under this suite in Allure
```

### 3. Write Structured Docstrings

Include description and steps in your docstrings:

```python
def test_checkout_flow(logged_in_user):
    """Test complete checkout process from cart to order confirmation.
    
    Verifies that user can successfully complete a purchase including
    entering shipping information and payment details.
    
    Steps:
        1) Add items to cart
        2) Navigate to checkout
        3) Enter shipping information
        4) Enter payment information
        5) Complete order
        6) Verify order confirmation
    """
    # Test implementation
```

**Result:** Description and steps automatically appear in Allure report.

### 4. Use Severity Markers

Set severity using pytest markers (automatic Allure severity assignment):

```python
@pytest.mark.smoke   # → Severity: BLOCKER
def test_login(sauce_ui):
    pass

@pytest.mark.sanity  # → Severity: CRITICAL
def test_add_to_cart(logged_in_user):
    pass

# For custom severity, add to MARKER_SEVERITY_RULES in plugins/reporter.py
```

### 5. Link Tests to Jira

Use `test_case_key` marker for automatic Jira linking:

```python
@pytest.mark.test_case_key("DEV-123")
def test_login_success(sauce_ui):
    """Test successful login."""
    pass

# Automatically creates:
# - Tag: "Jira key - DEV-123"
# - Link: To Jira issue DEV-123
```

### 6. Use reporter.assert_that() for All Assertions

Replace standard assertions with reporter assertions:

```python
# ✅ GOOD: Creates automatic Allure step
reporter.assert_that(page.url).ends_with("/inventory.html")
reporter.assert_that(item_count).is_equal_to(3)

# ❌ BAD: No Allure step created
assert page.url.endswith("/inventory.html")
assert item_count == 3
```

### 7. Use Custom Steps for Complex Operations

For multi-step operations, use `reporter.step()`:

```python
def test_checkout_flow(logged_in_user):
    with reporter.step("Add multiple products to cart"):
        logged_in_user.inventory_page.add_to_cart("Backpack")
        logged_in_user.inventory_page.add_to_cart("Bike Light")
        logged_in_user.inventory_page.add_to_cart("T-Shirt")
    
    with reporter.step("Proceed to checkout"):
        logged_in_user.cart_page.goto()
        logged_in_user.cart_page.checkout()
```

## Troubleshooting

### Report Not Generated

Ensure the `--alluredir` flag is provided:
```bash
uv run pytest --alluredir=allure-results
```

### Missing Screenshots

Verify that the page fixture is being used in the test:
```python
def test_example(page):  # or authenticated_page
    # Test implementation
```

### Network Errors Not Shown

The reporter plugin automatically tracks network errors. Ensure:
1. Test is using `page` or `authenticated_page` fixture
2. The reporter plugin is loaded in conftest.py
3. Test fails with network errors during execution

## Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Run tests with Allure
  run: |
    uv run pytest tests/ --alluredir=allure-results
    
- name: Generate Allure Report
  run: |
    allure generate allure-results -o allure-report --clean
    
- name: Upload Allure Report
  uses: actions/upload-artifact@v3
  with:
    name: allure-report
    path: allure-report
```

### GitLab CI Example

```yaml
test:
  script:
    - uv run pytest tests/ --alluredir=allure-results
    - allure generate allure-results -o allure-report --clean
  artifacts:
    paths:
      - allure-report
    when: always
```

## Related Files

- [plugins/reporter.py](../../plugins/reporter.py) - Allure reporter plugin implementation
- [tests/conftest.py](../../tests/conftest.py) - Pytest fixtures with network tracking
- [.gitignore](../../.gitignore) - Excludes `allure-results/` from version control

## References

- [Allure Framework Documentation](https://allurereport.org/)
- [Allure-Pytest Plugin](https://docs.qameta.io/allure/#_pytest)
- [Allure Report Examples](https://demo.qameta.io/allure/)
