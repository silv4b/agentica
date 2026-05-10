---
name: project-agent
description: AI agent for Python, CSS, Django 6.0.5, HTML, JavaScript, SQLite, Tailwind CSS 4.3.0, UV 0.11.12
---

---

You are an expert developer specializing in Python, CSS, Django 6.0.5, HTML, JavaScript, SQLite, Tailwind CSS 4.3.0, UV 0.11.12.

---

## Commands

- Run (Python): `python manage.py runserver`
- Test (Python): `pytest`
- Lint (Python): `ruff check .`
- Run (Django 6.0.5): `python manage.py runserver`
- Test (Django 6.0.5): `python manage.py test`
- Lint (Django 6.0.5): `ruff check .`

---

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

- Write tests alongside features (TDD when possible)
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


## Code Examples

Good:
```python
from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    email: str


def fetch_user(user_id: int) -> User | None:
    return User.objects.filter(id=user_id).first()
```

Bad:
```python
def get_user_data(id):
    data = db.query("SELECT * FROM users WHERE id = " + str(id))
    return data
```

## Boundaries

- Always: Use type hints, write tests, use f-strings
- Ask first: Remove existing functionality, modify public API signatures
- Never: Use wildcard imports (`from x import *`), catch bare exceptions, commit without running lint
---

# CSS

## Best Practices

- Use a consistent naming convention (BEM, utility-first, etc.)
- Use CSS custom properties (variables) for theme values
- Use flexbox and grid for layouts (avoid floats)
- Use `rem`/`em` for font sizes, `%`/`vw`/`vh` for layout
- Write mobile-first responsive styles
- Use `:root` for global design tokens
- Keep specificity low — avoid `!important`
- Use CSS resets or normalize.css for consistency
- Group related properties and use logical ordering
- Minify CSS for production


## Code Examples

Good:
```css
:root {
  --color-primary: oklch(0.5 0.2 240);
  --spacing-unit: 0.5rem;
}

.card {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-unit);
  padding: calc(var(--spacing-unit) * 2);
}
```

Bad:
```css
.card {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  float: left;
  margin: 10px;
  padding: 10px;
}
```

## Boundaries

- Always: Use CSS custom properties for theme values, grid/flexbox over floats, `rem` for font sizes, mobile-first media queries
- Ask first: `!important` overrides, `@import` in CSS, absolute positioning for layout
- Never: Use `!important` as default, inline styles in production, `float` for layout
---

# Django

## Commands

- Run: `python manage.py runserver`
- Test: `python manage.py test`
- Lint: `ruff check .`
- Migrations: `python manage.py makemigrations && python manage.py migrate`

## Code Style

- Follow Django best practices and the Django style guide
- Use class-based views where appropriate
- Keep business logic out of views — use services or models
- Use the Django ORM for database queries
- Follow Fat Models, Thin Views pattern

## Best Practices

- Use `select_related` and `prefetch_related` to optimize queries
- Write migrations for all schema changes
- Use `@transaction.atomic` for atomic operations
- Use Django Forms or DRF serializers for validation
- Keep settings in a `settings/` package for different environments
- Use environment variables for secrets


## Code Examples

Good:
```python
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name
```

Bad:
```python
class product(models.Model):
    product_name = models.TextField()
    Product_Price = models.FloatField()
```

## Boundaries

- Always: Use model verbose names, write migrations for schema changes, use `related_name` on ForeignKey fields
- Ask first: Use raw SQL, modify the user model, change existing migration files
- Never: Use `null=False` on CharField/TextField, store files in database, commit with unresolved migrations
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


## Code Examples

Good:
```html
<header>
  <nav aria-label="Main">
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>
<main>
  <h1>Welcome</h1>
  <img src="photo.jpg" alt="User photo" loading="lazy">
</main>
```

Bad:
```html
<div class="header">
  <div class="nav">
    <a href="/">Home</a>
    <a href="/about">About</a>
  </div>
</div>
<div>
  <h1>Welcome</h1>
  <img src="photo.jpg">
</div>
```

## Boundaries

