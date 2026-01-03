import pytest


def test_inventory_page_loads_after_login(logged_in_user):
    """Test that inventory page loads successfully after login.

    Verifies that user is redirected to inventory page after successful login
    and the page displays the correct title.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Navigate to login page
        2) Login with valid credentials
        3) Verify redirect to inventory page
        4) Verify page title
    """
    assert logged_in_user.page.url.endswith(
        "/inventory.html"
    ), "Expected redirect to inventory page after login"
    assert (
        logged_in_user.inventory_page.page_title == "Products"
    ), "Expected page title to be 'Products'"


def test_add_item_to_cart_updates_badge(logged_in_user):
    """Test that adding item to cart updates the cart badge count.

    Verifies that clicking 'Add to cart' increments the cart badge counter.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory page
        2) Verify cart badge is initially empty
        3) Add item to cart
        4) Verify cart badge shows count of 1
    """
    assert (
        logged_in_user.inventory_page.cart_badge_count == "0"
    ), "Cart should be empty initially"

    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")

    assert (
        logged_in_user.inventory_page.cart_badge_count == "1"
    ), "Cart badge should show 1 after adding item"


def test_add_multiple_items_updates_badge_count(logged_in_user):
    """Test that adding multiple items updates the badge count correctly.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory page
        2) Add multiple items to cart
        3) Verify cart badge shows correct count
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    assert (
        logged_in_user.inventory_page.cart_badge_count == "3"
    ), "Cart badge should show 3 after adding three items"


def test_remove_item_from_cart_decrements_badge(logged_in_user):
    """Test that removing item from cart decrements the badge count.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory page
        2) Add two items to cart
        3) Remove one item
        4) Verify cart badge shows correct count
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    assert (
        logged_in_user.inventory_page.cart_badge_count == "2"
    ), "Cart should have 2 items"

    logged_in_user.inventory_page.remove_item_from_cart("Sauce Labs Backpack")

    assert (
        logged_in_user.inventory_page.cart_badge_count == "1"
    ), "Cart badge should show 1 after removing one item"


def test_add_to_cart_button_changes_to_remove(logged_in_user):
    """Test that 'Add to cart' button changes to 'Remove' after adding item.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory page
        2) Verify item not in cart
        3) Add item to cart
        4) Verify item is in cart (button shows 'Remove')
    """
    assert not logged_in_user.inventory_page.is_product_in_cart(
        "Sauce Labs Backpack"
    ), "Product should not be in cart initially"

    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")

    assert logged_in_user.inventory_page.is_product_in_cart(
        "Sauce Labs Backpack"
    ), "Product should be in cart after adding"


@pytest.mark.parametrize(
    "sort_option,expected_first,expected_last",
    [
        ("az", "Sauce Labs Backpack", "Test.allTheThings() T-Shirt (Red)"),
        ("za", "Test.allTheThings() T-Shirt (Red)", "Sauce Labs Backpack"),
    ],
)
def test_sort_products_by_name(
    logged_in_user, sort_option, expected_first, expected_last
):
    """Test sorting products alphabetically.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance
        sort_option: Sort option to apply
        expected_first: Expected first product name
        expected_last: Expected last product name

    Steps:
        1) Login and navigate to inventory page
        2) Sort products
        3) Verify first and last product names
    """
    logged_in_user.inventory_page.sort_products(sort_option)
    product_names = logged_in_user.inventory_page.get_product_names()

    assert (
        product_names[0] == expected_first
    ), f"First product should be {expected_first}"
    assert product_names[-1] == expected_last, f"Last product should be {expected_last}"


def test_all_products_displayed(logged_in_user):
    """Test that all 6 products are displayed on inventory page.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory page
        2) Verify count of displayed products
    """
    product_names = logged_in_user.inventory_page.get_product_names()

    assert len(product_names) == 6, "Inventory page should display 6 products"


def test_cart_state_persists_after_sorting(logged_in_user):
    """Test that cart items persist when sorting products.

    Verifies that items added to cart remain in cart after sorting.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory page
        2) Add items to cart
        3) Sort products
        4) Verify cart badge still shows correct count
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    initial_count = logged_in_user.inventory_page.cart_badge_count

    logged_in_user.inventory_page.sort_products("hilo")

    assert (
        logged_in_user.inventory_page.cart_badge_count == initial_count
    ), "Cart count should persist after sorting"


def test_remove_all_items_from_cart(logged_in_user):
    """Test that removing all items from cart clears the badge.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory page
        2) Add multiple items to cart
        3) Remove all items
        4) Verify cart badge is empty or shows 0
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    logged_in_user.inventory_page.remove_item_from_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.remove_item_from_cart("Sauce Labs Bike Light")
    logged_in_user.inventory_page.remove_item_from_cart("Sauce Labs Bolt T-Shirt")

    assert (
        logged_in_user.inventory_page.cart_badge_count == "0"
    ), "Cart badge should be empty after removing all items"


@pytest.mark.parametrize(
    "sort_option,expected_first,expected_last",
    [
        ("lohi", "Sauce Labs Onesie", "Sauce Labs Fleece Jacket"),
        ("hilo", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie"),
    ],
)
def test_sort_products_by_price(
    logged_in_user, sort_option, expected_first, expected_last
):
    """Test sorting products by price with verification of first and last items.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance
        sort_option: Sort option to apply ("lohi" or "hilo")
        expected_first: Expected first product name
        expected_last: Expected last product name

    Steps:
        1) Login and navigate to inventory page
        2) Sort products by price
        3) Verify first and last product names match expected values
    """
    logged_in_user.inventory_page.sort_products(sort_option)
    product_names = logged_in_user.inventory_page.get_product_names()

    assert (
        product_names[0] == expected_first
    ), f"First product should be {expected_first}, got {product_names[0]}"
    assert (
        product_names[-1] == expected_last
    ), f"Last product should be {expected_last}, got {product_names[-1]}"


def test_cart_badge_increments_correctly_with_individual_items(logged_in_user):
    """Test that adding multiple different items increments cart badge correctly.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory page
        2) Add different items one by one
        3) Verify cart badge increments after each addition
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    assert logged_in_user.inventory_page.cart_badge_count == "1"

    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    assert logged_in_user.inventory_page.cart_badge_count == "2"

    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")
    assert logged_in_user.inventory_page.cart_badge_count == "3"


def test_mixed_sorting_and_removal_maintains_correct_cart_count(logged_in_user):
    """Test that cart state is maintained correctly when adding items, sorting, and removing.

    Args:
        logged_in_user: Fixture providing logged-in SauceDemo instance

    Steps:
        1) Login and navigate to inventory page
        2) Add multiple items to cart
        3) Sort products by price
        4) Remove one item
        5) Verify cart count is correct and item is no longer marked as in cart
    """
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Backpack")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bike Light")
    logged_in_user.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")

    logged_in_user.inventory_page.sort_products("lohi")

    assert (
        logged_in_user.inventory_page.cart_badge_count == "3"
    ), "Cart should still have 3 items after sorting"

    logged_in_user.inventory_page.remove_item_from_cart("Sauce Labs Backpack")

    assert (
        logged_in_user.inventory_page.cart_badge_count == "2"
    ), "Cart should have 2 items after removing one"
    assert not logged_in_user.inventory_page.is_product_in_cart(
        "Sauce Labs Backpack"
    ), "Removed item should no longer be marked as in cart"
