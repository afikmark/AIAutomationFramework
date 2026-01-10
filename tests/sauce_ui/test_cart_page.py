import pytest
from plugins.reporter import reporter

TEST_SUITE_NAME = "SauceDemo Cart Page Tests"


@pytest.mark.test_case_key("DEV-51")
def test_cart_page_loads_after_adding_items(logged_in_user):
    """Test that cart page loads successfully after adding items.

    Verifies that user can navigate to cart page and see added items.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Navigate to login page
        2) Login with valid credentials
        3) Add items to cart from inventory
        4) Navigate to cart page
        5) Verify cart page title displays "Your Cart"
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    logged_in_user.inventory_page.click_cart_icon()

    reporter.assert_that(logged_in_user.cart_page.page_title).is_equal_to("Your Cart")


@pytest.mark.test_case_key("DEV-54")
def test_cart_displays_added_items(logged_in_user):
    """Test that cart displays all added items.

    Verifies that items added to cart are visible on the cart page.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory
        2) Add multiple items to cart
        3) Navigate to cart page
        4) Verify all items are displayed
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    logged_in_user.inventory_page.click_cart_icon()

    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(3)

    item_names = logged_in_user.cart_page.get_cart_item_names()
    reporter.assert_that(item_names).contains("Sauce Labs Backpack")
    reporter.assert_that(item_names).contains("Sauce Labs Bike Light")
    reporter.assert_that(item_names).contains("Sauce Labs Bolt T-Shirt")


@pytest.mark.test_case_key("DEV-50")
def test_cart_displays_correct_prices(logged_in_user):
    """Test that cart displays correct product prices.

    Verifies that item prices are shown correctly in the cart.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory
        2) Add items to cart
        3) Navigate to cart page
        4) Verify prices are displayed correctly
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    logged_in_user.inventory_page.click_cart_icon()

    prices = logged_in_user.cart_page.get_cart_item_prices()
    reporter.assert_that(len(prices)).is_equal_to(2)
    reporter.assert_that(prices[0]).is_equal_to(29.99)
    reporter.assert_that(prices[1]).is_equal_to(9.99)


@pytest.mark.test_case_key("DEV-52")
def test_cart_calculate_total(logged_in_user):
    """Test that cart total calculation is correct.

    Verifies that the sum of item prices is calculated correctly.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory
        2) Add items to cart
        3) Navigate to cart page
        4) Calculate and verify total
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    logged_in_user.inventory_page.click_cart_icon()

    total = logged_in_user.cart_page.calculate_total()
    expected_total = 29.99 + 9.99 + 15.99
    reporter.assert_that(abs(total - expected_total)).is_less_than(0.01)


@pytest.mark.test_case_key("DEV-49")
def test_remove_item_from_cart(logged_in_user):
    """Test that removing an item from cart reduces item count.

    Verifies that clicking remove button removes the item from cart.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory
        2) Add multiple items to cart
        3) Navigate to cart page
        4) Remove one item
        5) Verify item is removed and count is correct
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    logged_in_user.inventory_page.click_cart_icon()

    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(2)

    logged_in_user.cart_page.remove_item_by_name("Sauce Labs Backpack")

    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(1)
    item_names = logged_in_user.cart_page.get_cart_item_names()
    reporter.assert_that(item_names).does_not_contain("Sauce Labs Backpack")


@pytest.mark.test_case_key("DEV-48")
def test_empty_cart_shows_empty_state(logged_in_user):
    """Test that empty cart is detected correctly.

    Verifies that is_empty() returns True for an empty cart.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Navigate to cart page without adding items
        2) Verify cart is empty
    """
    logged_in_user.inventory_page.click_cart_icon()

    reporter.assert_that(logged_in_user.cart_page.is_empty()).is_true()


@pytest.mark.test_case_key("DEV-53")
def test_cart_continue_shopping_navigates_to_inventory(logged_in_user):
    """Test that 'Continue Shopping' button navigates back to inventory.

    Verifies that clicking continue shopping returns to inventory page.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory
        2) Add item to cart
        3) Navigate to cart page
        4) Click 'Continue Shopping'
        5) Verify navigation to inventory page
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")

    logged_in_user.inventory_page.click_cart_icon()

    logged_in_user.cart_page.click_continue_shopping()

    reporter.assert_that(logged_in_user.page.url).ends_with("/inventory.html")


