from playwright.sync_api import Page


class BasePage:
    """Base page object providing common functionality for all pages."""

    def __init__(self, page: Page, base_url: str):
        """Initialize the Base Page."""
        self._page: Page = page
        self.base_url: str = base_url
        self.url: str = ""

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

    def goto(self) -> None:
        """Navigate to the page's URL (alias for navigate_to_page)."""
        self.navigate_to_page()
