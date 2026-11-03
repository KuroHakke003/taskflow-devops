# Initial architecture

```text
Client
  |
  | HTTP
  v
TaskFlow API (FastAPI, port 8000)
  |
  | PostgreSQL protocol
  v
PostgreSQL database (port 5432)
```

The API is a single service (a modular monolith). PostgreSQL stores task records.
The `/health/live` endpoint checks that the API process responds. The
`/health/ready` endpoint checks whether the database can be reached.

This is an intentionally small starting point for infrastructure practice.
