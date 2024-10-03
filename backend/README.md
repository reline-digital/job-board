# Job Board Backend

This is the backend for the Job Board application, built using Django. Follow the steps below to set up the project on your local machine.

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtualenv (or another virtual environment manager..ie poetry)

## Getting Started

### 1. Create the virtual environment (Using Virtualenv)
```bash
python -m venv name_of_environment
```

### 2. Activate the environment
- Windows: env\Scripts\activate
- Mac/Linux: source env/bin/activate

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
- There is a `.env_example` file provided in the project. Create a `.env` file by copying the contents of `.env_example` and updating the values as needed:
```bash
cp .env_example .env
```

### 5. Start the project
```bash
python manage.py runserver
```
- Access the project on http://127.0.0.1:8000.

# API Endpoints
## 1. User Registration
- **Endpoint:** `/api/signup/`
- **Method:** `POST`
- **Description:** Register a new user with a unique username and email.

#### Request Body:
```json
{
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "password1": "password123",
    "password2": "password123"
}
```
**Response (Success: `201 Created`):**
```json
{
    "message": "User registered successfully."
}
```

## 2. User Login
- **Endpoint:** `/api/login/`
- **Method:** `POST`
- **Description:** Authenticates the user based on the provided credentials.

#### Request Body:
```json
{
    "username": "johndoe",
    "password": "password123"
}
```
**Response (Success: `200 OK`):**
```json
{
    "message": "Login successful"
}
```