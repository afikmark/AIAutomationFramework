# Pet Store API - Pet Endpoints

## Overview

Pet endpoints allow management of pet records in the store, including creating, reading, updating, and deleting pet information.

**Base Path:** `/pet`

**Authentication:** API key required (Header: `api_key: special-key`)

## Endpoints

### 1. Add a New Pet

**Method:** `POST`

**URL:** `/pet`

**Request Body:**
```json
{
  "id": 0,
  "category": {
    "id": 1,
    "name": "Dogs"
  },
  "name": "Buddy",
  "photoUrls": ["https://example.com/photo.jpg"],
  "tags": [
    {
      "id": 1,
      "name": "friendly"
    }
  ],
  "status": "available"
}
```

**Response:** `200 OK` - Returns the created pet object with ID

**Status Values:**
- `available` - Pet is available for purchase
- `pending` - Pet is reserved
- `sold` - Pet has been sold

### 2. Update an Existing Pet

**Method:** `PUT`

**URL:** `/pet`

**Request Body:**
```json
{
  "id": 123,
  "name": "Buddy Updated",
  "status": "sold",
  "category": {
    "id": 1,
    "name": "Dogs"
  },
  "photoUrls": ["https://example.com/photo_updated.jpg"],
  "tags": [
    {
      "id": 1,
      "name": "friendly"
    },
    {
      "id": 2,
      "name": "trained"
    }
  ]
}
```

**Response:** `200 OK` - Returns the updated pet object

**Error Responses:**
- `400` - Invalid ID supplied
- `404` - Pet not found
- `405` - Validation exception

### 3. Find Pets by Status

**Method:** `GET`

**URL:** `/pet/findByStatus`

**Query Parameters:**
- `status` (required) - Status values: `available`, `pending`, `sold`
- Multiple status values can be provided: `?status=available&status=pending`

**Response:** `200 OK` - Array of pet objects

**Example:**
```json
[
  {
    "id": 1,
    "name": "Buddy",
    "status": "available",
    "category": {"id": 1, "name": "Dogs"},
    "photoUrls": ["https://example.com/photo.jpg"],
    "tags": [{"id": 1, "name": "friendly"}]
  },
  {
    "id": 2,
    "name": "Max",
    "status": "available",
    "category": {"id": 1, "name": "Dogs"},
    "photoUrls": ["https://example.com/photo2.jpg"],
    "tags": [{"id": 2, "name": "playful"}]
  }
]
```

### 4. Find Pets by Tags

**Method:** `GET`

**URL:** `/pet/findByTags`

**Query Parameters:**
- `tags` (required) - Tags to filter by
- Multiple tags can be provided: `?tags=friendly&tags=trained`

**Response:** `200 OK` - Array of pet objects

**Note:** This endpoint is deprecated. Use `/pet/findByStatus` instead.

### 5. Find Pet by ID

**Method:** `GET`

**URL:** `/pet/{petId}`

**Path Parameters:**
- `petId` (required) - ID of pet to return

**Response:** `200 OK` - Pet object

**Error Responses:**
- `400` - Invalid ID supplied
- `404` - Pet not found

### 6. Update Pet with Form Data

**Method:** `POST`

**URL:** `/pet/{petId}`

**Path Parameters:**
- `petId` (required) - ID of pet to update

**Form Data:**
- `name` (optional) - Updated name of the pet
- `status` (optional) - Updated status of the pet

**Content-Type:** `application/x-www-form-urlencoded`

**Response:** `200 OK`

**Error Responses:**
- `405` - Invalid input

### 7. Delete a Pet

**Method:** `DELETE`

**URL:** `/pet/{petId}`

**Path Parameters:**
- `petId` (required) - Pet id to delete

**Headers:**
- `api_key` (optional) - API key for authorization

**Response:** `200 OK`

**Error Responses:**
- `400` - Invalid ID supplied
- `404` - Pet not found

### 8. Upload Pet Image

**Method:** `POST`

**URL:** `/pet/{petId}/uploadImage`

**Path Parameters:**
- `petId` (required) - ID of pet to update

**Form Data:**
- `additionalMetadata` (optional) - Additional data to pass to server
- `file` (required) - File to upload

**Content-Type:** `multipart/form-data`

**Response:** `200 OK`
```json
{
  "code": 200,
  "type": "unknown",
  "message": "additionalMetadata: file uploaded to ./uploaded_file.jpg, 12345 bytes"
}
```

## Pet Model

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

**Required Fields:**
- `name` - Pet name
- `photoUrls` - Array of photo URLs (at least one)

**Optional Fields:**
- `id` - Auto-generated if not provided
- `category` - Pet category
- `tags` - Array of tags
- `status` - Default is `available`