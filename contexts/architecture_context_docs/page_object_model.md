# Page Object Model (POM) Pattern

## Overview

The Page Object Model (POM) is a design pattern where each web page has a corresponding Python class that encapsulates:
- **Page structure** (elements via LocatorProvider)
- **Page actions** (methods to interact with the page)
- **Page state** (properties to query page information)

### Page Objects
Page objects represent entire web pages and inherit from `BasePage`:
```python
from playwright.sync_api import Page

class BasePage:
    """Base page object providing common functionality for all pages."""

    def __init__(self, page: Page, base_url: str):
        """Initialize the Base Page."""
        self._page = page
        self.base_url = base_url
        self.url = ""

    @property
    def page(self) -> Page:
        """
        Get the underlying Playwright page object.

        Returns:
            Page: Playwright page object
        """
        return self._page

    def navigate_to_page(self) -> None:
        """
        Navigate to the page's URL.

        Args:
            path (str): The path to navigate to.
        """
        self.page.goto(f"{self.base_url}{self.url}")
```

```python
from playwright.sync_api import Page
from core.web.base_page import BasePage
from core.web.consts import PagesURL


class LoginPage(BasePage):
    """
    Page object for the Login Page.
    Provides methods to interact with the login form and related elements.
    """

    def __init__(self, page: Page, base_url: str):
        """Initialize the Login Page."""
        super().__init__(page, base_url)
        self.url = f"{base_url}{PagesURL.Login}"

    def login(self, username: str, password: str) -> None:
        """
        Perform login with the provided username and password.

        Args:
            username (str): The username to enter
            password (str): The password to enter
        """
        self.page.get_by_role("textbox", name="Username").fill(username)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Login").click()
```

### Locators:
Locators are the central piece of Playwright's auto-waiting and retry-ability. In a nutshell, locators represent a way to find element(s) on the page at any moment.

Quick Guide
These are the recommended built-in locators.

page.get_by_role() to locate by explicit and implicit accessibility attributes.
page.get_by_text() to locate by text content.
page.get_by_label() to locate a form control by associated label's text.
page.get_by_placeholder() to locate an input by placeholder.
page.get_by_alt_text() to locate an element, usually image, by its text alternative.
page.get_by_title() to locate an element by its title attribute.
page.get_by_test_id() to locate an element based on its data-testid attribute (other attributes can be configured).

### CSS and Xpath:
If you absolutely must use CSS or XPath locators, you can use page.locator() to create a locator that takes a selector describing how to find an element in the page. Playwright supports CSS and XPath selectors, and auto-detects them if you omit css= or xpath= prefix.
CSS and XPath are not recommended as the DOM can often change leading to non resilient tests. Instead, try to come up with a locator that is close to how the user perceives the page such as role locators or define an explicit testing contract using test ids.