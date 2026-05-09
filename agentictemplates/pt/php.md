# PHP

## Comandos

- Executar: `php -S localhost:8000`
- Testar: `php artisan test` or `./vendor/bin/phpunit`
- Linter: `./vendor/bin/pint` or `php -l`
- Formatar: `./vendor/bin/pint`

## Estilo de Código

- Follow PSR-12 coding style
- Use type hints for function parameters and return types
- Use strict types (`declare(strict_types=1)`)
- Use dependency injection over static methods
- Use meaningful namespace conventions

## Melhores Práticas

- Use Composer for dependency management
- Use PSR-4 autoloading
- Use environment variables for configuration
- Sanitize all user input
- Use prepared statements for database queries
- Write unit and feature tests with PHPUnit
