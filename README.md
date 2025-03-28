# ELTS School of English - Backend API

## Overview
This is the backend API service for the ELTS (English Language Teaching System) School of English. Built with FastAPI, it provides a robust and scalable solution for managing students, teachers, courses, and enrollments in an English language school.

## Features
- 🔐 JWT Authentication
- 👥 User Management (Admin, Teachers, Students)
- 📚 Course Management
- ✍️ Enrollment System
- 📊 Dashboard Analytics
- 🔄 Real-time Status Updates
- 📈 Revenue Tracking

## Tech Stack
- **Framework**: FastAPI
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT with python-jose
- **Migration**: Alembic
- **API Documentation**: Swagger UI / OpenAPI

## Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd elts-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/elts_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Initialize the database:
```bash
alembic upgrade head
```

## Running the Server

Start the development server:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

### Main Endpoints

#### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration

#### Users
- `GET /api/users/` - List all users
- `GET /api/users/{id}` - Get user details
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

#### Teachers
- `GET /api/teachers/` - List all teachers
- `POST /api/teachers/` - Create new teacher
- `GET /api/teachers/{id}` - Get teacher details
- `PUT /api/teachers/{id}` - Update teacher
- `DELETE /api/teachers/{id}` - Delete teacher

#### Students
- `GET /api/students/` - List all students
- `POST /api/students/` - Create new student
- `GET /api/students/{id}` - Get student details
- `PUT /api/students/{id}` - Update student
- `DELETE /api/students/{id}` - Delete student

#### Courses
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create new course
- `GET /api/courses/{id}` - Get course details
- `PUT /api/courses/{id}` - Update course
- `DELETE /api/courses/{id}` - Delete course

#### Enrollments
- `GET /api/enrollments/` - List all enrollments
- `POST /api/enrollments/` - Create new enrollment
- `GET /api/enrollments/{id}` - Get enrollment details
- `PUT /api/enrollments/{id}` - Update enrollment
- `DELETE /api/enrollments/{id}` - Delete enrollment

#### Dashboard
- `GET /api/dashboard/stats/` - Get dashboard statistics

## Data Population

To populate the database with sample data:
```bash
cd scripts
python populate_data.py
```

## Development

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Testing

Run tests:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
