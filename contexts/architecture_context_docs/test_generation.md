# Test Generation Guidelines (Concise)

## UI Test Guidelines

### Pre-Test Generation Checklist

Before writing tests:
1. ☐ Page object class exists
2. ☐ All required methods implemented
3. ☐ Properties for state queries defined
4. ☐ No locators exposed to test layer

Then write tests using page object API only.

### Fundamentals

- Function-based tests only (no classes).
- One scenario per test, minimal steps.

### 1) Function Naming (abstract)

```python
def test_action_under_condition(sauce_ui):
    ...
```

### 2) Docstring (abstract)

```python
"""
What is verified, how it's exercised, expected outcome.
Args: sauce_ui – fixture providing page objects
Steps: 1) navigate 2) act 3) assert
"""
```

### 3) Fixture Usage

- Use `sauce_ui` from `tests/conftest.py`.
- Access page objects via `sauce_ui.<page>.<method_or_property>`.

### 4) Assertion with Message (abstract)

```python
assert condition, "descriptive failure message"
```

### 5) Parametrization (abstract)

```python
import pytest

@pytest.mark.parametrize("input_value, expected", [
    (..., ...),
    (..., ...),
])
def test_scenario(sauce_ui, input_value, expected):
    ...
    assert result == expected, "message"
```

### 6) `sauce_ui` Fixture Usage

- Primary entry to page objects and their APIs.
- Do not import page classes; call existing methods/properties via `sauce_ui`.
- Every page object has a 'goto' method, use it when needed.

### WHEN

- Parametrization: use when a single flow repeats with different arguments.
- Imports: only when needed (e.g., `pytest` for parametrization/marks).

### DONT

- Don't create multiple test functions for the same flow (use parametrization).
- Don't import pages or methods; use the `sauce_ui` fixture to access them.
- Don't add imports when not needed.
- Don't call methods/properties that do not exist.
- Don't use try/except in tests.
- Don't use page locators directly; page objects provide the required APIs.
- Don't create comments, keep the test clean and readable.

BAD❌:
```python
    # Try to access inventory page directly without logging in
    sauce_ui.page.goto(f"{sauce_ui.base_url}/inventory.html")
```
GOOD✅:
```python
    sauce_ui.page.goto(f"{sauce_ui.base_url}/inventory.html")
```

---

## API Test Guidelines

### Pre-Test Generation Checklist

Before writing API tests:
1. ☐ Controller class exists with required methods
2. ☐ Request schema (Pydantic model) defined
3. ☐ Response schema (Pydantic model) defined with `from_response()` method
4. ☐ Controller methods use type hints and return typed responses

### Fundamentals

- Function-based tests only (no classes).
- One API scenario per test, minimal steps.
- Use Pydantic schemas for request/response validation.
- Controller handles all HTTP logic.

### 1) Function Naming

```python
def test_api_operation_scenario(controller_fixture):
    ...
```

**Examples:**
- `test_user_creation(pet_store_controller)`
- `test_user_login(pet_store_controller)`
- `test_invalid_credentials(pet_store_controller)`

### 2) Docstring

```python
"""
Brief description of what API operation is tested and expected outcome.
Args: controller_fixture – fixture providing controller instance
"""
```

### 3) Fixture Usage

- Use controller fixture from `tests/conftest.py`.
- Controller provides typed methods for API operations.
- Access controller methods directly: `controller.create_user(data)`

### 4) Request Schema Usage

Always use Pydantic request models for API calls:

```python
from core.schemas.pet_store_user_creation import PetStoreUserCreateRequest

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
```

### 5) Response Validation

Response is automatically validated by Pydantic schemas:

```python
response = pet_store_controller.create_user(user_data)
assert response.code == 200, "User creation failed"
assert response.message == "12345", "Unexpected response message"
```

### 6) Parametrization for API Tests

```python
import pytest

@pytest.mark.parametrize("user_status,expected", [
    (1, "unknown"),
    (0, "unknown"),
])
def test_user_status_values(pet_store_controller, user_status, expected):
    """Test creating users with different status values"""
    user_data = PetStoreUserCreateRequest(
        id=10000 + user_status,
        username=f"user_{user_status}",
        firstName="Test",
        lastName="User",
        email=f"user{user_status}@example.com",
        password="pass",
        phone="123-456-7890",
        userStatus=user_status,
    )
    
    response = pet_store_controller.create_user(user_data)
    assert response.code == 200, f"Failed to create user with status {user_status}"
```

### 7) Error Testing

```python
def test_get_nonexistent_resource(pet_store_controller):
    """Test retrieving a non-existent resource returns 404"""
    with pytest.raises(Exception) as exc_info:
        pet_store_controller.get_pet_by_id(999999)
    
    assert "404" in str(exc_info.value), "Expected 404 error"
```

### 8) Workflow Testing

```python
def test_user_registration_and_login_workflow(pet_store_controller):
    """Test complete user registration and login workflow"""
    user_data = PetStoreUserCreateRequest(
        id=99999,
        username="newuser",
        firstName="New",
        lastName="User",
        email="newuser@example.com",
        password="securepass123",
        phone="555-555-5555",
        userStatus=1,
    )
    
    create_response = pet_store_controller.create_user(user_data)
    assert create_response.code == 200, "User registration failed"
    
    login_data = PetStoreLoginRequest(username="newuser", password="securepass123")
    login_response = pet_store_controller.login(login_data)
    assert login_response.code == 200, "Login failed"
```

### WHEN (API Tests)

- Use parametrization for testing multiple input values/scenarios
- Import schemas when creating request objects
- Import pytest when using parametrization or pytest features
- Test complete workflows when operations depend on each other

### DONT (API Tests)

- Don't make raw HTTP requests; use controller methods
- Don't manually parse JSON; use Pydantic schemas
- Don't use `response.json()` directly; controller returns typed objects
- Don't create request dicts; use Pydantic request models
- Don't ignore response validation; assert on response properties
- Don't use try/except for error testing; use `pytest.raises()`
- Don't test multiple unrelated operations in one test
- Don't create comments; keep tests clean and readable

### Schema Pattern

All response schemas should implement `from_response()`:

```python
from pydantic import BaseModel, Field
from requests import Response

class PetStoreUserCreateResponse(BaseModel):
    code: int = Field(..., description="Response code")
    type: str = Field(..., description="Response type")
    message: str = Field(..., description="Response message")
    
    @classmethod
    def from_response(cls, response: Response) -> "PetStoreUserCreateResponse":
        """Create response model from requests.Response object"""
        return cls.model_validate_json(response.text)
```

### Controller Pattern

Controller methods should use Pydantic models for type safety:

```python
def create_user(self, user_data: PetStoreUserCreateRequest) -> PetStoreUserCreateResponse:
    """Create a new user in the Pet Store API"""
    url = f"{self.BASE_URL}/user"
    response = self.session.post(url, data=user_data.model_dump_json())
    response.raise_for_status()
    return PetStoreUserCreateResponse.from_response(response)
```

### Complete Test Example

```python
def test_user_creation(pet_store_controller):
    """Test the user creation functionality of the PetStoreController"""
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
```

BAD❌:
```python
response = requests.post(url, json={"username": "test"})
data = response.json()
assert data["code"] == 200
```

GOOD✅:
```python
user_data = PetStoreUserCreateRequest(username="test", ...)
response = pet_store_controller.create_user(user_data)
assert response.code == 200, "User creation failed"
```
