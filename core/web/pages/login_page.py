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
        self.url = PagesURL.Login

    @property
    def error_message(self) -> str:
        """
        Get the error message text displayed on the login page.

        Returns:
            str: The error message text, or empty string if no error is visible
        """
        error_element = self.page.locator("[data-test='error']")
        return error_element.inner_text() if error_element.is_visible() else ""

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
