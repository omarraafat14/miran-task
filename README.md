# Miran Product Search API

A robust, multilingual product search API designed for the Miran fitness app, built with Django and PostgreSQL.
It supports fuzzy matching, and advanced filtering to deliver high-quality, relevant results.


## 🚀 Features

### 🔍 Advanced Search

- Full-text search in both **English** and **Arabic**
- **Fuzzy matching** for partial queries and misspellings (e.g. `"protien"` → `"protein"`)
- Configurable **similarity threshold** via environment variables
- Weighted fields for relevance tuning (e.g. `name` > `description`)

### ⚡ Performance Optimizations

- PostgreSQL **GIN-indexed** search vectors
- Fast lookups using **Redis** and Django's caching framework
- Efficient query planning and low DB overhead



## 🔎 API Usage

### Basic Search

```
GET /api/products/?search=protein
```

### Advanced Filters

```
GET /api/products/?search=protein&category=supplements&price_min=20&price_max=50
```

### Python Example

```python
import requests

response = requests.get(
    "http://localhost:8000/api/products/",
    params={"search": "protein", "category": "supplements", "price_min": 20}
)
results = response.json()
```

### Security & Rate Limiting

- To prevent abuse and ensure fair usage, the API uses Django REST Framework's throttling system:

```python
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "30/min",
        "user": "60/min",
    },
}
```
- Anonymous users: 5 requests per minute
- Authenticated users: 10 requests per minute

If you exceed the limit, the API responds with:

```json
{
  "detail": "Request was throttled. Expected available in x seconds."
}
```



## 🛠️ Development Setup

### Prerequisites
- Python 3.9+
- Postgresql 16+
- Docker and Docker Compose (optional, but recommended)
- Git
- Make (optional, but recommended)

### First Time Setup

0. **Clone the repository**
```bash
git clone https://github.com/miran/miran-backend.git
cd miran-backend
```

1. **Create and activate virtual environment**
```bash
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements/local.txt
```

3. **Set up pre-commit hooks**
```bash
pre-commit install
pre-commit run --all-files
```

4. **Set up environment variables**
```bash
cp .docker.env.example .docker.env  # Copy example env file
cp .env.example .env  # Copy example env file
# Edit .docker.env with your settings
```

5. **Start Docker services**
```bash
make up  # or: docker compose -f local.yml up -d
```

6. **Run migrations and create superuser**
```bash
make migrations
make migrate
make superuser  # Creates superuser with admin@example.com/admin
```

### Development Commands

**Docker Commands:**
```bash
make up           # Start all services
make down         # Stop all services
make logs         # View logs
make shell-web    # Access web container shell
make shell-db     # Access database shell
```

**Django Commands:**
```bash
make migrations   # Create new migrations
make migrate      # Apply migrations
make superuser    # Create superuser
make shell       # Django shell
make test        # Run tests
```

**Code Quality:**
```bash
make lint        # Run linting checks
make format      # Format code
```

### Available Services

- Django web: http://localhost:8000
- PostgreSQL: localhost:5433
- Redis: localhost:6379
- Redis Commander: http://localhost:8081
- MailHog (email testing): http://localhost:8025
- Celery
- Flower (celery monitor): http://localhost:5555

### Production Deployment

To run Django commands in production:
```bash
export DJANGO_SETTINGS_MODULE=miran.settings.production
python manage.py <command>
```

### Project Structure
```
├── compose/             # Docker compose files
├── miran/              # Django settings
├── requirements/        # Project dependencies
│   ├── base.txt        # Base requirements
│   ├── local.txt       # Development requirements
│   └── production.txt  # Production requirements
└── manage.py           # Django management script
```

### Testing

Run tests with:
```bash
python manage.py test
```

### Code Quality Tools

This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for code linting
- pre-commit for git hooks
