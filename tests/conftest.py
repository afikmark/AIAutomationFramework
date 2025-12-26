"""
Pytest configuration file with fixtures for UI automation testing.
"""

import pytest
from typing import Generator
from playwright.sync_api import sync_playwright, Page, Browser
from dotenv import load_dotenv
from core.controllers.pet_store_controller import PetStoreController
from core.web.pages.sauce_demo import SauceDemo

load_dotenv()


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
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser: Browser) -> Generator[Page, None, None]:
    """
    Fixture that provides a page instance.

    Args:
        browser (Browser): Playwright browser instance

    Yields:
        Page: Playwright page object
    """
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def sauce_ui(page: Page) -> SauceDemo:
    """
    Fixture that provides a SauceDemo instance with access to all page objects.

    Args:
        page (Page): Playwright page object

    Returns:
        SauceDemo: SauceDemo instance with all page objects
    """
    return SauceDemo(page)


@pytest.fixture(scope="function")
def pet_store_controller() -> PetStoreController:
    """
    Fixture that provides a PetStoreController instance.

    Returns:
        PetStoreController: PetStoreController instance
    """

    return PetStoreController()
