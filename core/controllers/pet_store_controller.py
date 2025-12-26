import requests
import os
from dotenv import load_dotenv
from core.schemas.pet_store_login import PetStoreLoginRequest, PetStoreLoginResponse
from core.schemas.pet_store_user_creation import (
    PetStoreUserCreateRequest,
    PetStoreUserCreateResponse,
)
from core.schemas.pet_store_pet import (
    PetStoreAddPetRequest,
    PetStoreAddPetResponse,
    PetStoreGetPetResponse,
)

load_dotenv()


class PetStoreController:
    BASE_URL = "https://petstore.swagger.io/v2"

    def __init__(self, api_key: str | None = None):
        """
        Initialize the Pet Store API client

        Args:
            api_key: API key for authorization (defaults to PET_STORE_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv("PET_STORE_API_KEY", "special-key")
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def login(self, login_data: PetStoreLoginRequest) -> PetStoreLoginResponse:
        """
        Log in to the Pet Store API

        Args:
            login_data: PetStoreLogin object containing username and password

        Returns:
            A dictionary containing the login response
        """
        url = f"{self.BASE_URL}/user/login"
        response = self.session.get(
            url,
            params={"username": login_data.username, "password": login_data.password},
        )
        response.raise_for_status()
        return PetStoreLoginResponse.from_response(response)

    def create_user_with_list(
        self, user_data: PetStoreUserCreateRequest
    ) -> PetStoreUserCreateResponse:
        """
        Create a new user in the Pet Store API

        Args:
            user_data: PetStoreUserCreateRequest object containing user details

        Returns:
            A dictionary containing the user creation response
        """
        url = f"{self.BASE_URL}/user/createWithList"
        response = self.session.post(url, data=user_data.model_dump_json())
        response.raise_for_status()
        return PetStoreUserCreateResponse.from_response(response)

    def create_user(
        self, user_data: PetStoreUserCreateRequest
    ) -> PetStoreUserCreateResponse:
        """
        Create a new user in the Pet Store API

        Args:
            user_data: PetStoreUserCreateRequest object containing user details

        Returns:
            A dictionary containing the user creation response
        """
        url = f"{self.BASE_URL}/user"
        response = self.session.post(url, data=user_data.model_dump_json())
        response.raise_for_status()
        return PetStoreUserCreateResponse.from_response(response)

    def add_pet(self, pet_data: PetStoreAddPetRequest) -> PetStoreAddPetResponse:
        """
        Add a new pet to the store

        Args:
            pet_data: PetStoreAddPetRequest object containing pet details

        Returns:
            PetStoreAddPetResponse containing the created pet with ID
        """
        url = f"{self.BASE_URL}/pet"
        headers = {"api_key": self.api_key}
        response = self.session.post(
            url, data=pet_data.model_dump_json(), headers=headers
        )
        response.raise_for_status()
        return PetStoreAddPetResponse.from_response(response)

    def get_pet_by_id(self, pet_id: int) -> PetStoreGetPetResponse:
        """
        Find pet by ID

        Args:
            pet_id: ID of pet to return

        Returns:
            PetStoreGetPetResponse containing the pet details
        """
        url = f"{self.BASE_URL}/pet/{pet_id}"
        headers = {"api_key": self.api_key}
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return PetStoreGetPetResponse.from_response(response)

    def delete_pet(self, pet_id: int) -> dict:
        """
        Delete a pet from the store

        Args:
            pet_id: ID of pet to delete

        Returns:
            Dictionary with deletion response
        """
        url = f"{self.BASE_URL}/pet/{pet_id}"
        headers = {"api_key": self.api_key}
        response = self.session.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
