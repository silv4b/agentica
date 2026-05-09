# Ruby

## Commands

- Run: `ruby script.rb`
- Test: `ruby -Ilib:test test/test_*.rb`
- Lint: `rubocop`
- Format: `rubocop -A`

## Code Style

- Follow the Ruby Style Guide
- Use 2 spaces for indentation
- Prefer symbols over strings for identifiers
- Use snake_case for methods and variables
- Use `attr_reader`/`attr_accessor` over explicit getters/setters

## Best Practices

- Prefer iterators over `for` loops
- Use `&:method_name` shorthand for block passes
- Use exception handling with `begin`/`rescue`/`ensure`
- Prefer `case`/`when` over multiple `if`/`elsif`
