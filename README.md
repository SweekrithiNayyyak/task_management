# task_management
# 📁 Full Project Setup for Flask + PostgreSQL Task Manager API


---

## 📦 Folder Structure

```
task_manager/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── projects.py
│   │   └── tasks.py
│   └── utils/
│       └── __init__.py
├── config.py
├── run.py
├── requirements.txt
├── .env
├── README.md
```

---

## 📄 .env

```env
DATABASE_URL=postgresql://task_user:yourpassword@localhost:5432/task_db
```

---

## 📄 requirements.txt

```text
Flask
SQLAlchemy
psycopg2-binary
python-dotenv
Flask-Migrate
```

---

## 📄 README.md

```markdown
# Task Management API (Flask + PostgreSQL)

A simple REST API to manage users, projects, and tasks with dependencies.

## 🚀 Setup Instructions

### 1. Clone the repository
```

git clone [https://github.com/yourusername/task-manager.git](https://github.com/yourusername/task-manager.git)
cd task-manager

```

### 2. Create virtual environment and activate
```

python -m venv venv

# On Windows:

venv\Scripts\activate

# On Linux/macOS:

source venv/bin/activate

```

### 3. Install dependencies
```

pip install -r requirements.txt

```

### 4. Setup PostgreSQL
Ensure PostgreSQL is installed and running.
Create a database and user:
```

psql -U postgres
CREATE DATABASE task\_db;
CREATE USER task\_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE task\_db TO task\_user;
\q

````

### 5. Configure `.env`
Create a `.env` file:
```env
DATABASE_URL=postgresql://task_user:yourpassword@localhost:5432/task_db
````

### 6. Run database migrations

```
flask db init       # Run only once
flask db migrate -m "Initial tables"
flask db upgrade
```

### 7. Run the Flask application

```
flask run
```

The app runs at `http://localhost:5000`

## 📬 API Endpoints

### Users

* `POST /users` – Create user
* `GET /users` – List users
* `GET /users/<id>` – Get user by ID

### Projects

* `POST /projects` – Create project
* `GET /projects` – List projects
* `GET /projects/<id>` – Get project by ID
* `GET /projects/<id>/tasks` – List tasks for a project

### Tasks

* `POST /tasks` – Create task
* `GET /tasks/<id>` – Get task by ID
* `PATCH /tasks/<id>/status` – Update task status
* `GET /tasks/user/<user_id>` – Tasks assigned to a user
* `GET /tasks/status/<status>` – Tasks by status

## ✅ Notes

* Task status must be one of: `PENDING`, `IN_PROGRESS`, `COMPLETED`
* A task cannot be completed unless all dependencies are completed
* Circular dependencies are not automatically detected (yet)

```

---

[The rest of the project files remain unchanged...]

```