@pytest.mark.test_case_key("DEV-55")
def test_cart_checkout_navigates_to_checkout_step_one(logged_in_user):
    """Test that 'Checkout' button navigates to checkout step one.

    Verifies that clicking checkout proceeds to checkout page.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory
        2) Add item to cart
        3) Navigate to cart page
        4) Click 'Checkout'
        5) Verify navigation to checkout step one page
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")

    logged_in_user.inventory_page.click_cart_icon()

    logged_in_user.cart_page.click_checkout()

    reporter.assert_that(logged_in_user.page.url).ends_with("/checkout-step-one.html")


@pytest.mark.test_case_key("DEV-57")
def test_remove_all_items_from_cart_clears_cart(logged_in_user):
    """Test that removing all items results in empty cart.

    Verifies that cart is empty after removing all items.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory
        2) Add multiple items to cart
        3) Navigate to cart page
        4) Remove all items
        5) Verify cart is empty
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    logged_in_user.inventory_page.click_cart_icon()

    logged_in_user.cart_page.remove_item_by_name("Sauce Labs Backpack")
    logged_in_user.cart_page.remove_item_by_name("Sauce Labs Bike Light")
    logged_in_user.cart_page.remove_item_by_name("Sauce Labs Bolt T-Shirt")

    reporter.assert_that(logged_in_user.cart_page.is_empty()).is_true()


@pytest.mark.test_case_key("DEV-56")
def test_cart_item_count_matches_added_items(logged_in_user):
    """Test that cart item count matches the number of added items.

    Verifies that the cart accurately tracks the number of items.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory
        2) Add various number of items
        3) Navigate to cart page
        4) Verify count matches expected number
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Fleece Jacket")

    logged_in_user.inventory_page.click_cart_icon()

    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(4)


@pytest.mark.test_case_key("DEV-60")
@pytest.mark.parametrize(
    "product_name,expected_price",
    [
        ("Sauce Labs Backpack", 29.99),
        ("Sauce Labs Bike Light", 9.99),
        ("Sauce Labs Bolt T-Shirt", 15.99),
        ("Sauce Labs Fleece Jacket", 49.99),
    ],
)
def test_cart_item_prices_are_correct(logged_in_user, product_name, expected_price):
    """Test that individual item prices are correct in cart.

    Verifies that each product shows the correct price.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance
        product_name: Name of product to test
        expected_price: Expected price of product

    Steps:
        1) Login and navigate to inventory
        2) Add specific item to cart
        3) Navigate to cart page
        4) Verify item price matches expected price
    """
    logged_in_user.inventory_page.add_item_to_cart(product_name)

    logged_in_user.inventory_page.click_cart_icon()

    prices = logged_in_user.cart_page.get_cart_item_prices()
    reporter.assert_that(len(prices)).is_equal_to(1)
    reporter.assert_that(abs(prices[0] - expected_price)).is_less_than(0.01)


@pytest.mark.test_case_key("DEV-58")
def test_cart_item_quantities_default_to_one(logged_in_user):
    """Test that added items have quantity of 1.

    Verifies that items added to cart have default quantity of 1.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory
        2) Add items to cart
        3) Navigate to cart page
        4) Verify quantities are 1
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    logged_in_user.inventory_page.click_cart_icon()

    quantities = logged_in_user.cart_page.get_cart_item_quantities()
    reporter.assert_that(quantities).is_equal_to([1, 1])


@pytest.mark.test_case_key("DEV-59")
def test_is_item_in_cart_returns_true_for_existing_item(logged_in_user):
    """Test that is_item_in_cart() returns True for items in cart.

    Verifies the is_item_in_cart method works correctly.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory
        2) Add item to cart
        3) Navigate to cart page
        4) Verify is_item_in_cart returns True
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")

    logged_in_user.inventory_page.click_cart_icon()

    reporter.assert_that(
        logged_in_user.cart_page.is_item_in_cart("Sauce Labs Backpack")
    ).is_true()


@pytest.mark.test_case_key("DEV-61")
def test_multiple_add_and_remove_operations(logged_in_user):
    """Test cart with multiple sequential add and remove operations.

    Verifies that cart correctly handles multiple operations.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory
        2) Add items, navigate to cart, remove items
        3) Add more items and verify
        4) Verify final state is correct
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    logged_in_user.inventory_page.click_cart_icon()
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(2)

    logged_in_user.cart_page.remove_item_by_name("Sauce Labs Backpack")
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(1)

    logged_in_user.cart_page.click_continue_shopping()
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Fleece Jacket")

    logged_in_user.inventory_page.click_cart_icon()
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(3)


