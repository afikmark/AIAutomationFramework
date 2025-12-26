# Pet Store API - Authorization

## Overview

The Pet Store API supports two types of authorization mechanisms for different types of operations.

## 1. API Key Authorization (Header-based)

Used for accessing protected pet-related endpoints.

### Configuration

**Header Name:** `api_key`

**Test Value:** `special-key`

### Usage in Framework

```python
from core.controllers.pet_store_controller import PetStoreController

# API key is set during initialization
controller = PetStoreController(api_key="special-key")
```

The controller automatically includes the API key in request headers for operations that require it.

### Endpoints Requiring API Key

- All `/pet` endpoints (GET, POST, PUT, DELETE)
- Some `/store` endpoints

### Request Example

```python
# API key is automatically added to headers
headers = {"api_key": "special-key"}
```

## 2. User Login (Session-based Authentication)

Used for user account operations and session management.

### Login Endpoint

**Method:** `GET`

**URL:** `/user/login`

**Parameters:**
- `username` (query) - Username for login
- `password` (query) - Password in clear text

**Response:**
```json
{
  "code": 200,
  "type": "unknown",
  "message": "logged in user session:1234567890"
}
```

**Response Headers:**
- `X-Rate-Limit` - Calls per hour allowed by the user
- `X-Expires-After` - Date in UTC when token expires

### Logout Endpoint

**Method:** `GET`

**URL:** `/user/logout`

**Parameters:** None

**Response:**
```json
{
  "code": 200,
  "type": "unknown",
  "message": "ok"
}
```

## Authorization Patterns

### Pattern 1: API Key for Resource Operations

Use API key authentication for CRUD operations on resources (pets, orders).

## Security Notes

- The `special-key` is a test key for the demo API
- In production, use environment variables for API keys
- Never hardcode credentials in code
- Password is sent in clear text (not recommended for production)
- Use HTTPS in production environments
