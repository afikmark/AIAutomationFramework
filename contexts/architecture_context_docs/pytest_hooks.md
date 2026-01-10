# Pytest Hooks Documentation

## Overview

The framework implements custom pytest hooks to enhance test execution, reporting, and integration with external systems like Xray test management.

## Hook Implementation

Hooks are implemented in:
- [plugins/reporter.py](../../plugins/reporter.py) - Allure reporter plugin with custom hooks
- [tests/conftest.py](../../tests/conftest.py) - Main fixture configuration

## Available Hooks

### 1. `pytest_addoption`

**Purpose:** Adds custom command-line options to pytest.

**Location:** `tests/conftest.py`

**Implementation:**
```python
def pytest_addoption(parser):
    """Add custom command-line options."""
    parser.addoption(
        "--base-url",
        action="store",
        default=os.getenv("BASE_URL", "https://www.saucedemo.com"),
        help="Base URL for the application under test"
    )
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run tests in headed mode (visible browser)"
    )
```

**Usage:**
```bash
# Use custom base URL
uv run pytest --base-url=https://staging.example.com tests/

# Run in headed mode
uv run pytest --headed tests/

# Combine options
uv run pytest --base-url=https://staging.example.com --headed tests/
```

### 2. `pytest_configure`

**Purpose:** Performs setup configuration when pytest starts.

**Location:** `plugins/reporter.py`

**Implementation:**
```python
def pytest_configure(config):
    """Configure Allure environment properties."""
    if hasattr(config, "workerinput"):
        return  # Skip for xdist workers
    
    alluredir = config.getoption("--alluredir")
    if not alluredir:
        return
    
    # Create allure results directory
    Path(alluredir).mkdir(parents=True, exist_ok=True)
    
    # Write environment properties
    env_properties = f"""
Browser=Chromium
Base.URL={config.getoption("--base-url", default="https://www.saucedemo.com")}
Python.Version={sys.version.split()[0]}
Playwright.Version=Latest
Test.Framework=Pytest
"""
    
    env_file = Path(alluredir) / "environment.properties"
    env_file.write_text(env_properties.strip())
```

**Result:** Creates environment metadata in Allure reports.

### 3. `pytest_runtest_setup`

**Purpose:** Runs before each test function executes.

**Location:** `plugins/reporter.py`

**Implementation:**
```python
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Setup hook to add test metadata before test execution."""
    # Extract test case key from markers
    test_case_key = None
    for marker in item.iter_markers(name="test_case_key"):
        if marker.args:
            test_case_key = marker.args[0]
            break
    
    # Add test case key to Allure metadata
    if test_case_key:
        allure.dynamic.label("test_case_key", test_case_key)
    
    # Add suite information
    if item.parent:
        suite_name = item.parent.name.replace("test_", "").replace(".py", "")
        allure.dynamic.suite(suite_name)
```

**Purpose:** Attaches test metadata (test case keys, suite names) to Allure reports.

### 4. `pytest_runtest_makereport`

**Purpose:** Processes test results after execution (captures screenshots, network errors).

**Location:** `plugins/reporter.py`

**Implementation:**
```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots and network errors on test failure."""
    outcome = yield
    report = outcome.get_result()
    
    # Only process on test call phase (not setup/teardown)
    if report.when == "call":
        # Capture screenshot on failure
        if report.failed:
            page = item.funcargs.get("page") or item.funcargs.get("authenticated_page")
            if page:
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
        
        # Attach network errors (both pass and fail)
        if hasattr(item, "_network_errors") and item._network_errors:
            network_errors_json = json.dumps(item._network_errors, indent=2)
            allure.attach(
                network_errors_json,
                name="network_errors",
                attachment_type=allure.attachment_type.JSON,
            )
```

**Features:**
- Automatically captures screenshot on test failure
- Attaches network errors (4xx, 5xx status codes) to reports
- Works with both `page` and `authenticated_page` fixtures

### 5. `pytest_sessionfinish`

**Purpose:** Runs after the entire test session completes.

**Location:** `plugins/reporter.py`

**Implementation:**
```python
def pytest_sessionfinish(session, exitstatus):
    """Session finish hook to add final metadata."""
    alluredir = session.config.getoption("--alluredir")
    if not alluredir:
        return
    
    # Add browser info if available
    if hasattr(session.config, "_browser_info"):
        browser_info = session.config._browser_info
        # Write categories or additional metadata
```

**Purpose:** Finalizes Allure report metadata after session completes.

## Hook Execution Order

