from playwright.sync_api import Page
from .login_page import LoginPage
from .inventory_page import InventoryPage
from .cart_page import CartPage
from ..components.hamburger_menu import HamburgerMenu


class SauceDemo:
    def __init__(self, page: Page, base_url: str = "https://www.saucedemo.com"):
        self._checkout_multi_page = None
        self.page: Page = page
        self.base_url = base_url
        self._login_page: LoginPage | None = None
        self._inventory_page: InventoryPage | None = None
        self._cart_page: CartPage | None = None
        self._hamburger_menu: HamburgerMenu | None = None

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

    @property
    def cart_page(self) -> CartPage:
        """
        Lazy initialization of CartPage.
        """
        if self._cart_page is None:
            self._cart_page = CartPage(self.page, self.base_url)
        return self._cart_page

    @property
    def hamburger_menu(self) -> HamburgerMenu:
        """
        Lazy initialization of HamburgerMenu.
        """
        if self._hamburger_menu is None:
            self._hamburger_menu = HamburgerMenu(self.page)
        return self._hamburger_menu
