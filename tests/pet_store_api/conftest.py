import pytest
from typing import Generator
from core.controllers.pet_store_controller import PetStoreController


@pytest.fixture(scope="function")
def pet_cleanup(
    pet_store_controller: PetStoreController,
) -> Generator[list[int], None, None]:
    """
    Fixture that tracks and cleans up created pets after tests.

    Usage:
        def test_example(pet_store_controller, pet_cleanup):
            pet_data = PetStoreAddPetRequest(id=12345, ...)
            response = pet_store_controller.add_pet(pet_data)
            pet_cleanup.append(response.id)  # Track for cleanup

    Yields:
        List to track pet IDs for cleanup
    """
    pet_ids: list[int] = []

    yield pet_ids

    # Cleanup: Delete all tracked pets
    for pet_id in pet_ids:
        try:
            pet_store_controller.delete_pet(pet_id)
            print(f"\n✓ Cleaned up pet with ID: {pet_id}")
        except Exception as e:
            # Pet might not exist or already deleted (404), ignore
            print(f"\n⚠ Could not delete pet {pet_id}: {str(e)}")
