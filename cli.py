import os
import shutil
import sys
from pathlib import Path

def main():
    """
    Scaffolds a new FastAPI Server Kit project by copying the template files
    to a new 'server' directory in the current working directory.
    """
    package_dir = Path(__file__).parent
    dest = Path.cwd() / "server"

    if dest.exists():
        print(f"Error: Directory 'server' already exists at {dest}")
        sys.exit(1)

    # List of files/dirs to copy
    to_copy = ["app", "tests", ".env_example", "README.md", "pyproject.toml"]

    try:
        print(f"Scaffolding FastAPI Server Kit into {dest}...")
        dest.mkdir(parents=True, exist_ok=True)
        
        for item in to_copy:
            src_path = package_dir / item
            if not src_path.exists():
                print(f"Warning: {item} not found in package.")
                continue
            
            if src_path.is_dir():
                shutil.copytree(src_path, dest / item)
            else:
                shutil.copy2(src_path, dest / item)

        print("\nSuccess! Your server template is ready.")
        print("\nTo get started:")
        print("  cd server")
        print("  uv sync")
        print("  uv run uvicorn app.main:app --reload")
    except Exception as e:
        print(f"Error during scaffolding: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
