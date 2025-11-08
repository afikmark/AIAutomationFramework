from playwright.sync_api import Page
from core.web.base_page import BasePage
from core.web.consts import PagesURL


class InventoryPage(BasePage):
    """Page object for the Inventory/Products page."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.path = PagesURL.Inventory

    @property
    def page_title(self) -> str:
        """Get the page title text."""
        return self.page.get_by_text("Products").text_content() or ""

    @property
    def cart_badge_count(self) -> str:
        """Get the cart badge count."""
        badge = self.page.locator(".shopping_cart_badge")
        return (badge.text_content() or "0") if badge.is_visible() else "0"

    @property
    def sort_dropdown_value(self) -> str:
        """Get the current sort dropdown value."""
        return self.page.locator(".product_sort_container").input_value()

    def add_item_to_cart(self, product_name: str) -> None:
        """
        Add an item to cart by product name.

        Args:
            product_name: Name of the product to add
        """
        # Convert product name to button ID format
        button_id = f"add-to-cart-{product_name.lower().replace(' ', '-')}"
        self.page.locator(f"#{button_id}").click()

    def remove_item_from_cart(self, product_name: str) -> None:
        """
        Remove an item from cart by product name.

        Args:
            product_name: Name of the product to remove
        """
        # Convert product name to button ID format
        button_id = f"remove-{product_name.lower().replace(' ', '-')}"
        self.page.locator(f"#{button_id}").click()

    def sort_products(self, sort_option: str) -> None:
        """
        Sort products using the dropdown.

        Args:
            sort_option: Sort option - "az", "za", "lohi", "hilo"
        """
        sort_map = {
            "az": "Name (A to Z)",
            "za": "Name (Z to A)",
            "lohi": "Price (low to high)",
            "hilo": "Price (high to low)",
        }
        self.page.locator(".product_sort_container").select_option(
            sort_map[sort_option]
        )

    def get_product_names(self) -> list[str]:
        """Get list of all product names in current order."""
        return [
            name.text_content() or ""
            for name in self.page.locator(".inventory_item_name").all()
        ]

    def get_product_prices(self) -> list[float]:
        """Get list of all product prices in current order."""
        price_texts = [
            price.text_content() or "$0"
            for price in self.page.locator(".inventory_item_price").all()
        ]
        return [float(price.replace("$", "")) for price in price_texts]

    def is_product_in_cart(self, product_name: str) -> bool:
        """
        Check if a product has been added to cart (button shows 'Remove').

        Args:
            product_name: Name of the product to check

        Returns:
            True if product is in cart, False otherwise
        """
        button_id = f"remove-{product_name.lower().replace(' ', '-')}"
        return self.page.locator(f"#{button_id}").is_visible()
