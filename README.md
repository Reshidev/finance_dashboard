# Finance Dashboard API

A Django REST API for managing personal or organizational financial records with role-based access control and JWT authentication.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Permissions](#permissions)
- [Database Models](#database-models)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project provides a RESTful API for tracking financial transactions (income and expenses) with user management and dashboard summaries. It supports multiple user roles (Viewer, Analyst, Admin) with appropriate access controls.

## Features

- **User Management**: Registration, authentication, and role-based access
- **Financial Records**: CRUD operations for income/expense tracking
- **Dashboard**: Real-time summary of total income, expenses, and net balance
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Permissions**: Granular access control (Viewer, Analyst, Admin)
- **RESTful API**: Full REST API with Django REST Framework
- **SQLite Database**: Lightweight database for development

## Tech Stack

- **Backend**: Django 5.2.4
- **API Framework**: Django REST Framework
- **Authentication**: Simple JWT
- **Database**: SQLite (development), configurable for production
- **Python**: 3.8+

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd finance_dashboard
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for Django admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`.

## Configuration

### Environment Variables

Create a `.env` file in the project root (optional for development):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### Settings

Key configuration in `finance_dashboard/settings.py`:

- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Use a strong, unique key in production
- `ALLOWED_HOSTS`: Configure for your domain in production
- `DATABASES`: Configure PostgreSQL/MySQL for production

## Usage

### Starting the Server

```bash
python manage.py runserver
```

### API Testing

Import the provided Postman collection (`finance_dashboard.postman_collection.json`) into Postman for easy testing.

1. Set the `base_url` variable to `http://localhost:8000`
2. Register a new user or use existing credentials
3. Obtain JWT tokens via the login endpoint
4. Use the access token in the `Authorization` header for authenticated requests

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/login/` | Obtain JWT access and refresh tokens | No |
| POST | `/api/token/refresh/` | Refresh access token | No |
| POST | `/api/register/` | Register a new user | No |

### Users

| Method | Endpoint | Description | Auth Required | Permissions |
|--------|----------|-------------|---------------|-------------|
| GET | `/api/users/` | List all users | Yes | Admin only |

### Financial Records

| Method | Endpoint | Description | Auth Required | Permissions |
|--------|----------|-------------|---------------|-------------|
| GET | `/api/records/` | List financial records | Yes | Analyst/Admin (read), Admin (write) |
| POST | `/api/records/` | Create a new record | Yes | Admin |
| GET | `/api/records/{id}/` | Retrieve a specific record | Yes | Analyst/Admin |
| PUT | `/api/records/{id}/` | Update a record | Yes | Admin |
| PATCH | `/api/records/{id}/` | Partially update a record | Yes | Admin |
| DELETE | `/api/records/{id}/` | Delete a record | Yes | Admin |

### Dashboard

| Method | Endpoint | Description | Auth Required | Permissions |
|--------|----------|-------------|---------------|-------------|
| GET | `/api/dashboard/` | Get financial summary | Yes | Any authenticated user |

### Admin

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| N/A | `/admin/` | Django admin interface | Yes (staff) |

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Login**: Send POST request to `/api/login/` with `username` and `password`
2. **Receive Tokens**: Response includes `access` and `refresh` tokens
3. **Use Access Token**: Include in requests as `Authorization: Bearer <access_token>`
4. **Refresh Token**: Use `/api/token/refresh/` when access token expires

Tokens expire according to settings:
- Access token: 60 minutes
- Refresh token: 7 days

## Permissions

The system implements role-based access control:

### User Roles

- **Viewer**: Can view their own financial records and dashboard
- **Analyst**: Can view all financial records and dashboard (read-only)
- **Admin**: Full access to all records, users, and dashboard (read/write)

### Permission Matrix

| Resource | Viewer | Analyst | Admin |
|----------|--------|---------|-------|
| Own Records | Read | Read | Read/Write |
| All Records | No | Read | Read/Write |
| Dashboard | Read | Read | Read |
| User List | No | No | Read |

## Database Models

### User Model

Custom user model extending Django's `AbstractUser`:

```python
class User(AbstractUser):
    ROLE_CHOICES = (
        ('Viewer', 'Viewer'),
        ('Analyst', 'Analyst'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Viewer')
```

### FinancialRecord Model

```python
class FinancialRecord(models.Model):
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    amount = models.FloatField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

## Testing

### Running Tests

```bash
python manage.py test
```

### Test Coverage

The project includes basic test files in each app (`tests.py`), though they are currently empty. Add comprehensive tests for:

- User registration and authentication
- Financial record CRUD operations
- Permission checks
- Dashboard calculations

### Postman Testing

Use the provided Postman collection for manual API testing:

1. Import `finance_dashboard.postman_collection.json`
2. Set environment variables
3. Run requests in order

## Deployment

### Production Checklist

1. Set `DEBUG = False`
2. Use a strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Use a production database (PostgreSQL recommended)
5. Set up proper logging
6. Configure static files serving
7. Use HTTPS
8. Set up monitoring and backups

### Example Production Settings

```python
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}
```

### Docker Deployment

Create a `Dockerfile` and `docker-compose.yml` for containerized deployment.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `python manage.py test`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Create a Pull Request

### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write comprehensive tests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For questions or support, please open an issue in the repository.