```
pytest_configure
    └─> Configure Allure environment properties
    └─> Create allure results directory

Test Session Start
    └─> Session-scoped fixtures run (auth_state_file, base_url)

For Each Test:
    pytest_runtest_setup
        └─> Add test metadata (test case key, suite)
    
    Test Execution
        └─> Fixtures run (browser, page, logged_in_user)
        └─> Test function executes
    
    pytest_runtest_makereport
        └─> Check test result (pass/fail)
        └─> Capture screenshot if failed
        └─> Attach network errors
        └─> Create Allure report entry

Test Session End
    pytest_sessionfinish
        └─> Finalize Allure metadata
        └─> Write session summary
```

## Custom Markers

### `test_case_key` - Xray Test Case Identifier

**Purpose:** Links pytest test to Xray test case in Jira.

**Usage:**
```python
@pytest.mark.test_case_key("DEV-51")
def test_cart_page_loads(logged_in_user):
    """Test cart page loads successfully."""
    pass
```

**Result:** 
- Test case key appears in Allure report metadata
- Can be used for Xray test execution updates
- Enables traceability between tests and Jira issues

## Hook Best Practices

### 1. Use `hookimpl` Decorators

```python
# Specify execution order
@pytest.hookimpl(tryfirst=True)  # Run early
def pytest_runtest_setup(item):
    pass

@pytest.hookimpl(trylast=True)   # Run late
def pytest_runtest_teardown(item):
    pass

@pytest.hookimpl(hookwrapper=True)  # Wrap around other hooks
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
```

### 2. Check for xdist Workers

When using pytest-xdist for parallel execution:

```python
def pytest_configure(config):
    """Skip configuration for xdist workers."""
    if hasattr(config, "workerinput"):
        return  # Skip for worker processes
    # Main process configuration
```

### 3. Handle Missing Fixtures Gracefully

```python
def pytest_runtest_makereport(item, call):
    # Check if fixture exists before accessing
    page = item.funcargs.get("page") or item.funcargs.get("authenticated_page")
    if page:
        # Use page fixture
        pass
```

### 4. Use Proper Report Phases

```python
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # report.when can be: "setup", "call", "teardown"
    if report.when == "call":
        # Only process during test execution phase
        pass
```

## Common Hook Use Cases

### 1. Add Custom Metadata to All Tests

```python
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Add custom metadata to every test."""
    allure.dynamic.label("team", "QA Automation")
    allure.dynamic.label("environment", "staging")
```

### 2. Conditional Test Skipping

```python
def pytest_runtest_setup(item):
    """Skip tests based on conditions."""
    if "requires_api" in item.keywords and not api_available():
        pytest.skip("API not available")
```

### 3. Custom Test Reporting

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.failed:
        # Send notification, update dashboard, etc.
        notify_team(f"Test {item.name} failed")
```

### 4. Test Duration Tracking

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        duration = report.duration
        allure.dynamic.label("duration", f"{duration:.2f}s")
```

## Integration with Allure

The hooks work seamlessly with Allure reporting:

```python
import allure

# Dynamic labels
allure.dynamic.label("key", "value")
allure.dynamic.feature("Feature Name")
allure.dynamic.story("Story Name")
allure.dynamic.suite("Suite Name")
allure.dynamic.title("Test Title")
allure.dynamic.severity(allure.severity_level.CRITICAL)

# Attachments
allure.attach(data, name="name", attachment_type=allure.attachment_type.JSON)
allure.attach.file(path, name="name", attachment_type=allure.attachment_type.PNG)
```

## Debugging Hooks

### Enable Verbose Output

```bash
# See hook execution order
uv run pytest --setup-show tests/

# See fixture setup and teardown
uv run pytest -v --setup-show tests/

# Enable pytest debug output
uv run pytest --debug tests/
```

### Print Hook Information

```python
def pytest_runtest_setup(item):
    """Debug hook execution."""
    print(f"\n=== Setup for test: {item.name} ===")
    print(f"Markers: {[m.name for m in item.iter_markers()]}")
    print(f"Fixtures: {item.fixturenames}")
```

## Related Documentation

- [Fixtures](fixtures.md) - Pytest fixtures documentation
- [Allure Reporting](allure_reporting.md) - Allure integration details
- [Test Organization](test_organization.md) - Test structure conventions

## Related Files

- [plugins/reporter.py](../../plugins/reporter.py) - Reporter plugin with hooks
- [tests/conftest.py](../../tests/conftest.py) - Main configuration and hooks

## References

- [Pytest Hook Reference](https://docs.pytest.org/en/stable/reference/reference.html#hooks)
- [Pytest Plugin Development](https://docs.pytest.org/en/stable/how-to/writing_plugins.html)
- [Allure Pytest Plugin](https://docs.qameta.io/allure/#_pytest)
