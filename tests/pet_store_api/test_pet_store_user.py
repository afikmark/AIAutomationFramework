from core.controllers.pet_store_controller import PetStoreController
from core.schemas.pet_store_login import PetStoreLoginRequest, PetStoreLoginResponse
from core.schemas.pet_store_user_creation import (
    PetStoreUserCreateRequest,
    PetStoreUserCreateResponse,
)


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
    assert response.code == 200, "User creation failed"
    assert response.type == "unknown", "Unexpected response type"
    assert response.message == "12345", "Unexpected response message"


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
    assert response.code == 200, "Login failed"
    assert response.type == "unknown", "Unexpected response type"
    assert "logged in user session:" in response.message, "Unexpected response message"
