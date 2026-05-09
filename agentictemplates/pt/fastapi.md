# FastAPI

## Comandos

- Executar: `uvicorn app.main:app --reload`
- Testar: `pytest`
- Linter: `ruff check .`
- Formatar: `ruff format .`

## Estilo de Código

- Use Pydantic models for request/response validation
- Use dependency injection for shared logic
- Keep route handlers thin
- Use async endpoints where possible
- Use `Annotated` for dependency injection (FastAPI 0.95+)

## Melhores Práticas

- Structure the app with routers, schemas, services, and models
- Use `BackgroundTasks` for non-critical async work
- Configure CORS explicitly for production
- Use `HTTPException` with proper status codes
- Enable OpenAPI docs only in development
- Use `uvicorn` with `--workers` for production
