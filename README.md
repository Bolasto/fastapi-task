# 📝 FastAPI Task Management API

A robust and secure **Task Management API** built with **FastAPI** and **MongoDB**, featuring JWT authentication, comprehensive task management, and advanced validation.

---

## 🚀 Features

- ✅ User Authentication (JWT-based)
- ✅ MongoDB Integration for Persistent Storage
- ✅ Create, Retrieve, Update, and Delete Tasks
- ✅ Advanced Task Validation
  - Title & Description Validation
  - Email Format Validation
  - Date Format Validation (YYYY-MM-DD)
  - Priority & Status Enums
- ✅ Search & Filter Tasks
  - Filter by Priority
  - Filter by Status
  - Search in Title/Description
- ✅ Duplicate Title Prevention
- ✅ Auth-protected Endpoints
- ✅ Comprehensive Error Handling

---

## 📦 Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **MongoDB**: NoSQL database for persistent storage
- **Motor**: Async MongoDB driver for Python
- **Python 3.10+**: Modern Python features
- **JWT**: Secure authentication
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fastapi-task-api.git
cd fastapi-task-api
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file with the following required variables:
```env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MONGO_URL=your_mongodb_connection_string  # Required for database connection
```

### 5. Run the Server
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`
API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`

---

## 📂 Project Structure
```
fastapi-task-api/
│
├── app/
│   ├── routes/
│   │   ├── auth.py      # Authentication endpoints
│   │   └── tasks.py     # Task management endpoints
│   ├── database.py      # MongoDB connection and configuration
│   ├── models.py        # Pydantic models and validation
│   ├── utils.py         # Utility functions
│   └── main.py         # FastAPI application setup
│
├── requirements.txt    # Project dependencies
├── .env              # Environment variables (create this)
└── README.md
```

## 🔐 Authentication

### Get Token
Use `/token` endpoint with:
```json
{
  "username": "admin",
  "password": "admin"
}
```

## 📌 API Endpoints

| Method | Endpoint | Description | Query Parameters |
|--------|----------|-------------|------------------|
| POST | `/token` | Login & get access token | - |
| POST | `/tasks` | Create new task | - |
| GET | `/tasks` | Get all tasks | `priority`, `status`, `search` |
| GET | `/tasks/{task_id}` | Get a specific task | - |
| PUT | `/tasks/{task_id}` | Update a task | - |
| DELETE | `/tasks/{task_id}` | Delete a task | - |

## 📝 Task Model

```json
{
  "title": "string (required, max 100 chars)",
  "description": "string (required)",
  "email": "string (valid email format)",
  "due_date": "string (YYYY-MM-DD format)",
  "priority": "enum (LOW, MEDIUM, HIGH)",
  "status": "enum (NOT_STARTED, IN_PROGRESS, COMPLETED)"
}
```

## 🔍 Query Parameters

- `priority`: Filter tasks by priority (LOW, MEDIUM, HIGH)
- `status`: Filter tasks by status (NOT_STARTED, IN_PROGRESS, COMPLETED)
- `search`: Search in task titles and descriptions

## ⚠️ Error Handling

The API includes comprehensive error handling:
- Validation errors for invalid input
- Duplicate title prevention
- Database connection errors
- Authentication errors
- Not found errors for invalid task IDs
