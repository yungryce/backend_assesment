<p align="center">
  <img src="https://img.shields.io/badge/Flask-2.0+-000000?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-red" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/Status-Interview_Project-success" alt="Status">
</p>

<div align="center">
  <h1>📚 Library Management System</h1>
  <p><em>Microservices-based Backend Assessment for Cowrywise</em></p>
</div>

---

## 📋 Table of Contents
- [📖 Overview](#-overview)
- [🎯 Assessment Objectives](#-assessment-objectives)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
- [💡 Usage](#-usage)
- [🏆 Key Features](#-key-features)
- [📚 Resources](#-resources)
- [👥 Contributors](#-contributors)

## 📖 Overview

This Library Management System is a comprehensive backend assessment project developed for Cowrywise's technical interview process. It demonstrates advanced Flask microservices architecture, featuring separate backend and frontend services that communicate through RESTful APIs and webhook notifications.

The system showcases enterprise-grade patterns including service-oriented architecture, database migrations, containerization with Docker, comprehensive testing strategies, and API documentation with Swagger. It implements a complete library ecosystem where administrators can manage books and users can enroll and borrow resources.

**🎯 Assessment Context**: This project was specifically designed to evaluate backend engineering competencies including microservices design, API development, database modeling, testing practices, and DevOps implementation.

## 🎯 Assessment Objectives

Through this project, the following competencies are demonstrated:

- **Microservices Architecture**: Design and implementation of loosely coupled, independently deployable services
- **RESTful API Development**: Creation of well-structured APIs with proper HTTP semantics and error handling
- **Database Design & Migrations**: SQLAlchemy ORM usage with Flask-Migrate for schema versioning
- **Inter-Service Communication**: Webhook-based service integration and data synchronization
- **Containerization**: Docker and Docker Compose for consistent development and deployment environments
- **Testing Strategy**: Comprehensive unit and integration testing with pytest and Flask-Testing
- **API Documentation**: Interactive API documentation using Swagger/OpenAPI specifications
- **Configuration Management**: Environment-based configuration with proper separation of concerns
- **Logging & Monitoring**: Structured logging with JSON format for production-ready observability

## 🛠️ Tech Stack

**Core Technologies:**
- **Flask 2.0+**: Lightweight web framework with Blueprint-based modular architecture
- **Python 3.8+**: Modern Python runtime with type hints and async capabilities
- **SQLAlchemy**: Advanced ORM with relationship mapping and query optimization
- **Flask-Migrate**: Database migration management using Alembic

**Development Tools:**
- **Docker & Docker Compose**: Containerization and orchestration for local development
- **pytest**: Comprehensive testing framework with fixtures and mocking
- **Flasgger**: Swagger/OpenAPI integration for interactive API documentation
- **python-dotenv**: Environment variable management for configuration
- **Gunicorn**: WSGI HTTP server for production deployment

**Database & Storage:**
- **SQLite**: Development database with file-based storage
- **MySQL**: Production-ready relational database support
- **Database Migrations**: Version-controlled schema changes with Flask-Migrate

**DevOps & Monitoring:**
- **JSON Logging**: Structured logging with python-json-logger
- **Requests**: HTTP client library for inter-service communication
- **Flask-Testing**: Specialized testing utilities for Flask applications

## 📁 Project Structure

```
backend_assessment/
├── 🐳 docker-compose.yml          # Multi-service orchestration configuration
├── 📋 requirements.txt            # Python dependencies and versions
├── 📖 README.md                   # Project documentation
├── 🏗️ ARCHITECTURE.md             # System architecture documentation
├── 🎯 SKILLS-INDEX.md             # Learning objectives and skills catalog
├── 👥 AUTHORS.md                  # Contributor information
├── 📄 LICENSE.txt                 # Open source license
├── 🔧 .repo-context.json          # Project metadata schema
├── 🗂️ api/                        # API layer with versioning
│   └── v1/
│       ├── backend/               # Backend service endpoints
│       │   ├── backend_view.py    # Admin API controllers
│       │   └── swagger.yml        # Backend API documentation
│       └── frontend/              # Frontend service endpoints
│           ├── frontend_view.py   # User API controllers
│           └── swagger.yml        # Frontend API documentation
├── 🏗️ backend/                    # Backend microservice
│   ├── app.py                     # Backend Flask application
│   ├── Dockerfile                 # Backend containerization
│   ├── migrations/                # Backend database migrations
│   └── tests/                     # Backend-specific tests
├── 🎨 frontend/                   # Frontend microservice
│   ├── app.py                     # Frontend Flask application
│   ├── Dockerfile                 # Frontend containerization
│   ├── migrations/                # Frontend database migrations
│   └── tests/                     # Frontend-specific tests
├── ⚙️ config/                     # Configuration management
│   ├── base_database.py          # Database initialization
│   ├── config.py                 # Environment configurations
│   └── error_handlers.py         # Global error handling
├── 📊 models/                     # Data layer with ORM
│   ├── base_model.py             # Abstract base model
│   ├── book.py                   # Book entity model
│   └── user.py                   # User entity model
└── 📁 instance/                   # Runtime database files
    ├── backend_library.db
    └── frontend_library.db
```

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Docker & Docker Compose**: For containerized development environment
  - [Install Docker](https://docs.docker.com/get-docker/)
  - [Install Docker Compose](https://docs.docker.com/compose/install/)

- **Python 3.8+**: For local development and testing
  - [Download Python](https://www.python.org/downloads/)
  - Verify: `python --version`

- **Git**: For version control
  - [Install Git](https://git-scm.com/downloads/)

### Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd backend_assessment
   ```

2. **Environment Setup**
   ```bash
   # Create virtual environment (optional for Docker setup)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Database Migration Setup**
   
   **For Backend Service:**
   ```bash
   export FLASK_APP=backend.app
   export APP_ROLE=backend
   flask db init --directory backend/migrations
   flask db migrate --directory backend/migrations
   flask db upgrade --directory backend/migrations
   ```
   
   **For Frontend Service:**
   ```bash
   export FLASK_APP=frontend.app
   export APP_ROLE=frontend
   flask db init --directory frontend/migrations
   flask db migrate --directory frontend/migrations
   flask db upgrade --directory frontend/migrations
   ```

### Running the Project

1. **Build Docker Containers**
   ```bash
   docker-compose build
   ```

2. **Start All Services**
   ```bash
   docker-compose up -d
   ```

3. **Verify Services**
   - Backend API: http://localhost:5000
   - Frontend API: http://localhost:5001
   - Backend Swagger: http://localhost:5000/apidocs
   - Frontend Swagger: http://localhost:5001/apidocs

4. **Run Tests**
   ```bash
   # Backend tests
   docker-compose run backend_tests
   
   # Frontend tests
   docker-compose run frontend_tests
   ```

## 💡 Usage

### API Endpoints Overview

#### Backend Service (Admin Operations) - Port 5000
- **POST** `/api/v1/backend/admin/books/add` - Add new book to library
- **GET** `/api/v1/backend/admin/books` - List all books with filters
- **PUT** `/api/v1/backend/admin/books/{id}` - Update book information
- **DELETE** `/api/v1/backend/admin/books/{id}` - Remove book from library
- **POST** `/api/v1/backend/admin/webhooks/add-user` - Webhook for user enrollment

#### Frontend Service (User Operations) - Port 5001
- **POST** `/api/v1/frontend/enroll` - User registration
- **GET** `/api/v1/frontend/books` - Browse available books
- **POST** `/api/v1/frontend/books/borrow` - Borrow a book
- **POST** `/api/v1/frontend/books/return` - Return borrowed book
- **GET** `/api/v1/frontend/users/{id}/books` - View user's borrowed books

### Example API Usage

#### User Enrollment
```bash
curl -X POST http://localhost:5001/api/v1/frontend/enroll \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "firstname": "John",
    "lastname": "Doe"
  }'
```

#### Add New Book (Admin)
```bash
curl -X POST http://localhost:5000/api/v1/backend/admin/books/add \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Clean Code",
    "publisher": "Prentice Hall",
    "category": "Technology"
  }'
```

#### Borrow Book
```bash
curl -X POST http://localhost:5001/api/v1/frontend/books/borrow \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "book_id": 1
  }'
```

### Inter-Service Communication

The system demonstrates webhook-based communication:

1. **User Enrollment Flow**: Frontend service registers user and notifies backend via webhook
2. **Book Addition Flow**: Backend service adds book and can notify frontend of inventory changes
3. **Data Synchronization**: Both services maintain synchronized user and book information

## 🏆 Key Features

### 🏗️ **Microservices Architecture**
- Independent backend and frontend services
- Service-specific databases with data synchronization
- RESTful API design with proper HTTP semantics
- Webhook-based inter-service communication

### 📊 **Advanced Database Design**
- SQLAlchemy ORM with relationship mapping
- Database migrations with Flask-Migrate
- Multi-database support (SQLite for dev, MySQL for production)
- Optimized queries with lazy loading and relationship management

### 🐳 **Containerization & DevOps**
- Docker containerization for both services
- Docker Compose orchestration with networking
- Separate test containers for isolated testing
- Environment-specific configuration management

### 🧪 **Comprehensive Testing**
- Unit tests with pytest framework
- Integration tests for API endpoints
- Mocking for external dependencies
- Test containers for isolated testing environment

### 📚 **API Documentation**
- Interactive Swagger/OpenAPI documentation
- Service-specific API specifications
- Request/response examples and schemas
- Built-in API testing interface

### 🔍 **Monitoring & Observability**
- Structured JSON logging for production
- Request/response logging middleware
- Error tracking and handling
- Health check endpoints for monitoring

### 🔒 **Security & Best Practices**
- Input validation and sanitization
- SQL injection prevention with parameterized queries
- Error handling without information leakage
- Environment-based configuration management

## 📚 Resources

### Documentation
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detailed system architecture and design patterns
- [SKILLS-INDEX.md](./SKILLS-INDEX.md) - Comprehensive skills catalog and learning outcomes
- [API Documentation](http://localhost:5000/apidocs) - Interactive Swagger documentation

### Flask Framework Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy Guide](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Flasgger (Swagger) Documentation](https://github.com/flasgger/flasgger)

### Testing Resources
- [pytest Documentation](https://docs.pytest.org/)
- [Flask-Testing Guide](https://flask-testing.readthedocs.io/)
- [requests-mock Documentation](https://requests-mock.readthedocs.io/)

### DevOps Resources
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Python Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 👥 Contributors

**Assessment Candidate**: Chigbu Joshua  
**Role**: Backend Engineer Candidate  
**Company**: Cowrywise Technical Assessment  
**Assessment Period**: 2024

### Assessment Context
This project was developed as part of Cowrywise's backend engineering interview process, demonstrating:
- **Technical Proficiency**: Advanced Flask development and microservices architecture
- **System Design**: End-to-end library management system with proper separation of concerns
- **Best Practices**: Industry-standard development practices including testing, documentation, and containerization
- **Problem Solving**: Creative solutions for inter-service communication and data synchronization

### Key Achievements
- **Microservices Implementation**: Successfully designed and implemented loosely coupled services
- **Database Architecture**: Created efficient data models with proper relationships and migrations
- **API Design**: Developed RESTful APIs following OpenAPI specifications
- **Testing Strategy**: Achieved comprehensive test coverage with unit and integration tests
- **DevOps Integration**: Implemented containerization with Docker Compose orchestration

---

<div align="center">
  <p><em>🚀 Developed for Cowrywise Backend Engineering Assessment</em></p>
  <p>Demonstrating enterprise-grade Flask microservices architecture and best practices</p>
</div>