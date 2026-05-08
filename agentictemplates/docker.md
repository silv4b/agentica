# Docker

## Commands

- Run: `docker compose up`
- Build: `docker compose build`
- Down: `docker compose down`
- Logs: `docker compose logs -f`

## Best Practices

- Use multi-stage builds to keep images small
- Use `.dockerignore` to exclude unnecessary files
- Pin base image versions (avoid `:latest`)
- Use `COPY --chown` for proper file ownership
- Use health checks in Docker Compose
- Keep each container focused on a single concern
- Use Docker volumes for persistent data in development
