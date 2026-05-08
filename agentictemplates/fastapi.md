# FastAPI

## Commands

- Run: `uvicorn app.main:app --reload`
- Test: `pytest`
- Lint: `ruff check .`
- Format: `ruff format .`

## Code Style

- Use Pydantic models for request/response validation
- Use dependency injection for shared logic
- Keep route handlers thin
- Use async endpoints where possible
- Use `Annotated` for dependency injection (FastAPI 0.95+)

## Best Practices

- Structure the app with routers, schemas, services, and models
- Use `BackgroundTasks` for non-critical async work
- Configure CORS explicitly for production
- Use `HTTPException` with proper status codes
- Enable OpenAPI docs only in development
- Use `uvicorn` with `--workers` for production
