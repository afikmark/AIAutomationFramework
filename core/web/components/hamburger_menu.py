from playwright.sync_api import Page


class HamburgerMenu:
    """
    Component object for the Hamburger Menu.
    Provides methods to interact with the hamburger menu and its items.
    """

    OPEN_MENU_BUTTON: str = "OpenMenuButton"
    ALL_ITEMS_LINK: str = "AllItemsLink"
    ABOUT_LINK: str = "AboutLink"
    LOGOUT_LINK: str = "LogoutLink"
    RESET_APP_STATE_LINK: str = "ResetAppStateLink"
    CLOSE_MENU_BUTTON: str = "CloseMenuButton"

    def __init__(self, page: Page):
        """Initialize the Hamburger Menu component."""
        self._page = page

    @property
    def page(self):
        """Get the underlying Playwright page object."""
        return self._page

    def open_menu(self) -> None:
        """Open the hamburger menu."""
        self.page.get_by_role("button", name="Open Menu").click()

    def close_menu(self) -> None:
        """Close the hamburger menu."""
        self.page.get_by_role("button", name="Close Menu").click()

    def click_logout(self) -> None:
        """Click the logout link in the hamburger menu."""
        self.page.get_by_role("link", name="Logout").click()

    def click_all_items(self) -> None:
        """Click the all items link in the hamburger menu."""
        self.page.get_by_role("link", name="All Items").click()

    def click_about(self) -> None:
        """Click the about link in the hamburger menu."""
        self.page.get_by_role("link", name="About").click()

    def click_reset_app_state(self) -> None:
        """Click the reset app state link in the hamburger menu."""
        self.page.get_by_role("link", name="Reset App State").click()
