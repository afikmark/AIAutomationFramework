# Pet Store API - User Endpoints

## Overview

User endpoints handle user account management, including creation, retrieval, updates, deletion, and authentication.

**Base Path:** `/user`

**Authentication:** Username/password for login operations

## Endpoints

### 1. Create User

**Method:** `POST`

**URL:** `/user`

**Request Body:**
```json
{
  "id": 12345,
  "username": "testuser",
  "firstName": "Test",
  "lastName": "User",
  "email": "testuser@example.com",
  "password": "password123",
  "phone": "123-456-7890",
  "userStatus": 1
}
```

**Response:** `200 OK`
```json
{
  "code": 200,
  "type": "unknown",
  "message": "12345"
}
```

**userStatus Values:**
- `1` - Active user
- `0` - Inactive user

### 2. Create List of Users with Array

**Method:** `POST`

**URL:** `/user/createWithArray`

**Request Body:** Array of user objects
```json
[
  {
    "id": 1,
    "username": "user1",
    "firstName": "First1",
    "lastName": "Last1",
    "email": "user1@example.com",
    "password": "pass1",
    "phone": "111-111-1111",
    "userStatus": 1
  },
  {
    "id": 2,
    "username": "user2",
    "firstName": "First2",
    "lastName": "Last2",
    "email": "user2@example.com",
    "password": "pass2",
    "phone": "222-222-2222",
    "userStatus": 1
  }
]
```

**Response:** `200 OK`

### 3. Create List of Users with List

**Method:** `POST`

**URL:** `/user/createWithList`

**Request Body:** Array of user objects (same format as createWithArray)

**Response:** `200 OK`
```json
{
  "code": 200,
  "type": "unknown",
  "message": "ok"
}
```

### 4. User Login

**Method:** `GET`

**URL:** `/user/login`

**Query Parameters:**
- `username` (required) - The username for login
- `password` (required) - The password for login in clear text

**Response:** `200 OK`
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

**Error Responses:**
- `400` - Invalid username/password supplied

### 5. User Logout

**Method:** `GET`

**URL:** `/user/logout`

**Response:** `200 OK`
```json
{
  "code": 200,
  "type": "unknown",
  "message": "ok"
}
```

### 6. Get User by Username

**Method:** `GET`

**URL:** `/user/{username}`

**Path Parameters:**
- `username` (required) - The username to retrieve

**Response:** `200 OK` - User object
```json
{
  "id": 12345,
  "username": "testuser",
  "firstName": "Test",
  "lastName": "User",
  "email": "testuser@example.com",
  "password": "password123",
  "phone": "123-456-7890",
  "userStatus": 1
}
```

**Error Responses:**
- `400` - Invalid username supplied
- `404` - User not found

### 7. Update User

**Method:** `PUT`

**URL:** `/user/{username}`

**Path Parameters:**
- `username` (required) - Username to update

**Request Body:**
```json
{
  "id": 12345,
  "username": "testuser",
  "firstName": "Updated",
  "lastName": "Name",
  "email": "newemail@example.com",
  "password": "newpassword",
  "phone": "999-999-9999",
  "userStatus": 1
}
```

**Response:** `200 OK`

**Error Responses:**
- `400` - Invalid user supplied
- `404` - User not found

### 8. Delete User

**Method:** `DELETE`

**URL:** `/user/{username}`

**Path Parameters:**
- `username` (required) - The username to delete

**Response:** `200 OK`

**Error Responses:**
- `400` - Invalid username supplied
- `404` - User not found

## User Model

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

**Fields:**
- `id` - User ID (can be provided or auto-generated)
- `username` - Unique username
- `firstName` - User's first name
- `lastName` - User's last name
- `email` - User's email address
- `password` - User's password (sent in clear text)
- `phone` - User's phone number
- `userStatus` - User account status (0=inactive, 1=active)

## Notes

- User passwords are sent in clear text (not recommended for production)
- The API does not validate email format or password strength
- User IDs can be provided or auto-generated
- Session tokens from login are managed in the controller's session object
- The `message` field in create response contains the user ID as a string
