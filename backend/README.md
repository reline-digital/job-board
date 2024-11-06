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
    "message": "User registered successfully.",
    "token": {
        "refresh": "<refresh_token>",
        "access": "<access_token>"
    }
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
    "message": "Login successful",
    "tokens": {
        "refresh": "<refresh_token>",
        "access": "<access_token>"
    }
}
```

## 3. Password Reset Request:
- **Endpoint:** `/password-reset/`
- **Method:** `POST`
- **Description:** Sends a password reset email to the register user.
#### Request Body:
```json
{
    "email": "johndoe@example.com"
}
```
**Response (Success: `200 OK`):**
```json
{
    "message": "Password reset email sent."
}
```

## 4. Password Reset Confirmation
- **Endpoint:** `/reset/<uidb64>/<token>/`
- **Method:** `POST`
- **Description:** Confirms the password reset using the token and allows the user to set a new password.

#### Request Body:
```json
{
    "new_password": "newpassword123",
    "confirm_password": "newpassword123"
}
```
**Response (Success: `200 OK`):**
```json
{
    "message": "Password has been reset successfully."
}
```

## 5. Token Refresh
- **Endpoint:** `/api/toke/refresh/`
- **Method:** `POST`
- **Description:** Refreshes the access token using the refresh token.

#### Request Body
```json
{
    "refresh": "<refresh_token>"
}
```
**Response (Success: `200 OK`)**
```json
{
    "access": "<new_access_token>"
}
```


# JOb Management Endpoints
## 1. List Jobs
- **Endpoint:** `/jobs/`
- **Method:** `GET`
- **Description:** Retrieves a list of all job postings. Requires authentication.

**Response (Success: `200 OK`)**
```json
[
    {
        "id": 1,
        "title": "Software Engineer",
        "description": "Develop and maintain software solutions.",
        "employer": "Company ABC"
    },
    ...
]
```

## 2. Create Job
- **Endpoint:** `/jobs/create/`
- **Method:** `POST`
- **Description:** Creates a new job posting. Requires authentication.

#### Request Body**
```json
{
    "title": "Software Engineer",
    "description": "Looking for a Software Engineer to join our team.",
    "requirements": "Experience with Django and REST Framework.",
    "salary": 70000,
    "location": "Remote"
}
```

**Response (SuccessL `201 Created`)**
```json
{
    "id": 1,
    "title": "Software Engineer",
    "description": "Looking for a Software Engineer to join our team.",
    "requirements": "Experience with Django and REST Framework.",
    "salary": 70000,
    "location": "Remote",
    "employer_id": 1
}
```

## 3. Retrieve Job
- **Endpoint:** `/jobs/<int:pk>/`
- **Method:** `GET`
- **Description:** Retrieves details of a specific job by ID. Requires authentication.

**Response (Success: `200 Ok`)**
```json
{
    "id": 1,
    "title": "Software Engineer",
    "description": "Looking for a Software Engineer to join our team.",
    "requirements": "Experience with Django and REST Framework.",
    "salary": 70000,
    "location": "Remote",
    "employer_id": 1
}
```

## Update Job
- **Endpoint:** `/jobs/<int:pk>/update/`
- **Method:** `PUT`
- **Description:** Updates a job posting. Only the job creator can update the job. Requires authentication.

**Request Body**
```json
{
    "id": 1,
    "title": "Backend Developer",
    "description": "Looking for a Backend Developer to join our team.",
    "requirements": "Experience with Django and REST Framework.",
    "salary": 70000,
    "location": "Remote",
    "employer_id": 1
}
```
**Response (Success: `200 ok`)**

## 5. Delete Job
- **Endpoint:** `/jobs/<int:pk>/delete/`
- **Method:** `DELETE`
- **Description:** Deletes a job posting. Only the job creator can delete the job. Requires authentication.

**Response (Success: `204 No Content`)**
