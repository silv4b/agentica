# Python

## Comandos

- Executar: `python manage.py runserver` or `python main.py`
- Testar: `pytest`
- Linter: `ruff check .`
- Formatar: `ruff format .`
- Verificação de tipos: `mypy .`

## Estilo de Código

- Follow PEP 8
- Use type hints for all public functions and methods
- Prefer async where applicable
- Use f-strings for formatting
- Use pathlib over `os.path`

## Melhores Práticas

- Keep business logic out of views/controllers
- Use dependency injection for testability
- Prefer composition over inheritance
- Use dataclasses or Pydantic for data containers
- Handle exceptions at the appropriate layer
- Use context managers (`with` statement) for resource management
