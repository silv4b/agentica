# PHP

## Commands

- Run: `php -S localhost:8000`
- Test: `php artisan test` or `./vendor/bin/phpunit`
- Lint: `./vendor/bin/pint` or `php -l`
- Format: `./vendor/bin/pint`

## Code Style

- Follow PSR-12 coding style
- Use type hints for function parameters and return types
- Use strict types (`declare(strict_types=1)`)
- Use dependency injection over static methods
- Use meaningful namespace conventions

## Best Practices

- Use Composer for dependency management
- Use PSR-4 autoloading
- Use environment variables for configuration
- Sanitize all user input
- Use prepared statements for database queries
- Write unit and feature tests with PHPUnit