@pytest.mark.test_case_key("DEV-40")
def test_cart_items_display_correctly(logged_in_user):
    """Test that all cart items display correctly with required information.

    Based on: DEV-40 - Verify Cart Items Display Correctly

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login to SauceDemo
        2) Add 2-3 items to cart
        3) Navigate to cart page
        4) Verify cart page loads successfully
        5) Verify all items display with required elements
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    logged_in_user.inventory_page.click_cart_icon()

    reporter.assert_that(logged_in_user.cart_page.page_title).is_equal_to("Your Cart")
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(2)

    cart_items = logged_in_user.cart_page.get_cart_item_names()
    reporter.assert_that(cart_items).contains("Sauce Labs Backpack")
    reporter.assert_that(cart_items).contains("Sauce Labs Bike Light")

    prices = logged_in_user.cart_page.get_cart_item_prices()
    reporter.assert_that(len(prices)).is_equal_to(2)
    reporter.assert_that(all(price > 0 for price in prices)).is_true()


@pytest.mark.test_case_key("DEV-33")
def test_remove_single_item_from_cart(logged_in_user):
    """Test removing a single item from cart updates badge and cart correctly.

    Based on: DEV-33 - Verify Remove Single Item from Cart

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and add 3 items to cart
        2) Navigate to cart page
        3) Remove first item
        4) Verify item removed and cart badge updated
        5) Verify other items remain
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    logged_in_user.inventory_page.click_cart_icon()

    initial_count = logged_in_user.cart_page.cart_items_count
    reporter.assert_that(initial_count).is_equal_to(3)

    logged_in_user.cart_page.remove_item_by_name("Sauce Labs Backpack")

    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(2)
    reporter.assert_that(logged_in_user.cart_page.cart_badge_count).is_equal_to("2")

    remaining_items = logged_in_user.cart_page.get_cart_item_names()
    reporter.assert_that(remaining_items).does_not_contain("Sauce Labs Backpack")
    reporter.assert_that(remaining_items).contains("Sauce Labs Bike Light")
    reporter.assert_that(remaining_items).contains("Sauce Labs Bolt T-Shirt")


@pytest.mark.test_case_key("DEV-32")
def test_continue_shopping_navigation(logged_in_user):
    """Test Continue Shopping button navigates back and preserves cart contents.

    Based on: DEV-32 - Verify Continue Shopping Navigation

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and add items
        2) Navigate to cart
        3) Click Continue Shopping
        4) Verify navigation to inventory
        5) Verify cart badge persists
        6) Return to cart and verify items intact
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Fleece Jacket")

    logged_in_user.inventory_page.click_cart_icon()
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(2)

    logged_in_user.cart_page.click_continue_shopping()

    reporter.assert_that(logged_in_user.page.url).contains("/inventory.html")
    reporter.assert_that(logged_in_user.cart_page.cart_badge_count).is_equal_to("2")

    logged_in_user.cart_page.click_cart_icon()
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(2)

    cart_items = logged_in_user.cart_page.get_cart_item_names()
    reporter.assert_that(cart_items).contains("Sauce Labs Backpack")
    reporter.assert_that(cart_items).contains("Sauce Labs Fleece Jacket")


@pytest.mark.test_case_key("DEV-39")
def test_checkout_button_navigation(logged_in_user):
    """Test Checkout button navigates to checkout and preserves cart contents.

    Based on: DEV-39 - Verify Checkout Button Navigation

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and add items
        2) Navigate to cart
        3) Click Checkout button
        4) Verify navigation to checkout-step-one
        5) Verify cart badge persists
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Onesie")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")

    logged_in_user.inventory_page.click_cart_icon()
    reporter.assert_that(
        logged_in_user.cart_page.is_checkout_button_visible()
    ).is_true()

    logged_in_user.cart_page.click_checkout()

    reporter.assert_that(logged_in_user.page.url).contains("/checkout-step-one.html")
    reporter.assert_that(logged_in_user.cart_page.cart_badge_count).is_equal_to("2")


