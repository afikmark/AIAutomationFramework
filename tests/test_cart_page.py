import pytest


def test_cart_page_loads_after_adding_items(sauce_ui):
    """Test that cart page loads successfully after adding items.

    Verifies that user can navigate to cart page and see added items.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Navigate to login page
        2) Login with valid credentials
        3) Add items to cart from inventory
        4) Navigate to cart page
        5) Verify cart page title displays "Your Cart"
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    # Navigate to cart by clicking the cart button
    sauce_ui.page.locator(".shopping_cart_link").click()

    assert (
        sauce_ui.cart_page.page_title == "Your Cart"
    ), "Expected cart page title to be 'Your Cart'"


def test_cart_displays_added_items(sauce_ui):
    """Test that cart displays all added items.

    Verifies that items added to cart are visible on the cart page.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory
        2) Add multiple items to cart
        3) Navigate to cart page
        4) Verify all items are displayed
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    sauce_ui.page.locator(".shopping_cart_link").click()

    assert sauce_ui.cart_page.cart_items_count == 3, "Expected 3 items in cart"

    item_names = sauce_ui.cart_page.get_cart_item_names()
    assert "Sauce Labs Backpack" in item_names, "Backpack should be in cart"
    assert "Sauce Labs Bike Light" in item_names, "Bike Light should be in cart"
    assert "Sauce Labs Bolt T-Shirt" in item_names, "Bolt T-Shirt should be in cart"


def test_cart_displays_correct_prices(sauce_ui):
    """Test that cart displays correct product prices.

    Verifies that item prices are shown correctly in the cart.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory
        2) Add items to cart
        3) Navigate to cart page
        4) Verify prices are displayed correctly
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    sauce_ui.page.locator(".shopping_cart_link").click()

    prices = sauce_ui.cart_page.get_cart_item_prices()
    assert len(prices) == 2, "Should have 2 prices"
    assert prices[0] == 29.99, "Backpack price should be $29.99"
    assert prices[1] == 9.99, "Bike Light price should be $9.99"


def test_cart_calculate_total(sauce_ui):
    """Test that cart total calculation is correct.

    Verifies that the sum of item prices is calculated correctly.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory
        2) Add items to cart
        3) Navigate to cart page
        4) Calculate and verify total
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    sauce_ui.page.locator(".shopping_cart_link").click()

    total = sauce_ui.cart_page.calculate_total()
    # Backpack: $29.99, Bike Light: $9.99, Bolt T-Shirt: $15.99
    expected_total = 29.99 + 9.99 + 15.99
    assert (
        abs(total - expected_total) < 0.01
    ), f"Expected total ~${expected_total}, got ${total}"


def test_remove_item_from_cart(sauce_ui):
    """Test that removing an item from cart reduces item count.

    Verifies that clicking remove button removes the item from cart.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory
        2) Add multiple items to cart
        3) Navigate to cart page
        4) Remove one item
        5) Verify item is removed and count is correct
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    sauce_ui.page.locator(".shopping_cart_link").click()

    assert sauce_ui.cart_page.cart_items_count == 2, "Should start with 2 items"

    sauce_ui.cart_page.remove_item_by_name("Sauce Labs Backpack")

    assert sauce_ui.cart_page.cart_items_count == 1, "Should have 1 item after removal"
    item_names = sauce_ui.cart_page.get_cart_item_names()
    assert "Sauce Labs Backpack" not in item_names, "Backpack should be removed"


def test_empty_cart_shows_empty_state(sauce_ui):
    """Test that empty cart is detected correctly.

    Verifies that is_empty() returns True for an empty cart.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Navigate to cart page without adding items
        2) Verify cart is empty
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.page.locator(".shopping_cart_link").click()

    assert sauce_ui.cart_page.is_empty(), "Cart should be empty initially"


def test_cart_continue_shopping_navigates_to_inventory(sauce_ui):
    """Test that 'Continue Shopping' button navigates back to inventory.

    Verifies that clicking continue shopping returns to inventory page.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory
        2) Add item to cart
        3) Navigate to cart page
        4) Click 'Continue Shopping'
        5) Verify navigation to inventory page
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")

    sauce_ui.page.locator(".shopping_cart_link").click()

    sauce_ui.cart_page.click_continue_shopping()

    assert sauce_ui.page.url.endswith(
        "/inventory.html"
    ), "Should navigate back to inventory page"


def test_cart_checkout_navigates_to_checkout_step_one(sauce_ui):
    """Test that 'Checkout' button navigates to checkout step one.

    Verifies that clicking checkout proceeds to checkout page.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory
        2) Add item to cart
        3) Navigate to cart page
        4) Click 'Checkout'
        5) Verify navigation to checkout step one page
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")

    sauce_ui.page.locator(".shopping_cart_link").click()

    sauce_ui.cart_page.click_checkout()

    assert sauce_ui.page.url.endswith(
        "/checkout-step-one.html"
    ), "Should navigate to checkout step one"


