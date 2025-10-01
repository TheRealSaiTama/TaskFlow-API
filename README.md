<div align="center">

# 🎯 Kanban Board API

### A Production-Ready RESTful API for Kanban Board Management

[![FastAPI](https://img.shields.io/badge/FastAPI-0.117.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.43-D71F00?style=for-the-badge&logo=databricks&logoColor=white)](https://www.sqlalchemy.org/)
[![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[Features](#-features) • [Tech Stack](#-tech-stack) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Deployment](#-deployment)

</div>

---

## ✨ Features

<table>
  <tr>
    <td>🔐 <b>Secure Authentication</b></td>
    <td>JWT-based authentication with bcrypt password hashing</td>
  </tr>
  <tr>
    <td>📊 <b>Multi-Board Management</b></td>
    <td>Create and manage multiple Kanban boards per user</td>
  </tr>
  <tr>
    <td>📝 <b>Flexible Organization</b></td>
    <td>Organize tasks with customizable columns and cards</td>
  </tr>
  <tr>
    <td>🔒 <b>Data Isolation</b></td>
    <td>User-specific boards with proper access control</td>
  </tr>
  <tr>
    <td>🚀 <b>High Performance</b></td>
    <td>Built on FastAPI with async support</td>
  </tr>
  <tr>
    <td>🐳 <b>Docker Ready</b></td>
    <td>Containerized deployment with production configurations</td>
  </tr>
  <tr>
    <td>🌐 <b>CORS Enabled</b></td>
    <td>Ready for frontend integration</td>
  </tr>
  <tr>
    <td>💾 <b>Dual Database</b></td>
    <td>SQLite for development, PostgreSQL for production</td>
  </tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Client App    │
│  (Frontend)     │
└────────┬────────┘
         │
         │ HTTPS/JWT
         │
┌────────▼────────┐
│   FastAPI       │
│   Application   │
├─────────────────┤
│  • Auth Layer   │
│  • Business     │
│    Logic        │
│  • Validation   │
└────────┬────────┘
         │
         │ ORM (SQLAlchemy)
         │
┌────────▼────────┐
│    Database     │
│  SQLite / PG    │
└─────────────────┘
```

### Data Model

```
User
 └── Boards (1:N)
      └── Columns (1:N)
           └── Cards (1:N)
```

---

## 🛠️ Tech Stack

### Core Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.10+** - Programming language
- **Uvicorn** - Lightning-fast ASGI server

### Database & ORM
- **SQLAlchemy 2.0** - SQL toolkit and ORM
- **SQLite** - Development database
- **PostgreSQL** - Production database (via psycopg2)

### Authentication & Security
- **python-jose** - JWT token generation and validation
- **passlib** - Password hashing with bcrypt
- **python-dotenv** - Environment variable management

### Data Validation
- **Pydantic 2.0** - Data validation using Python type annotations

### Deployment
- **Docker** - Containerization
- **Vercel** - Cloud deployment platform

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/todo-api.git
   cd todo-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create a .env file in the root directory
   echo "SECRET_KEY=your-secret-key-here" > .env
   echo "ENVIRONMENT=development" >> .env
   ```

   Generate a secure secret key:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

---

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build the Docker image
docker build -t kanban-api .

# Run the container
docker run -d -p 8000:8000 --env-file .env kanban-api
```

### Docker Compose (with PostgreSQL)

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: mypguser
      POSTGRES_PASSWORD: newpassword
      POSTGRES_DB: mypgdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db

volumes:
  postgres_data:
```

Run with:
```bash
docker-compose up -d
```

---

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /users/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

#### Login
```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /users/me/
Authorization: Bearer <token>
```

---

### Board Management

#### Create Board
```http
POST /boards
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My Project Board"
}
```

#### Get All Boards
```http
GET /boards/
Authorization: Bearer <token>
```

#### Get Single Board
```http
GET /boards/{board_id}
Authorization: Bearer <token>
```

#### Update Board
```http
PUT /boards/{board_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Board Name"
}
```

#### Delete Board
```http
DELETE /boards/{board_id}
Authorization: Bearer <token>
```

---

### Column Management

#### Create Column
```http
POST /boards/{board_id}/columns/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "To Do"
}
```

#### Get All Columns
```http
GET /boards/{board_id}/columns/
Authorization: Bearer <token>
```

#### Update Column
```http
PUT /columns/{column_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "In Progress"
}
```

#### Delete Column
```http
DELETE /columns/{column_id}
Authorization: Bearer <token>
```

---

### Card Management

#### Create Card
```http
POST /columns/{column_id}/cards/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Task Title",
  "content": "Task description",
  "position": 0
}
```

#### Get All Cards
```http
GET /columns/{column_id}/cards/
Authorization: Bearer <token>
```

#### Update Card
```http
PUT /cards/{card_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated description",
  "position": 1
}
```

#### Delete Card
```http
DELETE /cards/{card_id}
Authorization: Bearer <token>
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required
SECRET_KEY=your-secret-key-here

# Optional
ENVIRONMENT=development  # or 'production'
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database Configuration

The application automatically selects the database based on the `ENVIRONMENT` variable:

- **Development**: SQLite (`todo.db`)
- **Production**: PostgreSQL (`postgresql://mypguser:newpassword@db:5432/mypgdb`)

---

## 📁 Project Structure

```
todo-api/
├── main.py              # Application entry point and route definitions
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for validation
├── auth.py              # Authentication and JWT logic
├── database.py          # Database configuration
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker container configuration
├── .env                # Environment variables (not in repo)
├── todo.db             # SQLite database (development)
└── README.md           # This file
```

---

## 🧪 Testing

### Interactive API Documentation

FastAPI automatically generates interactive API documentation:

1. **Swagger UI**: http://localhost:8000/docs
2. **ReDoc**: http://localhost:8000/redoc

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy"
}
```

---

## 🔒 Security Features

- **Password Hashing**: Bcrypt with automatic salting
- **JWT Tokens**: Secure token-based authentication
- **Password Requirements**: Minimum 8 characters, maximum 72 characters
- **SQL Injection Protection**: SQLAlchemy ORM parameterized queries
- **CORS Configuration**: Configurable allowed origins
- **Cascade Deletion**: Automatic cleanup of related records

---

## 🚀 Deployment

### Vercel Deployment

This project is configured for deployment on Vercel.

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Production Checklist

- [ ] Set strong `SECRET_KEY` in environment variables
- [ ] Configure production database (PostgreSQL)
- [ ] Update CORS origins in `main.py`
- [ ] Set `ENVIRONMENT=production`
- [ ] Enable HTTPS
- [ ] Set up database backups
- [ ] Configure monitoring and logging
- [ ] Review rate limiting (if needed)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The amazing web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - The Python SQL toolkit
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation library

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

Made with ❤️ by TheRealSaitama

</div>

