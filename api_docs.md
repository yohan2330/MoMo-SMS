# Mobile Money SMS API Documentation

**Base URL:** `http://localhost:8000`  
**Authentication:** Basic Auth (username:password)

---

## Authentication

All endpoints require Basic Authentication.

**Valid Credentials:**
- Username: `admin` | Password: `password123`
- Username: `user1` | Password: `securepass`

**Header Format:**
```
Authorization: Basic <base64_encoded_credentials>
```

**Example:**
```bash
curl -u admin:password123 http://localhost:8000/transactions
```

---

## Endpoints

### 1. GET /transactions

Get all transactions.

**Request:**
```bash
curl -u admin:password123 http://localhost:8000/transactions
```

**Response (200 OK):**
```json
{
  "data": [
    {
      "id": 1,
      "type": "deposit",
      "amount": 50000.0,
      "sender": "John Doe",
      "receiver": "MTN_MOMO",
      "timestamp": "2024-01-15T10:30:00",
      "message": "Deposit successful"
    }
  ]
}
```

**Errors:**
- `401 Unauthorized` - Invalid credentials

---

### 2. GET /transactions/{id}

Get one transaction by ID.

**Request:**
```bash
curl -u admin:password123 http://localhost:8000/transactions/1
```

**Response (200 OK):**
```json
{
  "data": {
    "id": 1,
    "type": "deposit",
    "amount": 50000.0,
    "sender": "John Doe",
    "receiver": "MTN_MOMO",
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

**Errors:**
- `401 Unauthorized` - Invalid credentials
- `404 Not Found` - Transaction doesn't exist

---

### 3. POST /transactions

Create new transaction.

**Request:**
```bash
curl -X POST -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "type": "transfer",
    "amount": 75000,
    "sender": "Alice",
    "receiver": "Bob",
    "message": "Payment"
  }' \
  http://localhost:8000/transactions
```

**Required Fields:**
- `type` (string)
- `amount` (number)
- `sender` (string)
- `receiver` (string)

**Response (201 Created):**
```json
{
  "data": {
    "id": 31,
    "type": "transfer",
    "amount": 75000,
    "sender": "Alice",
    "receiver": "Bob",
    "message": "Payment",
    "timestamp": "2024-10-01T14:30:00"
  }
}
```

**Errors:**
- `400 Bad Request` - Missing required fields
- `401 Unauthorized` - Invalid credentials

---

### 4. PUT /transactions/{id}

Update existing transaction.

**Request:**
```bash
curl -X PUT -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"amount": 85000, "message": "Updated"}' \
  http://localhost:8000/transactions/1
```

**Response (200 OK):**
```json
{
  "data": {
    "id": 1,
    "type": "deposit",
    "amount": 85000,
    "sender": "John Doe",
    "receiver": "MTN_MOMO",
    "message": "Updated",
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

**Errors:**
- `401 Unauthorized` - Invalid credentials
- `404 Not Found` - Transaction doesn't exist

---

### 5. DELETE /transactions/{id}

Delete transaction.

**Request:**
```bash
curl -X DELETE -u admin:password123 \
  http://localhost:8000/transactions/1
```

**Response (200 OK):**
```json
{
  "data": {
    "message": "Transaction 1 deleted",
    "deleted": {
      "id": 1,
      "type": "deposit",
      "amount": 50000
    }
  }
}
```

**Errors:**
- `401 Unauthorized` - Invalid credentials
- `404 Not Found` - Transaction doesn't exist

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Success |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Auth failed |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |

---

## Error Format

All errors return:
```json
{
  "error": "Error description"
}
```

---

## Testing Examples

### Postman

1. **Set Authorization:** Basic Auth
   - Username: `admin`
   - Password: `password123`

2. **Test GET:**
   - Method: GET
   - URL: `http://localhost:8000/transactions`

3. **Test POST:**
   - Method: POST
   - URL: `http://localhost:8000/transactions`
   - Body: Raw JSON
   ```json
   {
     "type": "deposit",
     "amount": 50000,
     "sender": "Test",
     "receiver": "MTN"
   }
   ```

### Python

```python
import requests
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('admin', 'password123')
url = 'http://localhost:8000/transactions'

# GET
response = requests.get(url, auth=auth)
print(response.json())

# POST
data = {
    "type": "deposit",
    "amount": 50000,
    "sender": "Test",
    "receiver": "MTN"
}
response = requests.post(url, json=data, auth=auth)
print(response.json())
```

---

**Version:** 1.0  
**Last Updated:** October 2024
