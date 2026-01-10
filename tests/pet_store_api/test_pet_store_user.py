from core.controllers.pet_store_controller import PetStoreController
from core.schemas.pet_store_login import PetStoreLoginRequest
from core.schemas.pet_store_user_creation import PetStoreUserCreateRequest
from plugins.reporter import reporter
import pytest


def test_user_creation(
    pet_store_controller: PetStoreController,
) -> None:
    """
    Test the user creation functionality of the PetStoreController.

    Args:
        pet_store_controller: The PetStoreController instance to use for the test.
    """
    user_data = PetStoreUserCreateRequest(
        id=12345,
        username="testuser",
        firstName="Test",
        lastName="User",
        email="testuser@example.com",
        password="password123",
        phone="123-456-7890",
        userStatus=1,
    )

    response = pet_store_controller.create_user(user_data)
    reporter.assert_that(response.code).is_equal_to(200)
    reporter.assert_that(response.type).is_equal_to("unknown")
    reporter.assert_that(response.message).is_equal_to("12345")


def test_user_login(
    pet_store_controller: PetStoreController,
) -> None:
    """
    Test the user login functionality of the PetStoreController.

    Args:
        pet_store_controller: The PetStoreController instance to use for the test.
    """
    login_data = PetStoreLoginRequest(
        username="testuser",
        password="password123",
    )

    response = pet_store_controller.login(login_data)
    reporter.assert_that(response.code).is_equal_to(200)
    reporter.assert_that(response.type).is_equal_to("unknown")
    reporter.assert_that(response.message).contains("logged in user session:")
