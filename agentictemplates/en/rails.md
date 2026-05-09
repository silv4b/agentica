# Ruby on Rails

## Commands

- Run: `bin/rails server`
- Test: `bin/rails test`
- Lint: `rubocop`
- Console: `bin/rails console`

## Code Style

- Follow Rails conventions and "Convention over Configuration"
- Use skinny controllers, fat models (or service objects)
- Use partials and helpers for view logic
- Write comprehensive tests (unit, integration, system)

## Best Practices

- Use `scopes` for common queries
- Use `ActiveRecord` callbacks judiciously
- Use `strong_parameters` for mass assignment protection
- Use `I18n` for internationalization
- Use `credentials` for secrets management
- Use `background_jobs` (Sidekiq) for async tasks
- Follow Rails API mode for JSON-only apps
