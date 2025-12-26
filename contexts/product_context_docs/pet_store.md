# Pet Store REST API

## Overview

The Pet Store API is a sample RESTful API that demonstrates CRUD operations for managing pets, store orders, and users. It follows OpenAPI 2.0 specification.

**Base URL:** `https://petstore.swagger.io/v2`

**Swagger Documentation:** https://petstore.swagger.io/

## Authentication

The API supports two authentication methods:

1. **API Key Authentication (Header-based)**
   - Header: `api_key: special-key`
   - Used for: Pet operations (GET, POST, PUT, DELETE)
   - Test key: `special-key`

2. **User Login (Session-based)**
   - Endpoint: `GET /user/login`
   - Parameters: username, password
   - Returns session token in response headers

## API Categories

The API is organized into three main resource categories:

### 1. Pet Operations
Manage pet records in the store
- **Endpoints:** `/pet`, `/pet/{petId}`, `/pet/findByStatus`, `/pet/findByTags`
- **Operations:** Create, Read, Update, Delete pets
- **Authentication:** API key required

### 2. Store Operations
Manage store orders and inventory
- **Endpoints:** `/store/order`, `/store/order/{orderId}`, `/store/inventory`
- **Operations:** Place orders, retrieve orders, check inventory
- **Authentication:** API key (for some operations)

### 3. User Operations
Manage user accounts and authentication
- **Endpoints:** `/user`, `/user/{username}`, `/user/login`, `/user/logout`
- **Operations:** Create, Read, Update, Delete users; Login/Logout
- **Authentication:** Username/password for login

## Request/Response Format

**Content-Type:** `application/json`

**Accept:** `application/json`

### Standard Response Structure

Most operations return a response with:
```json
{
  "code": 200,
  "type": "unknown",
  "message": "success"
}
```

### HTTP Status Codes

- `200` - Success
- `201` - Created (for POST operations)
- `400` - Invalid input
- `404` - Resource not found
- `405` - Method not allowed
- `500` - Server error

## Data Models

### Pet
```json
{
  "id": 0,
  "category": {
    "id": 0,
    "name": "string"
  },
  "name": "string",
  "photoUrls": ["string"],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available|pending|sold"
}
```

### User
```json
{
  "id": 0,
  "username": "string",
  "firstName": "string",
  "lastName": "string",
  "email": "string",
  "password": "string",
  "phone": "string",
  "userStatus": 0
}
```

### Order
```json
{
  "id": 0,
  "petId": 0,
  "quantity": 0,
  "shipDate": "2024-01-01T00:00:00.000Z",
  "status": "placed|approved|delivered",
  "complete": true
}
```

## Implementation in Framework

### Controller
`core/controllers/pet_store_controller.py` - Main API client class

### Schemas
`core/schemas/` - Pydantic models for request/response validation:
- `pet_store_login.py` - Login request/response models
- `pet_store_user_creation.py` - User creation request/response models

### Tests
`tests/test_pet_store_user.py` - API test examples

## Quick Start

```python
from core.controllers.pet_store_controller import PetStoreController
from core.schemas.pet_store_login import PetStoreLoginRequest

# Initialize controller
controller = PetStoreController(api_key="special-key")

# Login
login_request = PetStoreLoginRequest(username="testuser", password="password123")
response = controller.login(login_request)
```

## Related Documentation

- [Authorization Endpoints](pet_store_authorization.md)
- [Pet Endpoints](pet_store_pet.md)
- [Store Endpoints](pet_store_store.md)
- [User Endpoints](pet_store_user.md)
- [API Test Guidelines](../architecture_context_docs/test_generation.md)