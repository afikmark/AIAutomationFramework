from playwright.sync_api import Page
from .login_page import LoginPage
from .inventory_page import InventoryPage


class SauceDemo:
    def __init__(self, page: Page):
        self._checkout_multi_page = None
        self.page = page
        self.base_url = "https://www.saucedemo.com/v1"
        self._login_page = None
        self._inventory_page = None
        self._cart_page = None
        self._checkout_page = None

    @property
    def login_page(self) -> LoginPage:
        """
        Lazy initialization of LoginPage to ensure it's only created
        after the browser has navigated to the actual page.
        """
        if self._login_page is None:
            self._login_page = LoginPage(self.page, self.base_url)
        return self._login_page

    @property
    def inventory_page(self) -> InventoryPage:
        """
        Lazy initialization of InventoryPage.
        """
        if self._inventory_page is None:
            self._inventory_page = InventoryPage(self.page, self.base_url)
        return self._inventory_page
