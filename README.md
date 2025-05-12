# miran

👋 Miran is an AI-powered fitness app that offers smart meal tracking, real-time workout  guidance using computer vision, and engaging fitness challenges. Users can log meals easily, get instant feedback on exercise form, and stay motivated through leaderboards and rewards.

## Development Setup

### Prerequisites
- Python 3.12+
- Postgresql 16+
- Docker and Docker Compose (optional, but recommended)
- Git
- Make (optional, but recommended)

### First Time Setup

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
- Redis Commander: http://localhost:8081
- MailHog (email testing): http://localhost:8025
- PostgreSQL: localhost:5433

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
make test
# or for specific tests:
pytest path/to/test.py -v
```

### Code Quality Tools

This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for code linting
- pre-commit for git hooks

### Contributing

1. Create a new branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

### Troubleshooting

1. **Database Issues**
   ```bash
   make docker-clean  # Reset all containers and volumes
   make up           # Start fresh
   ```

2. **Permission Issues**
   ```bash
   sudo chown -R $USER:$USER .  # Fix ownership
   ```

### Additional Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [Docker Documentation](https://docs.docker.com/)
