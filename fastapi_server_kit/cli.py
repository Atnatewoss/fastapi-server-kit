import os
import shutil
import sys
import subprocess
import argparse
from pathlib import Path

try:
    import questionary
except ImportError:
    questionary = None

def run_command(command, cwd=None):
    """Utility to run a command and handle errors."""
    try:
        # Using shell=True for windows compatibility with uv
        subprocess.run(command, cwd=cwd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error executing command: {' '.join(command)}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"\n❌ Error: Command '{command[0]}' not found. Is it installed?")
        sys.exit(1)

def main():
    """
    Scaffolds a new FastAPI Server Kit project with interactive prompts,
    industry-standard automated setup, and immediate server start.
    """
    parser = argparse.ArgumentParser(description="Scaffold a new FastAPI Server Kit project.")
    parser.add_argument("name", nargs="?", help="Project name")
    parser.add_argument("--db", choices=["sqlite", "postgres", "mysql"], help="Database type")
    parser.add_argument("--no-input", action="store_true", help="Skip interactive prompts")
    parser.add_argument("--no-run", action="store_true", help="Do not start the server after scaffolding")
    args = parser.parse_args()

    # ASCII Banner
    print("\n" + "="*50)
    print("🚀 Welcome to FastAPI Server Kit")
    print("="*50 + "\n")

    package_dir = Path(__file__).parent

    # 1. Project Name Logic
    project_name = args.name
    if not project_name and not args.no_input:
        if questionary:
            project_name = questionary.text(
                "What is your project named?", 
                default="server"
            ).ask()
        else:
            project_name = input("What is your project named? (default: server): ") or "server"
    elif not project_name:
        project_name = "server"

    if not project_name:
        print("❌ Project name cannot be empty.")
        sys.exit(1)

    dest = Path.cwd() / project_name

    if dest.exists():
        print(f"\n❌ Error: Directory '{project_name}' already exists at {dest}")
        sys.exit(1)

    # 2. Database Selection Logic
    db_choice_type = args.db
    if not db_choice_type and not args.no_input:
        if questionary:
            db_choice_label = questionary.select(
                "Which database would you like to use?",
                choices=["SQLite", "PostgreSQL", "MySQL"]
            ).ask()
            db_choice_type = {"SQLite": "sqlite", "PostgreSQL": "postgres", "MySQL": "mysql"}.get(db_choice_label)
        else:
            print("\nChoose a database:")
            print("1) SQLite")
            print("2) PostgreSQL")
            print("3) MySQL")
            choice = input("Choice (1-3) [default 1]: ") or "1"
            db_choice_type = {"1": "sqlite", "2": "postgres", "3": "mysql"}.get(choice, "sqlite")
    elif not db_choice_type:
        db_choice_type = "sqlite"

    # Mapping types to URLs
    db_urls = {
        "sqlite": "sqlite+aiosqlite:///./test.db",
        "postgres": "postgresql+asyncpg://user:password@localhost:5432/dbname",
        "mysql": "mysql+aiomysql://user:password@localhost:3306/dbname"
    }
    db_url = db_urls[db_choice_type]

    # List of files/dirs to copy
    to_copy = ["app", "tests", ".env_example", "pyproject.toml"]

    try:
        print(f"\n🛠️  Scaffolding {project_name} into {dest}...")
        dest.mkdir(parents=True, exist_ok=True)
        
        for item in to_copy:
            # Look for template version of pyproject.toml first
            if item == "pyproject.toml":
                src_path = package_dir / "pyproject.toml.template"
                if not src_path.exists():
                    src_path = package_dir / "pyproject.toml"
            else:
                src_path = package_dir / item

            if not src_path.exists():
                print(f"  ⚠️  Warning: {item} not found in package.")
                continue
            
            if src_path.is_dir():
                shutil.copytree(src_path, dest / item)
            else:
                target_name = item
                if src_path.name == "pyproject.toml.template":
                    target_name = "pyproject.toml"
                shutil.copy2(src_path, dest / target_name)

        # Generate a project-specific README
        readme_content = f"""# {project_name}

Built with [FastAPI Server Kit](https://pypi.org/project/fastapi-server-kit/).

## Getting Started

```bash
# Install dependencies
uv sync

# Run the development server
uv run uvicorn app.main:app --reload
```

## Project Structure

```text
{project_name}/
├── app/
│   ├── core/          # Configuration and security
│   ├── models/        # SQLAlchemy models
│   ├── repositories/  # Data access layer
│   ├── routers/       # API endpoints
│   ├── schemas/       # Pydantic models
│   └── services/      # Business logic
└── tests/             # Unit and integration tests
```
"""
        with open(dest / "README.md", "w") as f:
            f.write(readme_content)


        # 3. Configure .env based on DB choice
        env_path = dest / ".env"
        env_content = [
            "# Project Configuration",
            f'PROJECT_NAME="{project_name}"',
            "",
            "# Database Configuration",
            f"DATABASE_TYPE={db_choice_type}",
            f"DATABASE_URL={db_url}",
            ""
        ]
        with open(env_path, "w") as f:
            f.write("\n".join(env_content))

        # 4. Update project name in pyproject.toml
        pyproject_path = dest / "pyproject.toml"
        if pyproject_path.exists():
            content = pyproject_path.read_text()
            new_content = content.replace('name = "server"', f'name = "{project_name}"')
            pyproject_path.write_text(new_content)

        print(f"\n✨ Success! Your server template is ready at {dest}")
        
        # 5. Initialize environment (like npm install)
        print("\n📦 Initializing environment with uv sync...")
        run_command(["uv", "sync"], cwd=dest)
        
        print("\n" + "="*50)
        print("✅ ENVIRONMENT READY & ACTIVATED")
        print("="*50)
        if sys.platform == "win32":
            print(f"To manually activate this shell in the future:")
            print(f"  cd {project_name}; .\\.venv\\Scripts\\activate")
        else:
            print(f"To manually activate this shell in the future:")
            print(f"  cd {project_name} && source .venv/bin/activate")
        print("="*50)

        if not args.no_run:
            # 6. Start server (Next.js dev server style)
            print("\n🚀 Starting FastAPI server...")
            run_command(["uv", "run", "uvicorn", "app.main:app", "--reload"], cwd=dest)
        else:
            print("\n⏭️  Skipping server start as requested.")

    except Exception as e:
        print(f"\n❌ Error during scaffolding: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Stopped by user.")
        sys.exit(0)
