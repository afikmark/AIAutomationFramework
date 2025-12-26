from core.controllers.pet_store_controller import PetStoreController
from core.schemas.pet_store_pet import (
    PetStoreAddPetRequest,
    Category,
    Tag,
)


def test_add_new_pet(
    pet_store_controller: PetStoreController, pet_cleanup: list
) -> None:
    """
    Test adding a new pet to the store
    Args: pet_store_controller – fixture providing controller instance
    Steps: 1) create pet data 2) add pet via controller 3) assert response
    """
    pet_data = PetStoreAddPetRequest(
        id=12345,
        category=Category(id=1, name="Dogs"),
        name="Buddy",
        photoUrls=["https://example.com/photo.jpg"],
        tags=[Tag(id=1, name="friendly")],
        status="available",
    )

    response = pet_store_controller.add_pet(pet_data)
    pet_cleanup.append(response.id)

    assert response.id == 12345, "Pet ID mismatch"
    assert response.name == "Buddy", "Pet name mismatch"
    assert response.status == "available", "Pet status mismatch"
    assert response.category is not None, "Pet category is missing"
    assert response.category.name == "Dogs", "Pet category mismatch"


def test_get_pet_by_id(
    pet_store_controller: PetStoreController, pet_cleanup: list
) -> None:
    """
    Test retrieving a pet by ID
    Args: pet_store_controller – fixture providing controller instance
    Steps: 1) add a pet 2) retrieve it by ID 3) assert response matches
    """
    pet_data = PetStoreAddPetRequest(
        id=67890,
        category=Category(id=2, name="Cats"),
        name="Whiskers",
        photoUrls=["https://example.com/cat.jpg"],
        tags=[Tag(id=2, name="playful")],
        status="available",
    )

    add_response = pet_store_controller.add_pet(pet_data)
    pet_cleanup.append(add_response.id)

    assert add_response.id == 67890, "Pet creation failed"

    get_response = pet_store_controller.get_pet_by_id(67890)
    assert get_response.id == 67890, "Pet ID mismatch"
    assert get_response.name == "Whiskers", "Pet name mismatch"
    assert get_response.status == "available", "Pet status mismatch"
    assert get_response.category is not None, "Pet category is missing"
    assert get_response.category.name == "Cats", "Pet category mismatch"
