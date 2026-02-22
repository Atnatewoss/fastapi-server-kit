# FastAPI Server Kit

A production-grade FastAPI template and toolkit with support for PostgreSQL (Sync/Async), SQLite (Async), and MySQL (Async). Built for speed, scalability, and clean architecture.

## Features

- **Multi-Database Support**: Easily switch between SQLite, PostgreSQL, and MySQL.
- **SQLAlchemy 2.0 (Async)**: Modern ORM patterns with centralized session management.
- **Clean Architecture**: Organized into Core, Models, Repositories, Services, and Routers.
- **Alembic Migrations**: Ready-to-use async migration setup.
- **Environment Management**: Robust configuration using `pydantic-settings`.

## Installation

You can install `fastapi-server-kit` using `uv` (recommended) or `pip`:

```bash
uv add fastapi-server-kit
# or
pip install fastapi-server-kit
```

## Quick Start (CLI)

The easiest way to start a new project is to use the built-in CLI tool:

```bash
# Initialize a new server folder in your current directory
fastapi-server-kit
```

This will create a `server/` directory with the complete production-ready structure.

## Manual Setup
If you prefer to clone the repository or use it as a template:

```bash
git clone https://github.com/atnatewoshw/fastapi-starter-template
cd fastapi-starter-template/server
```

### 2. Configure Environment
Create and configure your `.env` file from `.env_example`:

```bash
cp .env_example .env
```

### 3. Install Dependencies
```bash
uv sync
```

### 4. Running Locally
```bash
uv run uvicorn fastapi_server_kit.server.app.main:app --reload
```

## Project Structure

The kit follows a structured directory layout within the `server` package:

```text
fastapi_server_kit/
└── server/
    └── app/
        ├── core/          # Configuration and security
        ├── models/        # SQLAlchemy models
        ├── repositories/  # Data access layer
        ├── routers/       # API endpoints
        ├── schemas/       # Pydantic models
        └── services/      # Business logic
```

## Database Migrations

Initialize your database:
```bash
uv run alembic upgrade head
```

Create a new migration:
```bash
uv run alembic revision --autogenerate -m "description"
```

## License

This project is licensed under the MIT License.
