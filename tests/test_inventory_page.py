import pytest


def test_inventory_page_loads_after_login(sauce_ui):
    """Test that inventory page loads successfully after login.

    Verifies that user is redirected to inventory page after successful login
    and the page displays the correct title.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Navigate to login page
        2) Login with valid credentials
        3) Verify redirect to inventory page
        4) Verify page title
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    assert sauce_ui.page.url.endswith(
        "/inventory.html"
    ), "Expected redirect to inventory page after login"
    assert (
        sauce_ui.inventory_page.page_title == "Products"
    ), "Expected page title to be 'Products'"


def test_add_item_to_cart_updates_badge(sauce_ui):
    """Test that adding item to cart updates the cart badge count.

    Verifies that clicking 'Add to cart' increments the cart badge counter.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory page
        2) Verify cart badge is initially empty
        3) Add item to cart
        4) Verify cart badge shows count of 1
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    assert (
        sauce_ui.inventory_page.cart_badge_count == "0"
    ), "Cart should be empty initially"

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")

    assert (
        sauce_ui.inventory_page.cart_badge_count == "1"
    ), "Cart badge should show 1 after adding item"


def test_add_multiple_items_updates_badge_count(sauce_ui):
    """Test that adding multiple items updates the badge count correctly.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory page
        2) Add multiple items to cart
        3) Verify cart badge shows correct count
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    assert (
        sauce_ui.inventory_page.cart_badge_count == "3"
    ), "Cart badge should show 3 after adding three items"


def test_remove_item_from_cart_decrements_badge(sauce_ui):
    """Test that removing item from cart decrements the badge count.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory page
        2) Add two items to cart
        3) Remove one item
        4) Verify cart badge shows correct count
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    assert sauce_ui.inventory_page.cart_badge_count == "2", "Cart should have 2 items"

    sauce_ui.inventory_page.remove_item_from_cart("Sauce Labs Backpack")

    assert (
        sauce_ui.inventory_page.cart_badge_count == "1"
    ), "Cart badge should show 1 after removing one item"


def test_add_to_cart_button_changes_to_remove(sauce_ui):
    """Test that 'Add to cart' button changes to 'Remove' after adding item.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory page
        2) Verify item not in cart
        3) Add item to cart
        4) Verify item is in cart (button shows 'Remove')
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    assert not sauce_ui.inventory_page.is_product_in_cart(
        "Sauce Labs Backpack"
    ), "Product should not be in cart initially"

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")

    assert sauce_ui.inventory_page.is_product_in_cart(
        "Sauce Labs Backpack"
    ), "Product should be in cart after adding"


@pytest.mark.parametrize(
    "sort_option,expected_first,expected_last",
    [
        ("az", "Sauce Labs Backpack", "Test.allTheThings() T-Shirt (Red)"),
        ("za", "Test.allTheThings() T-Shirt (Red)", "Sauce Labs Backpack"),
    ],
)
def test_sort_products_by_name(sauce_ui, sort_option, expected_first, expected_last):
    """Test sorting products alphabetically.

    Args:
        sauce_ui: Fixture providing page objects
        sort_option: Sort option to apply
        expected_first: Expected first product name
        expected_last: Expected last product name

    Steps:
        1) Login and navigate to inventory page
        2) Sort products
        3) Verify first and last product names
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.sort_products(sort_option)
    product_names = sauce_ui.inventory_page.get_product_names()

    assert (
        product_names[0] == expected_first
    ), f"First product should be {expected_first}"
    assert product_names[-1] == expected_last, f"Last product should be {expected_last}"


def test_sort_products_by_price_low_to_high(sauce_ui):
    """Test sorting products by price from low to high.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory page
        2) Sort by price (low to high)
        3) Verify prices are in ascending order
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.sort_products("lohi")
    prices = sauce_ui.inventory_page.get_product_prices()

    assert prices == sorted(prices), "Prices should be sorted in ascending order"
    assert prices[0] == 7.99, "Cheapest item should be $7.99 (Onesie)"


def test_sort_products_by_price_high_to_low(sauce_ui):
    """Test sorting products by price from high to low.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory page
        2) Sort by price (high to low)
        3) Verify prices are in descending order
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.sort_products("hilo")
    prices = sauce_ui.inventory_page.get_product_prices()

    assert prices == sorted(
        prices, reverse=True
    ), "Prices should be sorted in descending order"
    assert prices[0] == 49.99, "Most expensive item should be $49.99 (Fleece Jacket)"


def test_all_products_displayed(sauce_ui):
    """Test that all 6 products are displayed on inventory page.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory page
        2) Verify count of displayed products
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    product_names = sauce_ui.inventory_page.get_product_names()

    assert len(product_names) == 6, "Inventory page should display 6 products"
