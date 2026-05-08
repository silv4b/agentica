# Python

## Commands

- Run: `python manage.py runserver` or `python main.py`
- Test: `pytest`
- Lint: `ruff check .`
- Format: `ruff format .`
- Type check: `mypy .`

## Code Style

- Follow PEP 8
- Use type hints for all public functions and methods
- Prefer async where applicable
- Use f-strings for formatting
- Use pathlib over `os.path`

## Best Practices

- Keep business logic out of views/controllers
- Use dependency injection for testability
- Prefer composition over inheritance
- Use dataclasses or Pydantic for data containers
- Handle exceptions at the appropriate layer
- Use context managers (`with` statement) for resource management
