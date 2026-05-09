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
