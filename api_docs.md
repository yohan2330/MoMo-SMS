# MoMo SMS API Documentation

**Base URL:** `http://localhost:8000`

## Authentication
All endpoints require Basic Authentication.

- Username: `admin`
- Password: `password`

Requests without valid credentials return **401 Unauthorized** and header `WWW-Authenticate`.

---

## Endpoints

### GET /transactions
**Description:** List all transactions.
