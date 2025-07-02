
# 🧑‍💼 Minimal HR System – Django API

A simple HR system built with Django. It allows candidates to register and upload resumes, and lets HR admins view candidates and manage application statuses.

---

## 🚀 Features

### Candidate Functionality
- Register with name, DOB, experience, department, email, and resume.
- Upload PDF or DOCX (max 5MB).
- View application status + feedback.

### Admin Functionality (via `X-ADMIN=1` HTTP header)
- View paginated list of candidates.
- Filter by department.
- Download resumes.
- Update application statuses and feedback.
- Track status change history.

---

## ⚙️ Tech Stack

- **Python 3.10**
- **Django 5.x**
- **PostgreSQL**
- **Docker + Docker Compose**

---

## 📦 Requirements

### Run via Docker (recommended)

- Docker
- Docker Compose

### Run locally (manual)

- Python 3.10+
- PostgreSQL
- pip / venv

---

## 🐳 Quickstart with Docker

```bash
# Clone the repo
git clone https://github.com/sameer-990/HR_System.git
cd hr-system

# Build and run
docker-compose up --build
```

- App: http://localhost:8000
- Admin resume download requires header: `X-ADMIN: 1`

---

## 🖥️ Manual Setup (Local Environment)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env or set DB settings in settings.py
# Create DB in PostgreSQL manually or use pgAdmin

# Run migrations
python manage.py migrate

# Run server
python manage.py runserver
```

---

## 🗃️ Database Setup

Use either method:

### A. With Docker (Auto setup)
```bash
docker-compose up
```

### B. Manually via psql
```sql
CREATE DATABASE hr_system_db;
CREATE USER hr_user WITH PASSWORD 'hr_pass';
GRANT ALL PRIVILEGES ON DATABASE hrdb TO hr_user;
```

---

## 📑 API Documentation

### 🔐 Authentication

- Admin endpoints require header:  
  `X-ADMIN: 1`

---

### 📥 Register Candidate

`POST /api/candidates/register/`

**Form Fields:**

| Field              | Required | Type                         |
|-------------------|----------|------------------------------|
| full_name          | ✅       | string                       |
| date_of_birth      | ✅       | date (YYYY-MM-DD)            |
| years_of_experience| ✅       | int >= 0                     |
| department         | ✅       | enum (`IT`, `HR`, `Finance`) |
| resume             | ✅       | file (PDF/DOCX) only         |


**Returns:**
```json
{
    "id": 1,
    "full_name": "Test 1",
    "date_of_birth": "2014-09-29",
    "experience_years": 3,
    "department": "Finance",
    "email": "test1@gmail.com",
    "resume": "http://127.0.0.1:8000/media/resumes/1/API_Documentation_-_Order_Status_Update.pdf",
    "created_at": "2025-07-01T10:44:45.198960Z",
    "application_status": "Submitted"
}
```


---

### 🔍 Check Application Status

`GET /api/candidates/status/<candidate_id>/`

**Returns:**

```json
{
    "full_name": "Test 1",
    "application_status": "Under Review",
    "statuses": [
        {
            "status": "Under Review",
            "updated_at": "2025-06-30T16:10:08.627059Z",
            "feedback": "Feedback 1",
            "updated_by": "Admin"
        },
        {
            "status": "Under Review",
            "updated_at": "2025-06-30T16:05:06.180348Z",
            "feedback": "Feedback 2",
            "updated_by": "Admin"
        }
    ]
}
```

---

### 🔐 Admin: List Candidates

`GET /api/candidates/admin/candidates/`

**Headers:**

`X-ADMIN: 1`

**Query Params:**

- `department=IT|HR|Finance`
- `page=1`

**Returns:**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "full_name": "Test 2",
            "date_of_birth": "2004-10-19",
            "experience_years": 15,
            "department": "HR"
        },
        {
            "full_name": "Test 1",
            "date_of_birth": "2014-09-29",
            "experience_years": 3,
            "department": "Finance"
        }
    ]
}
```


---

### 🔐 Admin: Download Resume

`GET /api/candidates/admin/candidates/<candidate_id>/resume/`

Returns `application/pdf` or `application/vnd.openxmlformats-officedocument.wordprocessingml.document`.

---

### 🔐 Admin: Update Application Status

`POST /api/candidates/admin/candidates/<candidate_id>/status/`

**Body:**

```json
{
  "status": "Accepted",
  "feedback": "Welcome aboard"
}
```

**Returns:**

```json
{
    "detail": "Status updated"
}
```

---

## 🧪 Running Tests

```bash
# Unit and integration tests
python manage.py test candidates.test
```

---

## 📁 File Uploads

Uploaded resumes stored at:

```
media/resumes/<candidate_id>/filename.pdf
```

---

## 📃 Requirements

```txt
Django>=5.0
djangorestframework
psycopg2-binary
boto3
django-storages
gunicorn
```

> Full list in [`requirements.txt`](./requirements.txt)

---

## 📝 License

MIT – Do what you want, but give credit.

---

## 🙋 Support

Have questions? [Open an issue](https://github.com/sameer-990/HR_System/issues).
