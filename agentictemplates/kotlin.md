# Kotlin

## Commands

- Run: `./gradlew run`
- Test: `./gradlew test`
- Lint: `./gradlew ktlintCheck`

## Code Style

- Use nullable types explicitly with `?`
- Prefer `val` over `var`
- Use data classes for models
- Use extension functions for utility methods
- Use Kotlin's stdlib functions (`let`, `apply`, `run`, `with`)

## Best Practices

- Use coroutines for async operations
- Use `sealed class` / `sealed interface` for sealed hierarchies
- Use `object` for singletons
- Use `companion object` for static members
- Use Flow for reactive streams
- Enable `strictMode` in Kotlin compiler
