# Ruby on Rails

## Comandos

- Executar: `bin/rails server`
- Testar: `bin/rails test`
- Linter: `rubocop`
- Console: `bin/rails console`

## Estilo de Código

- Follow Rails conventions and "Convention over Configuration"
- Use skinny controllers, fat models (or service objects)
- Use partials and helpers for view logic
- Write comprehensive tests (unit, integration, system)

## Melhores Práticas

- Use `scopes` for common queries
- Use `ActiveRecord` callbacks judiciously
- Use `strong_parameters` for mass assignment protection
- Use `I18n` for internationalization
- Use `credentials` for secrets management
- Use `background_jobs` (Sidekiq) for async tasks
- Follow Rails API mode for JSON-only apps