def test_remove_all_items_from_cart_clears_cart(sauce_ui):
    """Test that removing all items results in empty cart.

    Verifies that cart is empty after removing all items.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory
        2) Add multiple items to cart
        3) Navigate to cart page
        4) Remove all items
        5) Verify cart is empty
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    sauce_ui.page.locator(".shopping_cart_link").click()

    sauce_ui.cart_page.remove_item_by_name("Sauce Labs Backpack")
    sauce_ui.cart_page.remove_item_by_name("Sauce Labs Bike Light")
    sauce_ui.cart_page.remove_item_by_name("Sauce Labs Bolt T-Shirt")

    assert (
        sauce_ui.cart_page.is_empty()
    ), "Cart should be empty after removing all items"


def test_cart_item_count_matches_added_items(sauce_ui):
    """Test that cart item count matches the number of added items.

    Verifies that the cart accurately tracks the number of items.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory
        2) Add various number of items
        3) Navigate to cart page
        4) Verify count matches expected number
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    # Add 4 items
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Fleece Jacket")

    sauce_ui.page.locator(".shopping_cart_link").click()

    assert sauce_ui.cart_page.cart_items_count == 4, "Cart should contain 4 items"


@pytest.mark.parametrize(
    "product_name,expected_price",
    [
        ("Sauce Labs Backpack", 29.99),
        ("Sauce Labs Bike Light", 9.99),
        ("Sauce Labs Bolt T-Shirt", 15.99),
        ("Sauce Labs Fleece Jacket", 49.99),
    ],
)
def test_cart_item_prices_are_correct(sauce_ui, product_name, expected_price):
    """Test that individual item prices are correct in cart.

    Verifies that each product shows the correct price.

    Args:
        sauce_ui: Fixture providing page objects
        product_name: Name of product to test
        expected_price: Expected price of product

    Steps:
        1) Login and navigate to inventory
        2) Add specific item to cart
        3) Navigate to cart page
        4) Verify item price matches expected price
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart(product_name)

    sauce_ui.page.locator(".shopping_cart_link").click()

    prices = sauce_ui.cart_page.get_cart_item_prices()
    assert len(prices) == 1, "Should have 1 item"
    assert (
        abs(prices[0] - expected_price) < 0.01
    ), f"Expected {product_name} price to be ${expected_price}, got ${prices[0]}"


def test_cart_item_quantities_default_to_one(sauce_ui):
    """Test that added items have quantity of 1.

    Verifies that items added to cart have default quantity of 1.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory
        2) Add items to cart
        3) Navigate to cart page
        4) Verify quantities are 1
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    sauce_ui.page.locator(".shopping_cart_link").click()

    quantities = sauce_ui.cart_page.get_cart_item_quantities()
    assert quantities == [1, 1], "All items should have quantity of 1"


def test_is_item_in_cart_returns_true_for_existing_item(sauce_ui):
    """Test that is_item_in_cart() returns True for items in cart.

    Verifies the is_item_in_cart method works correctly.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory
        2) Add item to cart
        3) Navigate to cart page
        4) Verify is_item_in_cart returns True
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")

    sauce_ui.page.locator(".shopping_cart_link").click()

    assert sauce_ui.cart_page.is_item_in_cart(
        "Sauce Labs Backpack"
    ), "Should find Backpack in cart"


def test_multiple_add_and_remove_operations(sauce_ui):
    """Test cart with multiple sequential add and remove operations.

    Verifies that cart correctly handles multiple operations.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Login and navigate to inventory
        2) Add items, navigate to cart, remove items
        3) Add more items and verify
        4) Verify final state is correct
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("standard_user", "secret_sauce")

    # Add initial items
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    sauce_ui.page.locator(".shopping_cart_link").click()
    assert sauce_ui.cart_page.cart_items_count == 2

    # Remove one item
    sauce_ui.cart_page.remove_item_by_name("Sauce Labs Backpack")
    assert sauce_ui.cart_page.cart_items_count == 1

    # Go back and add more items
    sauce_ui.cart_page.click_continue_shopping()
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")
    sauce_ui.inventory_page.add_item_to_cart("Sauce Labs Fleece Jacket")

    sauce_ui.page.locator(".shopping_cart_link").click()
    assert sauce_ui.cart_page.cart_items_count == 3, "Should have 3 items total"
