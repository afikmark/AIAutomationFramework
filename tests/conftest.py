"""
Pytest configuration file with fixtures for UI automation testing.
"""

pytest_plugins = ["plugins.reporter"]

import pytest
from typing import Generator
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser
from dotenv import load_dotenv
from core.controllers.pet_store_controller import PetStoreController
from core.web.pages.sauce_demo import SauceDemo
import allure

load_dotenv()


@pytest.fixture(scope="session")
def auth_state_file(base_url: str) -> str:
    """
    Session-scoped fixture that performs login once and saves authentication state.
    This runs once at the start of the test session.
    Always runs in headless mode to avoid system-level browser compatibility issues.

    Args:
        base_url: Base URL from pytest configuration

    Returns:
        str: Path to the authentication state file
    """
    auth_file = "playwright/.auth/user.json"
    auth_path = Path(auth_file)

    auth_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(base_url=base_url)
        page = context.new_page()

        # Perform login
        page.goto("/")
        page.get_by_role("textbox", name="Username").fill("standard_user")
        page.get_by_role("textbox", name="Password").fill("secret_sauce")
        page.get_by_role("button", name="Login").click()
        page.wait_for_url("**/inventory.html")

        # Save authentication state
        context.storage_state(path=auth_file)

        browser.close()

    return auth_file


@allure.title("browser: Returns a playwright browser instance")
@pytest.fixture(scope="function")
def browser(request) -> Generator[Browser, None, None]:
    """
    Fixture that provides a browser instance.
    Headless by default, use --headed to show browser.

    Yields:
        Browser: Playwright browser object
    """
    # Use --headed option from pytest-playwright
    headless = not request.config.getoption("--headed", default=False)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        if not hasattr(request.config, "_browser_info"):
            request.config._browser_info = {
                "name": browser.browser_type.name.capitalize(),
                "version": browser.version,
                "headless": str(headless),
            }

        yield browser
        browser.close()


@allure.title("page: Returns a playwright page instance")
@pytest.fixture(scope="function")
def page(browser: Browser, request) -> Generator[Page, None, None]:
    """
    Fixture that provides a page instance with network error tracking.
    Use this for unauthenticated tests (e.g., login tests).

    Args:
        browser (Browser): Playwright browser instance
        request: Pytest request fixture for accessing test item

    Yields:
        Page: Playwright page object
    """
    context = browser.new_context()
    page = context.new_page()

    if not hasattr(request.node, "_network_errors"):
        request.node._network_errors = []

    def handle_response(response):
        """Capture HTTP responses with error status codes (4xx, 5xx)."""
        status = response.status

        if status >= 400:
            from datetime import datetime

            error_data = {
                "url": response.url,
                "status": status,
                "statusText": response.status_text,
                "method": response.request.method,
                "timestamp": datetime.now().isoformat(),
                "resourceType": response.request.resource_type,
            }
            request.node._network_errors.append(error_data)

    page.on("response", handle_response)

    yield page

    page.remove_listener("response", handle_response)
    context.close()


@allure.title("authenticated_page: Returns a playwright page with auth state")
@pytest.fixture(scope="function")
def authenticated_page(
    browser: Browser, request, auth_state_file: str
) -> Generator[Page, None, None]:
    """
    Fixture that provides a page instance with authentication state pre-loaded.
    Use this for tests that require an authenticated user.

    Args:
        browser (Browser): Playwright browser instance
        request: Pytest request fixture for accessing test item
        auth_state_file: Path to authentication state file

    Yields:
        Page: Playwright page object with authentication
    """
    context = browser.new_context(storage_state=auth_state_file)
    page = context.new_page()

    if not hasattr(request.node, "_network_errors"):
        request.node._network_errors = []

    def handle_response(response):
        """Capture HTTP responses with error status codes (4xx, 5xx)."""
        status = response.status

        if status >= 400:
            from datetime import datetime

            error_data = {
                "url": response.url,
                "status": status,
                "statusText": response.status_text,
                "method": response.request.method,
                "timestamp": datetime.now().isoformat(),
                "resourceType": response.request.resource_type,
            }
            request.node._network_errors.append(error_data)

    page.on("response", handle_response)

    yield page

    page.remove_listener("response", handle_response)
    context.close()


@allure.title("sauce_ui: Returns a SauceDemo instance with all page objects")
@pytest.fixture(scope="function")
def sauce_ui(page: Page, base_url: str) -> SauceDemo:
    """
    Fixture that provides a SauceDemo instance with access to all page objects.

    Args:
        page (Page): Playwright page object
        base_url (str): Base URL from pytest configuration

    Returns:
        SauceDemo: SauceDemo instance with all page objects
    """
    return SauceDemo(page, base_url)


@allure.title("pet_store_controller: Returns a PetStoreController instance")
@pytest.fixture(scope="function")
def pet_store_controller() -> PetStoreController:
    """
    Fixture that provides a PetStoreController instance.

    Returns:
        PetStoreController: PetStoreController instance
    """

    return PetStoreController()


@allure.title("logged_in_user: Returns a logged-in SauceDemo instance")
@pytest.fixture(scope="function")
def logged_in_user(authenticated_page: Page, base_url: str) -> SauceDemo:
    """
    Fixture that provides a SauceDemo instance with user already authenticated.
    Uses pre-saved authentication state for fast, isolated test execution.
    Navigates to inventory page to activate the authenticated session.

    Args:
        authenticated_page: Page fixture with authentication state loaded
        base_url: Base URL from pytest configuration

    Returns:
        SauceDemo: SauceDemo instance with user authenticated at inventory page
    """
    sauce_demo = SauceDemo(authenticated_page, base_url)
    # Navigate to inventory page to activate the authenticated session
    sauce_demo.inventory_page.navigate_to_page()
    return sauce_demo
