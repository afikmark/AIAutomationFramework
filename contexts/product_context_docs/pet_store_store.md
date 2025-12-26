# Pet Store API - Store Endpoints

## Overview

Store endpoints manage pet store orders and inventory tracking.

**Base Path:** `/store`

**Authentication:** API key (for some operations)

## Endpoints

### 1. Get Store Inventory

**Method:** `GET`

**URL:** `/store/inventory`

**Authentication:** API key required

**Description:** Returns pet inventories by status

**Response:** `200 OK` - Map of status codes to quantities

**Example Response:**
```json
{
  "available": 42,
  "pending": 15,
  "sold": 123
}
```

### 2. Place an Order for a Pet

**Method:** `POST`

**URL:** `/store/order`

**Request Body:**
```json
{
  "id": 0,
  "petId": 123,
  "quantity": 1,
  "shipDate": "2024-12-26T10:00:00.000Z",
  "status": "placed",
  "complete": false
}
```

**Response:** `200 OK` - Returns the created order object

**Error Responses:**
- `400` - Invalid order

**Status Values:**
- `placed` - Order has been placed
- `approved` - Order has been approved
- `delivered` - Order has been delivered

### 3. Find Purchase Order by ID

**Method:** `GET`

**URL:** `/store/order/{orderId}`

**Path Parameters:**
- `orderId` (required) - ID of order to retrieve (valid range: 1-10)

**Response:** `200 OK` - Order object

**Example Response:**
```json
{
  "id": 5,
  "petId": 123,
  "quantity": 2,
  "shipDate": "2024-12-26T10:00:00.000Z",
  "status": "approved",
  "complete": true
}
```

**Error Responses:**
- `400` - Invalid ID supplied
- `404` - Order not found

### 4. Delete Purchase Order by ID

**Method:** `DELETE`

**URL:** `/store/order/{orderId}`

**Path Parameters:**
- `orderId` (required) - ID of order to delete (minimum: 1)

**Response:** `200 OK`

**Error Responses:**
- `400` - Invalid ID supplied
- `404` - Order not found

## Order Model

```json
{
  "id": 0,
  "petId": 0,
  "quantity": 0,
  "shipDate": "2024-01-01T00:00:00.000Z",
  "status": "placed|approved|delivered",
  "complete": true|false
}
```

**Fields:**
- `id` - Order ID (auto-generated)
- `petId` - ID of the pet being ordered
- `quantity` - Number of pets in order
- `shipDate` - Estimated ship date (ISO 8601 format)
- `status` - Order status
- `complete` - Whether order is complete


## Notes

- Order IDs must be in the valid range (1-10) for retrieval
- The `shipDate` field uses ISO 8601 datetime format
- Inventory endpoint requires API key authentication
- Order endpoints do not require authentication (demo purposes)
