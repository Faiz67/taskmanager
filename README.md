# Task Manager API

A FastAPI-based task management system with user authentication, PostgreSQL, and Redis.

## Features

- User registration and login
- JWT-based authentication with session management via Redis
- CRUD operations for tasks
- PostgreSQL for persistent storage
- **Interactive API documentation available at** [`/docs`](http://localhost:8000/docs) **(Swagger UI)**

---

## Getting Started

### 1. Initialize Database

Start all services using Docker Compose:

```sh
docker-compose up --build
```

Initialize the database schema by visiting:

```
GET http://localhost:8000/initalize_db
```

---

### 2. Register User

```
POST /auth/register
Content-Type: application/json

{
  "user_name": "your_username",
  "email_id": "your_email@example.com",
  "password": "your_password"
}
```

---

### 3. User Login

```
POST /auth/login
Content-Type: application/json

{
  "user_name": "your_username",
  "password": "your_password"
}
```

- On success, a session token is set as a cookie (`x-session-token`).

---

### 4. Add Task

```
POST /tasks/add
Content-Type: application/json
Cookie: x-session-token=your_token

{
  "title": "Task Title",
  "description": "Task Description"
}
```

---

### 5. View All Tasks

```
GET /tasks/all
Cookie: x-session-token=your_token
```

Optional query params: `limit`, `page`, `show_only_completed`

---

### 6. View Task with Task ID

```
GET /tasks/{task_id}
Cookie: x-session-token=your_token
```

---

### 7. Edit Task

```
PUT /tasks/edit/{task_id}
Content-Type: application/json
Cookie: x-session-token=your_token

{
  "title": "Updated Title",
  "description": "Updated Description",
  "completed": true
}
```

---

### 8. Delete Task

```
DELETE /tasks/delete/{task_id}
Cookie: x-session-token=your_token
```

---

### 9. Logout

```
GET /auth/logout
Cookie: x-session-token=your_token
```

---

## API Documentation

You can interact with and test all endpoints using the **Swagger UI** at:

```
http://localhost:8000/docs
```

---

## Notes

- All endpoints (except registration, login, and database initialization) require authentication via the `x-session-token` cookie.
- Adjust host/port as needed if running on a different environment.

---

##
