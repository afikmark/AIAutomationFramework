from playwright.sync_api import Page
from core.web.base_page import BasePage
from core.web.consts import PagesURL


class CartPage(BasePage):
    """Page object for the Cart page.

    Represents the shopping cart page where users can review items,
    adjust quantities, remove items, and proceed to checkout.
    """

    def __init__(self, page: Page, base_url: str):
        """Initialize the Cart Page."""
        super().__init__(page, base_url)
        self.url = PagesURL.Cart

    @property
    def page_title(self) -> str:
        """Get the page title text.

        Returns:
            str: The page title "Your Cart" or empty string if not found
        """
        return self.page.get_by_text("Your Cart").text_content() or ""

    @property
    def cart_items_count(self) -> int:
        """Get the number of items currently in the cart.

        Returns:
            int: Count of cart item rows
        """
        items = self.page.locator(".cart_item").all()
        return len(items)

    def get_cart_item_names(self) -> list[str]:
        """Get list of all product names in the cart.

        Returns:
            list[str]: List of product names
        """
        return [
            name.text_content() or ""
            for name in self.page.locator(".inventory_item_name").all()
        ]

    def get_cart_item_prices(self) -> list[float]:
        """Get list of all product prices in the cart.

        Returns:
            list[float]: List of prices as floats
        """
        price_texts = [
            price.text_content() or "$0"
            for price in self.page.locator(".inventory_item_price").all()
        ]
        return [float(price.replace("$", "")) for price in price_texts]

    def get_cart_item_quantities(self) -> list[int]:
        """Get list of all product quantities in the cart.

        Returns:
            list[int]: List of quantities
        """
        quantities = []
        items = self.page.locator(".cart_item").all()
        for item in items:
            qty_text = item.locator(".cart_quantity").text_content() or "1"
            quantities.append(int(qty_text.strip()))
        return quantities

    def get_item_by_name(self, product_name: str):
        """Get a specific cart item by product name.

        Args:
            product_name: Name of the product to find

        Returns:
            Locator: The cart item row containing the product
        """
        return self.page.locator(f"text='{product_name}'").locator("..")

    def remove_item_by_name(self, product_name: str) -> None:
        """Remove an item from the cart by product name.

        Args:
            product_name: Name of the product to remove
        """
        # Convert product name to button ID format
        button_id = f"remove-{product_name.lower().replace(' ', '-')}"
        self.page.locator(f"#{button_id}").click()

    def is_item_in_cart(self, product_name: str) -> bool:
        """Check if a product exists in the cart.

        Args:
            product_name: Name of the product to check

        Returns:
            bool: True if product is in cart, False otherwise
        """
        try:
            self.page.get_by_text(product_name).is_visible()
            return True
        except Exception:
            return False

    def click_continue_shopping(self) -> None:
        """Click the 'Continue Shopping' button.

        Navigates back to the inventory page.
        """
        self.page.get_by_role("button", name="Continue Shopping").click()

    def click_checkout(self) -> None:
        """Click the 'Checkout' button.

        Proceeds to checkout step one.
        """
        self.page.get_by_role("button", name="Checkout").click()

    def calculate_total(self) -> float:
        """Calculate the total price of items in the cart.

        Returns:
            float: Sum of all item prices
        """
        prices = self.get_cart_item_prices()
        return sum(prices)

    def is_empty(self) -> bool:
        """Check if the cart is empty.

        Returns:
            bool: True if cart has no items, False otherwise
        """
        return self.cart_items_count == 0

    @property
    def cart_badge_count(self) -> str:
        """Get the cart badge count text.

        Returns:
            str: The cart badge count or empty string if no badge
        """
        try:
            badge = self.page.locator(".shopping_cart_badge")
            return badge.text_content() or ""
        except Exception:
            return ""

    def is_checkout_button_visible(self) -> bool:
        """Check if checkout button is visible.

        Returns:
            bool: True if checkout button is visible
        """
        return self.page.locator("#checkout").is_visible()

    def is_continue_shopping_button_visible(self) -> bool:
        """Check if continue shopping button is visible.

        Returns:
            bool: True if continue shopping button is visible
        """
        return self.page.locator("#continue-shopping").is_visible()

    def click_cart_icon(self) -> None:
        """Navigate to cart page by clicking the cart icon."""
        self.page.locator(".shopping_cart_link").click()

    def goto(self) -> None:
        """Navigate to cart page directly."""
        self.navigate_to_page()
