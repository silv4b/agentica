<!-- markdownlint-disable MD025 MD024 -->
# General Recommendations

These recommendations apply to any project regardless of technology stack.

## Git

- Write clear, descriptive commit messages in the imperative mood
- Keep commits small and focused on a single concern
- Use feature branches and squash merges for pull requests
- Never commit secrets, credentials, or `.env` files
- Keep `.gitignore` up to date

## Documentation

- Keep a `README.md` with setup, run, and deploy instructions
- Document architecture decisions in an `ADR` or `docs/` folder
- Use docstrings/comments for public APIs and complex logic
- Maintain a `CHANGELOG.md` following keepachangelog.com

## Testing

- Write tests alongside features
- Aim for meaningful coverage, not 100% for its own sake
- Test behavior, not implementation details
- Use realistic fixtures and avoid mocks when integration tests suffice
- Write docstrings in Portuguese for all tests explaining the scenario being tested

## Security

- Validate and sanitize all user input
- Use parameterized queries to prevent injection
- Keep dependencies updated
- Follow the principle of least privilege

## Code Quality

- Keep functions small and single-purpose
- Prefer readability over cleverness
- Avoid deep nesting — early return when possible
- Use meaningful names for variables, functions, and classes
- Eliminate dead code and unused imports

---

# Python

## Commands

- Run: `uv run python manage.py runserver`
- Shell: `uv run python manage.py shell`
- Test: `uv run python manage.py test`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`

## Code Style

- Follow PEP 8
- Use type hints for all public functions and methods
- Use f-strings for formatting
- Use pathlib over `os.path`

## Best Practices

- Keep business logic out of views — use services or models
- Use dataclasses for data containers
- Handle exceptions at the appropriate layer
- Use context managers (`with` statement) for resource management

---

# Django

## Commands

- Run: `uv run python manage.py runserver`
- Test: `uv run python manage.py test`
- Lint: `uv run ruff check .`
- Migrations: `uv run python manage.py makemigrations && uv run python manage.py migrate`
- Check: `uv run python manage.py check`

## Code Style

- Follow Django best practices and the Django style guide
- Use class-based views where appropriate
- Keep business logic out of views — use services or models
- Use the Django ORM for database queries

## Best Practices

- Use `select_related` and `prefetch_related` to optimize queries
- Write migrations for all schema changes
- Use `@transaction.atomic` for atomic operations
- Use Django Forms for validation
- Keep settings in a `settings/` package for different environments
- Use environment variables for secrets

---

# HTML / HTML5

## Best Practices

- Use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`)
- Use proper heading hierarchy (`h1`-`h6`)
- Use `alt` attributes on all images
- Use `label` elements for form inputs
- Use `aria-*` attributes for accessibility
- Validate HTML with W3C Validator
- Keep HTML structure clean and well-indented
- Use `defer` or `async` for script loading
- Use `viewport` meta tag for responsive design
- Avoid inline styles — use CSS classes instead

---

# CSS

## Best Practices

- Use CSS custom properties (variables) for theme values
- Use flexbox and grid for layouts (avoid floats)
- Use `rem`/`em` for font sizes, `%`/`vw`/`vh` for layout
- Write mobile-first responsive styles
- Use `:root` for global design tokens
- Keep specificity low — avoid `!important`
- Group related properties and use logical ordering
- Minify CSS for production

---

# JavaScript

## Commands

- Format: `npx prettier --write .`

## Code Style

- Use `const` by default, `let` only when reassigning
- Use arrow functions for callbacks and short functions
- Use template literals for string interpolation
- Use destructuring for objects and arrays
- Use optional chaining (`?.`) and nullish coalescing (`??`)
- Use `var` only when function-scoping is explicitly needed

## Best Practices

- Always use strict equality (`===` / `!==`)
- Avoid mutation — prefer immutable patterns
- Use `Array.map`, `filter`, `reduce` over loops
- Use `async/await` over promise chains
- Use `ES modules` (`import`/`export`) over CommonJS
- Handle errors with `try/catch` in async functions

---

# UV (Python Project Manager)

## Commands

- Install deps: `uv add <package>`
- Install dev deps: `uv add --dev <package>`
- Remove dep: `uv remove <package>`
- Remove dev dep: `uv remove --dev <package>`
- Run: `uv run <command>`
- Sync env: `uv sync`
- Build: `uv build`

## Best Practices

- Use `uv.lock` for reproducible builds
- Keep `pyproject.toml` as the single source of truth
- Use `uv venv` to create virtual environments
- Prefer `uv` over `pip` for faster installs