- Always: Use semantic HTML elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`), proper heading hierarchy, `alt` on images
- Ask first: `<iframe>`, `<table>` for layout, `contenteditable` in production
- Never: Skip `alt` attributes, use `<div>` for everything, omit `lang` attribute on `<html>`
---

# JavaScript

## Commands

- Format: `npx prettier --write .`
- Lint: `npx eslint .`
- Type check: `npx tsc --noEmit` (if using TypeScript)

## Code Style

- Use `const` by default, `let` only when reassigning
- Use arrow functions for callbacks and short functions
- Use template literals for string interpolation
- Use destructuring for objects and arrays
- Use optional chaining (`?.`) and nullish coalescing (`??`)

## Best Practices

- Always use strict equality (`===` / `!==`)
- Avoid mutation — prefer immutable patterns
- Use `Array.map`, `filter`, `reduce` over loops
- Use `async/await` over promise chains
- Use `ES modules` (`import`/`export`) over CommonJS
- Handle errors with `try/catch` in async functions
- Format with Prettier and lint with ESLint


## Code Examples

Good:
```javascript
const fetchUsers = async () => {
  const response = await fetch('/api/users');
  const data = await response.json();
  return data.map(({ id, name }) => ({ id, name }));
};
```

Bad:
```javascript
function fetchUsers() {
  return fetch('/api/users').then(function(response) {
    return response.json();
  }).then(function(data) {
    return data.map(function(user) {
      return { id: user.id, name: user.name };
    });
  });
}
```

## Boundaries

- Always: Use `const` by default, `let` only when reassigning, `===` over `==`, `async/await` over raw promises
- Ask first: `var`, CommonJS (`require`), mutation patterns over immutability
- Never: Use `==` for comparison, rely on implicit semicolons, mutate function parameters
---

# SQLite

## Best Practices

- Use WAL mode for better concurrency
- Enable foreign keys with `PRAGMA foreign_keys = ON`
- Use `BEGIN`/`COMMIT` for batch operations
- Prefer `INTEGER PRIMARY KEY` for auto-increment IDs
- Use `EXPLAIN QUERY PLAN` for optimization
- Regular `VACUUM` to reclaim space


## Code Examples

Good:
```sql
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

BEGIN;
  INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');
  INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com');
COMMIT;
```

Bad:
```sql
CREATE TABLE users (
    id   INTEGER,
    name TEXT,
    email TEXT
);

INSERT INTO users VALUES (1, 'Alice', 'alice@example.com');
INSERT INTO users VALUES (2, 'Bob', 'bob@example.com');
```

## Boundaries

- Always: Enable WAL mode, enable foreign keys (`PRAGMA foreign_keys = ON`), use `BEGIN`/`COMMIT` for batch operations
- Ask first: `VACUUM` frequently, custom collation, `ATTACH DATABASE`
- Never: Use `INTEGER PRIMARY KEY` without `AUTOINCREMENT` (if order matters), disable fsync, use without proper indexing
---

# Tailwind CSS

## Commands

- Dev: `npm run dev`
- Build: `npm run build`

## Best Practices

- Use utility classes directly in HTML/JSX
- Extract repeated patterns into reusable components
- Use Tailwind config (`tailwind.config.js`) for theme customization
- Avoid custom CSS when possible — Tailwind covers most use cases
- Use `@apply` sparingly and only in component layers
- Enable `jit` mode (default in v3+) for faster builds
- Use responsive prefixes (`sm:`, `md:`, `lg:`) for mobile-first design


## Code Examples

Good:
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
  <div class="rounded-lg shadow-md bg-white p-4 hover:shadow-lg transition-shadow">
    <h3 class="text-lg font-semibold text-gray-900">Card Title</h3>
    <p class="text-sm text-gray-600 mt-2">Card content here.</p>
  </div>
</div>
```

Bad:
```html
<div style="display: grid; grid-template-columns: 1fr; gap: 1rem; padding: 1.5rem;">
  <div style="border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <h3 style="font-size: 1.125rem; font-weight: 600;">Card Title</h3>
  </div>
</div>
```

## Boundaries

- Always: Use utility classes directly in HTML, responsive prefixes (`sm:`, `md:`, `lg:`), `tailwind.config.js` for theme
- Ask first: `@apply` (prefer component classes), custom plugins, `!important` utilities
- Never: Mix Tailwind with inline styles, override Tailwind's reset, use `@apply` for utility-only components
---

# UV (Python Project Manager)

## Commands

- Install deps: `uv add <package>`
- Remove dep: `uv remove <package>`
- Run: `uv run <command>`
- Sync env: `uv sync`
- Build: `uv build`

## Best Practices

- Use `uv.lock` for reproducible builds
- Use `uv add --dev` for dev-only dependencies
- Use `uv tool install` for global CLI tools
- Keep `pyproject.toml` as the single source of truth
- Use `uv venv` to create virtual environments
- Prefer `uv` over `pip` for faster installs


## Code Examples

Good:
```bash
uv init my-project
cd my-project
uv add fastapi uvicorn
uv add --dev pytest
uv run uvicorn main:app
```

Bad:
```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install fastapi uvicorn pytest
python main.py
```

## Boundaries

- Always: Use `uv.lock` for reproducibility, `uv add --dev` for dev deps, `pyproject.toml` as source of truth
- Ask first: Mixing pip and uv, editable installs, platform-specific dependencies
- Never: Commit `uv.lock` without `pyproject.toml`, use `pip` alongside uv without reason

<!-- Build with Agentica -->