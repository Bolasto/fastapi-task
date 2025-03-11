# 📝 FastAPI Task Management API

A simple and secure **Task Management API** built with **FastAPI**, supporting user authentication with JWT and CRUD operations for tasks.

---

## 🚀 Features

- ✅ User Authentication (JWT-based)
- ✅ Create, Retrieve, Update, and Delete Tasks
- ✅ Task Fields: Title, Description, Due Date, Priority, Status
- ✅ Auth-protected Endpoints
- ✅ Lightweight and Easy to Run

---

## 📦 Tech Stack

- **FastAPI**
- **Python 3.10+**
- **JWT (JSON Web Tokens)**
- **Pydantic**
- **Uvicorn**

---

## 🔧 Setup Instructions

### 1. Clone the Repository

git clone https://github.com/your-username/fastapi-task-api.git
cd fastapi-task-api

2. Create a Virtual Environment
### python3 -m venv venv
### source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
### pip install -r requirements.txt

4. Set Environment Variables (Optional)
Create a .env file and set your secret key:
### SECRET_KEY=your_secret_key_here
### ALGORITHM=HS256
### ACCESS_TOKEN_EXPIRE_MINUTES=30

5. Run the Server
### uvicorn app.main:app --reload

## 📂 Project Structure
fastapi-task-api/
│
├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── utils.py
│   └── main.py
│
├── requirements.txt
└── README.md

🔐 Authentication
Get Token
Use /token endpoint with:
###{
  "username": "admin",
  "password": "admin"
}

📌 API Endpoints
Method	Endpoint	Description
POST	/token	Login & get access token
POST	/tasks	Create new task
GET	/tasks	Get all tasks
GET	/tasks/{task_id}	Get a specific task
PUT	/tasks/{task_id}	Update a task
DELETE	/tasks/{task_id}	Delete a task
