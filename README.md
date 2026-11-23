## Hostel Visitor Register


A web-based application developed to manage visitor records in a hostel. The system allows hostel staff to register and log in, record visitor information and view the registered visitor details.

The main aim of this project is to make hostel visitor management easier and maintain visitor information digitally instead of maintaining everything manually.

---

## 1. Project and Team

### Project Name :**Hostel Visitor Register**
## Team Members: Amruta, Lakshya, Supriya
### Team Members and Endpoint Contribution

| Endpoint ID | Endpoint | Method | Developed By |
|---|---|---|---|
| A1 | Staff Registration | POST | Supriya |
| A2 | Staff Login | POST | Amruta |
| A3 | Refresh Token | POST | Amruta |
| E1 | Register Visitor | POST | Supriya |
| E2 | View Visitors | GET | Amrutha |

---

## 2. Live App

The application is deployed on an AWS EC2 instance.

**Live Application Link:**

http://13.126.187.132:8000/docs
<img width="1459" height="455" alt="image" src="https://github.com/user-attachments/assets/f1e32bb5-9db7-4206-a165-3967f9fd5338" />



---

## 3. How to Run the Project

Follow these steps to run the project on a fresh laptop.

### Step 1: Clone the Repository

```bash
git clone https://github.com/lakshyar175/hostel-visitor-register.git
```

Navigate into the project folder:

```bash
cd hostel-visitor-register
```

### Step 2: Run the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment (Windows PowerShell):

```bash
venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

The backend will run at:

`http://127.0.0.1:8000`

Swagger API documentation:

`http://127.0.0.1:8000/docs`

### Step 3: Run the Frontend

Open another terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will run at:

`http://localhost:5173`

### Step 4: Run Using Docker

Navigate to the directory containing the Dockerfile.

Build the Docker image:

```bash
docker build -t hostel-visitor-register .
```

Run the Docker container:

```bash
docker run -d -p 8000:8000 --name hostel-visitor-register hostel-visitor-register
```

Check whether the container is running:

```bash
docker ps
```

Access the application API:

`http://localhost:8000/docs`

---

## 4. API Contract

The application provides five main API endpoints for staff authentication and visitor management.

### Endpoint Details

| ID | Method | Endpoint | Request Body | Success Code |
|---|---|---|---|---|
| A1 | POST | `/register` | username, email, password | 201 |
| A2 | POST | `/login` | email, password | 201 |
| A3 | POST | `/refresh` | Refresh token in header | 201 |
| E1 | POST | `/visitors` | visitor_name, student_name, room_no, purpose, visit_date | 201 |
| E2 | GET | `/visitors` | Access token in header | 200 |

### Request Body Examples

**A1 – Staff Registration**

```json
{
  "username": "staff1",
  "email": "staff@gmail.com",
  "password": "password123"
}
```

**A2 – Staff Login**

```json
{
  "email": "staff@gmail.com",
  "password": "password123"
}
```

**A3 – Refresh Token**

The refresh token is passed through the request header.

**E1 – Register Visitor**

```json
{
  "visitor_name": "Rahul",
  "student_name": "Arun",
  "room_no": "205",
  "purpose": "Meeting",
  "visit_date": "2026-11-23"
}
```

**E2 – View Visitors**

The access token is passed through the request header.

### Error Rules

| HTTP Status Code | Error | Description |
|---|---|---|
| 401 | Unauthorized | Invalid email or password |
| 409 | Conflict | Email already exists |
| 422 | Validation Error | Required fields are missing or input data is invalid. |

---

## 5. Database

The application uses SQLite for storing staff and visitor information. SQLAlchemy is used to interact with the database.

The database file is named `visitors.db`.

### Table 1: Users

This table stores the staff registration and authentication details.

| Column Name | Data Type | Description |
|---|---|---|
| id | Integer | Primary key |
| username | String | Staff username |
| email | String | Staff email address |
| hashed_password | String | Hashed staff password |
| created_at | Date | Account creation date |

### Table 2: Visitors

This table stores the visitor information registered by staff members.

| Column Name | Data Type | Description |
|---|---|---|
| id | Integer | Primary key |
| user_id | Integer | Foreign key referencing users.id |
| visitor_name | String | Name of the visitor |
| student_name | String | Name of the student being visited |
| room_no | String | Student's room number |
| purpose | String | Purpose of the visit |
| visit_date | Date | Date of the visit |
| created_at | Date | Record creation date |


## 6. Screenshots

The following screenshots demonstrate the working of the application.

### 1. Staff Registration

<img width="917" height="775" alt="image" src="https://github.com/user-attachments/assets/f51fb2ad-7744-4612-bb6c-7ebaf0db7d66" />



<img width="317" height="433" alt="image" src="https://github.com/user-attachments/assets/b2600e4d-14dc-4765-a683-89c0b9c501ed" />




### 2. Staff Login


<img width="918" height="795" alt="image" src="https://github.com/user-attachments/assets/e9a2279f-09ce-43a0-8b74-b4a73175caef" />




### 3. Dashboard

<img width="506" height="241" alt="image" src="https://github.com/user-attachments/assets/ea4608bc-0745-4053-adea-66c8063efb6d" />




### 4. Error Message


<img width="605" height="648" alt="image" src="https://github.com/user-attachments/assets/af545c71-ad18-4446-96a1-9254b38dcb67" />



### 5. API Endpoint in Swagger UI

<img width="1600" height="850" alt="image" src="https://github.com/user-attachments/assets/96ad7fdd-91d7-40fd-97c1-241c22f8fc92" />




### 6. GitHub Actions

Screenshot showing a successful GitHub Actions workflow execution after deployment.

<img width="1360" height="353" alt="image" src="https://github.com/user-attachments/assets/2a2faeb6-689b-424b-ad70-935e5d62e2a2" />




## 7. Known Issues and Future Improvements