@pytest.mark.test_case_key("DEV-36")
def test_empty_cart_checkout_behavior(logged_in_user):
    """Test checkout button behavior when cart is empty.

    Based on: DEV-36 - Verify Empty Cart Checkout Behavior

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login
        2) Navigate to empty cart
        3) Verify cart is empty
        4) Check Continue Shopping button is functional
    """
    logged_in_user.inventory_page.click_cart_icon()

    reporter.assert_that(logged_in_user.cart_page.is_empty()).is_true()
    reporter.assert_that(logged_in_user.cart_page.cart_badge_count).is_equal_to("")
    reporter.assert_that(
        logged_in_user.cart_page.is_continue_shopping_button_visible()
    ).is_true()


@pytest.mark.test_case_key("DEV-41")
def test_cart_persistence_across_navigation(logged_in_user):
    """Test cart contents persist when navigating away and returning.

    Based on: DEV-41 - Verify Cart Persistence Across Navigation

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and add 3 items
        2) Navigate to cart
        3) Navigate away using Continue Shopping
        4) Navigate to product detail
        5) Return to cart
        6) Verify all items still present
        7) Refresh page and verify persistence
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    logged_in_user.inventory_page.click_cart_icon()
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(3)

    logged_in_user.cart_page.click_continue_shopping()

    logged_in_user.inventory_page.click_cart_icon()
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(3)

    logged_in_user.page.reload()
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(3)

    cart_items = logged_in_user.cart_page.get_cart_item_names()
    reporter.assert_that(cart_items).contains("Sauce Labs Backpack")
    reporter.assert_that(cart_items).contains("Sauce Labs Bike Light")
    reporter.assert_that(cart_items).contains("Sauce Labs Bolt T-Shirt")


@pytest.mark.test_case_key("DEV-38")
def test_hamburger_menu_navigation_from_cart(logged_in_user):
    """Test hamburger menu functions correctly from cart page.

    Based on: DEV-38 - Verify Hamburger Menu Navigation from Cart

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and add items
        2) Navigate to cart
        3) Open hamburger menu
        4) Click All Items option
        5) Verify navigation to inventory
        6) Return to cart and test Reset App State
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.click_cart_icon()

    logged_in_user.hamburger_menu.open_menu()
    logged_in_user.hamburger_menu.click_all_items()

    reporter.assert_that(logged_in_user.page.url).contains("/inventory.html")

    logged_in_user.inventory_page.click_cart_icon()

    logged_in_user.hamburger_menu.open_menu()
    logged_in_user.hamburger_menu.click_reset_app_state()
    logged_in_user.hamburger_menu.close_menu()

    logged_in_user.page.reload()
    logged_in_user.inventory_page.click_cart_icon()
    reporter.assert_that(logged_in_user.cart_page.is_empty()).is_true()


@pytest.mark.test_case_key("DEV-34")
def test_browser_back_button_handling(logged_in_user):
    """Test cart page handles browser back/forward buttons correctly.

    Based on: DEV-34 - Verify Browser Back Button Handling

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and add items to cart
        2) Navigate to cart
        3) Click Continue Shopping
        4) Use browser back button
        5) Verify return to cart with items intact
        6) Verify browser forward button works
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")

    logged_in_user.inventory_page.click_cart_icon()
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(2)

    logged_in_user.cart_page.click_continue_shopping()
    reporter.assert_that(logged_in_user.page.url).contains("/inventory.html")

    logged_in_user.page.go_back()
    reporter.assert_that(logged_in_user.page.url).contains("/cart.html")
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(2)

    logged_in_user.page.go_forward()
    reporter.assert_that(logged_in_user.page.url).contains("/inventory.html")

    logged_in_user.page.go_back()

    logged_in_user.cart_page.remove_item_by_name("Sauce Labs Backpack")
    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(1)

    logged_in_user.cart_page.click_continue_shopping()
    logged_in_user.page.go_back()

    reporter.assert_that(logged_in_user.cart_page.cart_items_count).is_equal_to(1)
