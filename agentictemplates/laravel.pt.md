# Laravel

## Comandos

- Executar: `php artisan serve`
- Testar: `php artisan test`
- Linter: `./vendor/bin/pint`
- Tinker: `php artisan tinker`

## Estilo de Código

- Use Eloquent ORM for database interactions
- Keep business logic in services or actions
- Use Form Requests for validation
- Follow PSR standards (PSR-2, PSR-4, PSR-12)

## Melhores Práticas

- Use `Route::resource` for RESTful controllers
- Use Eloquent `scope` methods for query filters
- Use `events` and `listeners` for decoupled logic
- Use `queues` for heavy or slow tasks
- Use `Laravel Debugbar` and `Clockwork` for local debugging
- Use `env()` only in config files — use config helpers elsewhere
- Write feature tests for critical paths
