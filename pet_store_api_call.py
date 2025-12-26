"""
Pet Store API Call Examples
============================
This module demonstrates various API operations with the Swagger Petstore API.
Base URL: https://petstore.swagger.io/v2
API Key for testing: special-key
"""

import requests
import json
from typing import Dict, Any, Optional


class PetStoreAPI:
    """Client for interacting with the Pet Store API"""

    BASE_URL = "https://petstore.swagger.io/v2"

    def __init__(self, api_key: str = "special-key"):
        """
        Initialize the Pet Store API client

        Args:
            api_key: API key for authorization (default: special-key)
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    # ========== 1. AUTHORIZATION REQUEST ==========

    def test_api_key_authorization(self) -> Dict[str, Any]:
        """
        Test API Key Authorization

        The Petstore API uses API key authorization for most endpoints.
        The API key 'special-key' is passed in the request headers as 'api_key'.
        This is different from user login (username/password).

        Returns:
            Response showing if API key authorization works
        """
        print(f"\n{'='*60}")
        print("1a. AUTHORIZATION - API Key Test")
        print(f"{'='*60}")
        print(f"API Key: {self.api_key}")
        print(f"Authorization Method: Header-based (api_key: {self.api_key})")

        # Test API key by accessing a protected endpoint
        url = f"{self.BASE_URL}/pet/findByStatus"
        params = {"status": "available"}
        headers = {"api_key": self.api_key}

        print(f"\nTesting API key authorization on protected endpoint:")
        print(f"Endpoint: GET {url}")
        print(f"Headers: {headers}")
        print(f"Params: {params}")

        response = self.session.get(url, params=params, headers=headers)

        print(f"\nStatus Code: {response.status_code}")
        if response.status_code == 200:
            print(f"✓ API Key Authorization Successful!")
            pets = response.json()
            print(f"✓ Retrieved {len(pets)} pets (authorization confirmed)")
        else:
            print(f"✗ Authorization Failed: {response.text}")

        return {
            "status_code": response.status_code,
            "authorized": response.status_code == 200,
            "api_key_used": self.api_key,
        }

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Logs user into the system (User Login Authentication example)

        Note: This is different from API key authorization.
        - API Key: Used via headers (api_key: special-key)
        - Login: Used via username/password for session-based auth

        Args:
            username: Username for login
            password: Password for login

        Returns:
            Response with login status and session token
        """
        print(f"\n{'='*60}")
        print("1b. AUTHORIZATION - User Login (Username/Password)")
        print(f"{'='*60}")

        url = f"{self.BASE_URL}/user/login"
        params = {"username": username, "password": password}

        print(f"Endpoint: GET {url}")
        print(f"Params: {params}")
        print(f"Authorization Method: Query parameters (username + password)")

        response = self.session.get(url, params=params)

        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")

        return {
            "status_code": response.status_code,
            "response": response.text,
            "headers": dict(response.headers),
        }

    def logout(self) -> Dict[str, Any]:
        """
        Logs out current logged in user session

        Returns:
            Response with logout status
        """
        url = f"{self.BASE_URL}/user/logout"

        print(f"\nLogging out...")
        print(f"Endpoint: GET {url}")

        response = self.session.get(url)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        return {"status_code": response.status_code, "response": response.text}

    # ========== 2. GET REQUEST ==========

    def get_pet_by_id(self, pet_id: int) -> Dict[str, Any]:
        """
        Find pet by ID (GET request example)

        Args:
            pet_id: ID of pet to return

        Returns:
            Pet details
        """
        print(f"\n{'='*60}")
        print("2. GET REQUEST - Find Pet by ID")
        print(f"{'='*60}")

        url = f"{self.BASE_URL}/pet/{pet_id}"
        headers = {"api_key": self.api_key}

        print(f"Endpoint: GET {url}")
        print(f"Headers: {headers}")

        response = self.session.get(url, headers=headers)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            pet_data = response.json()
            print(f"Pet Found:")
            print(json.dumps(pet_data, indent=2))
            return {"status_code": response.status_code, "data": pet_data}
        else:
            print(f"Error: {response.text}")
            return {"status_code": response.status_code, "error": response.text}

    def get_pets_by_status(self, status: str = "available") -> Dict[str, Any]:
        """
        Find pets by status (GET request with query parameters)

        Args:
            status: Status value (available, pending, sold)

        Returns:
            List of pets with the given status
        """
        print(f"\n{'='*60}")
        print("2. GET REQUEST - Find Pets by Status")
        print(f"{'='*60}")

        url = f"{self.BASE_URL}/pet/findByStatus"
        params = {"status": status}
        headers = {"api_key": self.api_key}

        print(f"Endpoint: GET {url}")
        print(f"Params: {params}")
        print(f"Headers: {headers}")

        response = self.session.get(url, params=params, headers=headers)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            pets = response.json()
            print(f"Found {len(pets)} pets with status '{status}'")
            if pets:
                print(f"First pet example:")
                print(json.dumps(pets[0], indent=2))
            return {
                "status_code": response.status_code,
                "data": pets,
                "count": len(pets),
            }
        else:
            print(f"Error: {response.text}")
            return {"status_code": response.status_code, "error": response.text}

    # ========== 3. POST REQUEST ==========

    def create_pet(
        self,
        name: str,
        status: str = "available",
        category: Optional[Dict] = None,
        photo_urls: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Add a new pet to the store (POST request example)

        Args:
            name: Pet name
            status: Pet status (available, pending, sold)
            category: Category object with id and name
            photo_urls: List of photo URLs

        Returns:
            Created pet details
        """
        print(f"\n{'='*60}")
        print("3. POST REQUEST - Add New Pet")
        print(f"{'='*60}")

        url = f"{self.BASE_URL}/pet"
        headers = {"api_key": self.api_key}

        pet_data = {
            "name": name,
            "status": status,
            "category": category or {"id": 1, "name": "Dogs"},
            "photoUrls": photo_urls or ["https://example.com/photo.jpg"],
            "tags": [{"id": 1, "name": "friendly"}],
        }

        print(f"Endpoint: POST {url}")
        print(f"Headers: {headers}")
        print(f"Request Body:")
        print(json.dumps(pet_data, indent=2))

        response = self.session.post(url, json=pet_data, headers=headers)

        print(f"\nStatus Code: {response.status_code}")

        if response.status_code in [200, 201]:
            created_pet = response.json()
            print(f"Pet Created Successfully:")
            print(json.dumps(created_pet, indent=2))
            return {"status_code": response.status_code, "data": created_pet}
        else:
            print(f"Error: {response.text}")
            return {"status_code": response.status_code, "error": response.text}

    def create_user(
        self, username: str, email: str, first_name: str, last_name: str
    ) -> Dict[str, Any]:
        """
        Create user (Another POST request example)

        Args:
            username: Username
            email: User email
            first_name: First name
            last_name: Last name

        Returns:
            Created user details
        """
        url = f"{self.BASE_URL}/user"

        user_data = {
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": "password123",
            "phone": "1234567890",
            "userStatus": 1,
        }

        print(f"\n--- Creating User ---")
        print(f"Endpoint: POST {url}")
        print(f"Request Body:")
        print(json.dumps(user_data, indent=2))

        response = self.session.post(url, json=user_data)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        return {"status_code": response.status_code, "response": response.text}

    # ========== 4. PUT REQUEST ==========

    def update_pet(
        self,
        pet_id: int,
        name: str,
        status: str,
        category: Optional[Dict] = None,
        photo_urls: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing pet (PUT request example)

        Args:
            pet_id: ID of pet to update
            name: Updated pet name
            status: Updated pet status
            category: Updated category object
            photo_urls: Updated photo URLs

        Returns:
            Updated pet details
        """
        print(f"\n{'='*60}")
        print("4. PUT REQUEST - Update Existing Pet")
        print(f"{'='*60}")

        url = f"{self.BASE_URL}/pet"
        headers = {"api_key": self.api_key}

        pet_data = {
            "id": pet_id,
            "name": name,
            "status": status,
            "category": category or {"id": 1, "name": "Dogs"},
            "photoUrls": photo_urls or ["https://example.com/updated_photo.jpg"],
            "tags": [{"id": 1, "name": "friendly"}, {"id": 2, "name": "trained"}],
        }

        print(f"Endpoint: PUT {url}")
        print(f"Headers: {headers}")
        print(f"Request Body:")
        print(json.dumps(pet_data, indent=2))

        response = self.session.put(url, json=pet_data, headers=headers)

        print(f"\nStatus Code: {response.status_code}")

        if response.status_code == 200:
            updated_pet = response.json()
            print(f"Pet Updated Successfully:")
            print(json.dumps(updated_pet, indent=2))
            return {"status_code": response.status_code, "data": updated_pet}
        else:
            print(f"Error: {response.text}")
            return {"status_code": response.status_code, "error": response.text}

    def update_user(
        self, username: str, email: str, first_name: str, last_name: str
    ) -> Dict[str, Any]:
        """
        Update user (Another PUT request example)

        Args:
            username: Username to update
            email: Updated email
            first_name: Updated first name
            last_name: Updated last name

        Returns:
            Update status
        """
        url = f"{self.BASE_URL}/user/{username}"

        user_data = {
            "username": username,
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "password": "newpassword456",
            "phone": "9876543210",
            "userStatus": 1,
        }

        print(f"\n--- Updating User ---")
        print(f"Endpoint: PUT {url}")
        print(f"Request Body:")
        print(json.dumps(user_data, indent=2))

        response = self.session.put(url, json=user_data)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        return {"status_code": response.status_code, "response": response.text}

    # ========== 5. DELETE REQUEST ==========

    def delete_pet(self, pet_id: int) -> Dict[str, Any]:
        """
        Deletes a pet (DELETE request example)

        Args:
            pet_id: Pet id to delete

        Returns:
            Deletion status
        """
        print(f"\n{'='*60}")
        print("5. DELETE REQUEST - Delete Pet")
        print(f"{'='*60}")

        url = f"{self.BASE_URL}/pet/{pet_id}"
        headers = {"api_key": self.api_key}

        print(f"Endpoint: DELETE {url}")
        print(f"Headers: {headers}")

        response = self.session.delete(url, headers=headers)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print(f"Pet Deleted Successfully")
            print(f"Response: {response.text}")
            return {"status_code": response.status_code, "response": response.text}
        else:
            print(f"Error: {response.text}")
            return {"status_code": response.status_code, "error": response.text}

    def delete_user(self, username: str) -> Dict[str, Any]:
        """
        Delete user (Another DELETE request example)

        Args:
            username: Username to delete

        Returns:
            Deletion status
        """
        url = f"{self.BASE_URL}/user/{username}"

        print(f"\n--- Deleting User ---")
        print(f"Endpoint: DELETE {url}")

        response = self.session.delete(url)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        return {"status_code": response.status_code, "response": response.text}


# ========== EXAMPLE USAGE ==========


def main():
    """
    Demonstrates all API operations:
    1. Authorization (Login)
    2. GET (Find pet by ID and by status)
    3. POST (Create new pet and user)
    4. PUT (Update pet and user)
    5. DELETE (Delete pet and user)
    """

    print("\n" + "=" * 60)
    print("PET STORE API EXAMPLES")
    print("=" * 60)

    # Initialize API client
    api = PetStoreAPI(api_key="special-key")

    try:
        # 1. AUTHORIZATION - API Key and Login
        print("\n\n" + "█" * 60)
        print("STEP 1: AUTHORIZATION (Two Methods)")
        print("█" * 60)

        # Test API key authorization
        api_key_result = api.test_api_key_authorization()

        # Test user login authorization
        login_result = api.login(username="testuser", password="testpass")

        # 2. GET REQUEST - Find existing pet
        print("\n\n" + "█" * 60)
        print("STEP 2: GET REQUEST")
        print("█" * 60)
        get_result = api.get_pet_by_id(pet_id=1)

        # Also demonstrate GET with query parameters
        get_status_result = api.get_pets_by_status(status="available")

        # 3. POST REQUEST - Create new pet
        print("\n\n" + "█" * 60)
        print("STEP 3: POST REQUEST")
        print("█" * 60)
        create_result = api.create_pet(
            name="Buddy",
            status="available",
            category={"id": 1, "name": "Dogs"},
            photo_urls=["https://example.com/buddy.jpg"],
        )

        # Store the created pet ID for later operations
        if create_result.get("status_code") in [200, 201]:
            created_pet_id = create_result["data"]["id"]
            print(f"\n✓ Pet created with ID: {created_pet_id}")

            # 4. PUT REQUEST - Update the pet we just created
            print("\n\n" + "█" * 60)
            print("STEP 4: PUT REQUEST")
            print("█" * 60)
            update_result = api.update_pet(
                pet_id=created_pet_id,
                name="Buddy Updated",
                status="sold",
                category={"id": 1, "name": "Dogs"},
                photo_urls=["https://example.com/buddy_new.jpg"],
            )

            # 5. DELETE REQUEST - Delete the pet
            print("\n\n" + "█" * 60)
            print("STEP 5: DELETE REQUEST")
            print("█" * 60)
            delete_result = api.delete_pet(pet_id=created_pet_id)

            # Verify deletion
            print("\n--- Verifying Deletion ---")
            verify_result = api.get_pet_by_id(pet_id=created_pet_id)
            if verify_result.get("status_code") == 404:
                print("✓ Pet successfully deleted (404 Not Found)")

        # Additional examples with User endpoints
        print("\n\n" + "█" * 60)
        print("BONUS: USER CRUD OPERATIONS")
        print("█" * 60)

        # Create user
        api.create_user(
            username="johndoe",
            email="john@example.com",
            first_name="John",
            last_name="Doe",
        )

        # Update user
        api.update_user(
            username="johndoe",
            email="john.updated@example.com",
            first_name="John",
            last_name="Doe-Updated",
        )

        # Delete user
        api.delete_user(username="johndoe")

        # Logout
        print("\n\n" + "█" * 60)
        print("LOGOUT")
        print("█" * 60)
        api.logout()

        print("\n\n" + "=" * 60)
        print("ALL API OPERATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
