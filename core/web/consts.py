class Pages:
    Login: str = "LoginPage"
    Inventory: str = "InventoryPage"
    Cart: str = "CartPage"
    Checkout: str = "CheckoutPage"


class ComponentNames:
    HamburgerMenu: str = "HamburgerMenuComponent"


class PagesURL:
    Login: str = "/"
    Inventory: str = "/inventory.html"
    Cart: str = "/cart.html"
    CheckoutStepOne: str = "/checkout-step-one.html"
    CheckoutStepTwo: str = "/checkout-step-two.html"
    CheckoutComplete: str = "/checkout-complete.html"


class Timeouts:
    """Timeout constants for various operations."""

    PERFORMANCE_GLITCH_TIMEOUT: int = 10000  # milliseconds
    DEFAULT_TIMEOUT: int = 30000  # milliseconds
