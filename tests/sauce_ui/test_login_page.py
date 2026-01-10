import pytest
from core.web.consts import Timeouts
from plugins.reporter import reporter
from core.web.pages.sauce_demo import SauceDemo

TEST_SUITE_NAME: str = "SauceDemo Login Page Tests"


@pytest.mark.sanity
@pytest.mark.test_case_key("DEV-67")
@pytest.mark.parametrize(
    "username,password",
    [
        ("standard_user", "secret_sauce"),
        ("problem_user", "secret_sauce"),
    ],
)
def test_login_with_valid_credentials(sauce_ui: SauceDemo, username, password):
    """Test successful login with valid credentials.

    Verifies that user can log in and is redirected to inventory page.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Navigate to login page
        2) Enter valid credentials
        3) Click login
        4) Verify redirect to inventory

    """

    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login(username, password)
    reporter.assert_that(sauce_ui.page.url).ends_with("/inventory.html")


@pytest.mark.test_case_key("DEV-65")
def test_login_with_performance_glitch_user(sauce_ui: SauceDemo):
    """Test successful login with performance glitch user.

    Verifies that user can log in despite performance delays.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Navigate to login page
        2) Enter performance glitch credentials
        3) Click login
        4) Wait for redirect to inventory
    """
    sauce_ui.login_page.navigate_to_page()
    sauce_ui.login_page.login("performance_glitch_user", "secret_sauce")
    sauce_ui.page.wait_for_url(
        "**/inventory.html", timeout=Timeouts.PERFORMANCE_GLITCH_TIMEOUT
    )
    reporter.assert_that(sauce_ui.page.url).ends_with("/inventory.html")


@pytest.mark.test_case_key("DEV-68")
@pytest.mark.parametrize(
    "username,password,expected_error",
    [
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out."),
        (
            "invalid_user",
            "secret_sauce",
            "Username and password do not match any user in this service",
        ),
        (
            "standard_user",
            "wrong_password",
            "Username and password do not match any user in this service",
        ),
    ],
)
def test_login_with_invalid_credentials(
    sauce_ui: SauceDemo, username, password, expected_error
):
    """Test failed login with invalid credentials.

    Verifies that login fails and appropriate error message is shown.

    Args:
        sauce_ui: Fixture providing page objects

    Steps:
        1) Navigate to login page
        2) Enter invalid credentials
        3) Click login
        4) Verify error message appears
        5) Verify no redirect
    """
    sauce_ui.login_page.navigate_to_page()
    initial_url = sauce_ui.page.url
    sauce_ui.login_page.login(username, password)
    reporter.assert_that(sauce_ui.login_page.error_message).contains(expected_error)
    reporter.assert_that(sauce_ui.page.url).is_equal_to(initial_url)
