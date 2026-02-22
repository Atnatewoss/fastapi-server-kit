# FastAPI Server Kit

A production-grade FastAPI template and toolkit with support for PostgreSQL (Sync/Async), SQLite (Async), and MySQL (Async). Built for speed, scalability, and clean architecture.

## Features

- **Multi-Database Support**: Easily switch between SQLite, PostgreSQL, and MySQL.
- **SQLAlchemy 2.0 (Async)**: Modern ORM patterns with centralized session management.
- **Clean Architecture**: Organized into Core, Models, Repositories, Services, and Routers.
- **Alembic Migrations**: Ready-to-use async migration setup.
- **Environment Management**: Robust configuration using `pydantic-settings`.

## Installation & Quick Start

The easiest way to start a new project is to use `uvx`. No installation or pre-existing project is required.

```bash
# In an empty directory, run:
uvx fastapi-server-kit
```

This single command will trigger an **interactive setup**:
1.  **Project Name**: Choose your own folder name.
2.  **Database Selection**: Choose between **SQLite**, **PostgreSQL**, or **MySQL**.
3.  **Auto-Initialization**: The tool runs `uv sync` to set up your `.venv`.
4.  **Instant Start**: The FastAPI server launches immediately.

### CLI Flags (Automation)
For non-interactive use or CI/CD:
```bash
uvx fastapi-server-kit my-app --db postgres --no-input
```

### Alternative Installation
If you want to add the kit as a dependency to an existing project:

```bash
uv add fastapi-server-kit
```

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
uv run uvicorn app.main:app --reload
```

## Project Structure

The kit follows a clean, modular directory layout:

```text
server/
├── app/
│   ├── core/          # Configuration and security
│   ├── models/        # SQLAlchemy models
│   ├── repositories/  # Data access layer
│   ├── routers/       # API endpoints
│   ├── schemas/       # Pydantic models
│   └── services/      # Business logic
├── tests/             # Unit and integration tests
├── cli.py             # Scaffolding CLI logic
└── pyproject.toml     # Project dependencies
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
