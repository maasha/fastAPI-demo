# FastAPI Demo

A full-stack analytics platform demonstrating modern web technologies for data management and visualization. This project showcases the integration of Python-based backend services with interactive data visualization dashboards.

## Purpose

This project demonstrates:
- RESTful API design with FastAPI
- Database management with PostgreSQL and SQLAlchemy ORM
- Interactive data visualization with R-Shiny
- Containerization with Docker
- Test-driven development with pytest
- Professional project structure and best practices

The platform provides a complete CRUD (Create, Read, Update, Delete) API for user management with real-time data visualization capabilities.

## Tech Stack

### Backend
- **FastAPI** - Modern, high-performance Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **PostgreSQL** - Relational database

### Frontend
- **R-Shiny** - Interactive web application framework for R
- **ggplot2** - Data visualization library
- **httr** - HTTP client for API communication

### DevOps & Infrastructure
- **Docker & Docker Compose** - Containerization
- **pytest** - Testing framework
- **GitHub Actions** - CI/CD (configuration ready)

### Development Tools
- **Python 3.9+**
- **R 4.5+**
- **uvicorn** - ASGI server

## Project Structure

```
demo/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py            # API endpoints and application
│   │   ├── models.py          # Pydantic data models
│   │   ├── db_models.py       # SQLAlchemy ORM models
│   │   └── database.py        # Database configuration
│   ├── tests/                 # Unit tests
│   │   ├── conftest.py        # Test fixtures
│   │   └── test_api.py        # API endpoint tests
│   ├── requirements.txt       # Python dependencies
│   └── pytest.ini             # Pytest configuration
├── frontend/
│   └── dashboard/             # R-Shiny dashboard
│       └── app.R              # Shiny application
├── docker-compose.yml         # Docker services configuration
├── .gitignore
└── README.md
```

## Installation

### Prerequisites

- **Python 3.9+** installed
- **R 4.5+** installed
- **Docker Desktop** installed and running
- **Git** (for cloning the repository)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd demo
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 3. Install Python Dependencies

```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Install development/testing dependencies (optional)
pip install -r backend/requirements-dev.txt
```

### 4. Install R Packages

```bash
# Open R or use Rscript
Rscript -e "install.packages(c('shiny', 'httr', 'jsonlite', 'ggplot2'), repos='https://cloud.r-project.org/')"
```

## Running the Application

### Step 1: Start PostgreSQL Database

Start the PostgreSQL database using Docker Compose:

```bash
docker-compose up -d
```

Verify the database is running:

```bash
docker ps | grep postgres
```

You should see the `demo_postgres` container running on port 5432.

### Step 2: Start FastAPI Backend

In a new terminal window:

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source ../venv/bin/activate

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API:** http://localhost:8000
- **Interactive API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative API Documentation (ReDoc):** http://localhost:8000/redoc

### Step 3: Start R-Shiny Dashboard

In another terminal window:

```bash
# Navigate to dashboard directory
cd frontend/dashboard

# Start Shiny app
Rscript -e "shiny::runApp(port=3838, host='0.0.0.0')"
```

The dashboard will be available at:
- **Dashboard:** http://localhost:3838

## Using the Application

### 1. Create Users via API

Visit http://localhost:8000/docs and use the **POST /users** endpoint to create users:

```json
{
  "name": "Alice Johnson",
  "age": 28,
  "address": "123 Main Street, Boston"
}
```

### 2. View Data in Dashboard

- Navigate to http://localhost:3838
- Click **"Refresh Data"** to fetch users from the API
- View the pie chart showing age distribution
- See the user data table below

### 3. API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /about` - API information
- `POST /users` - Create a new user
- `GET /users` - Get all users
- `GET /users/{id}` - Get a specific user
- `PUT /users/{id}` - Update a user
- `DELETE /users/{id}` - Delete a user

## Running Tests

The project includes comprehensive unit tests with 96% code coverage.

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source ../venv/bin/activate

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_api.py
```

## Stopping the Application

### Stop FastAPI and R-Shiny
Press `Ctrl+C` in their respective terminal windows.

### Stop PostgreSQL Database

```bash
docker-compose down
```

To stop and remove all data:

```bash
docker-compose down -v
```

## Development

### Database Migrations

The database tables are automatically created on application startup. To reset the database:

```bash
# Stop the application
docker-compose down -v

# Restart
docker-compose up -d
```

### Environment Variables

You can customize database credentials by modifying `docker-compose.yml`:

```yaml
environment:
  POSTGRES_USER: demo_user
  POSTGRES_PASSWORD: demo_password
  POSTGRES_DB: demo_db
```

## Troubleshooting

### PostgreSQL Connection Issues

If the FastAPI backend can't connect to PostgreSQL:

1. Ensure Docker Desktop is running
2. Verify PostgreSQL container is running: `docker ps`
3. Check logs: `docker logs demo_postgres`

### Port Already in Use

If ports 8000, 3838, or 5432 are already in use:

1. Stop other applications using those ports
2. Or modify the port numbers in the respective commands/configuration files

### R-Shiny Dashboard Shows No Data

1. Ensure FastAPI backend is running on port 8000
2. Create users via the API first (http://localhost:8000/docs)
3. Click "Refresh Data" button in the dashboard

## Architecture

The application follows a three-tier architecture:

1. **Presentation Layer:** R-Shiny dashboard for data visualization
2. **Application Layer:** FastAPI REST API for business logic
3. **Data Layer:** PostgreSQL database for persistent storage

**Data Flow:**
```
User → R-Shiny Dashboard → FastAPI API → PostgreSQL Database
```

## Features

- ✅ RESTful API with full CRUD operations
- ✅ Data validation with Pydantic
- ✅ ORM with SQLAlchemy
- ✅ Containerized PostgreSQL database
- ✅ Interactive data visualization
- ✅ Real-time data refresh
- ✅ Automatic API documentation
- ✅ Comprehensive test suite (96% coverage)
- ✅ CORS enabled for cross-origin requests

## License

This is a demonstration project for educational purposes.

## Contact

For questions or feedback, please reach out to the project maintainer.

