# UV (Python Project Manager)

## Comandos

- Install deps: `uv add <package>`
- Remove dep: `uv remove <package>`
- Executar: `uv run <command>`
- Sync env: `uv sync`
- Build: `uv build`

## Melhores Práticas

- Use `uv.lock` for reproducible builds
- Use `uv add --dev` for dev-only dependencies
- Use `uv tool install` for global CLI tools
- Keep `pyproject.toml` as the single source of truth
- Use `uv venv` to create virtual environments
- Prefer `uv` over `pip` for faster installs
