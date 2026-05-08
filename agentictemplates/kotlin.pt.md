# Kotlin

## Comandos

- Executar: `./gradlew run`
- Testar: `./gradlew test`
- Linter: `./gradlew ktlintCheck`

## Estilo de Código

- Use nullable types explicitly with `?`
- Prefer `val` over `var`
- Use data classes for models
- Use extension functions for utility methods
- Use Kotlin's stdlib functions (`let`, `apply`, `run`, `with`)

## Melhores Práticas

- Use coroutines for async operations
- Use `sealed class` / `sealed interface` for sealed hierarchies
- Use `object` for singletons
- Use `companion object` for static members
- Use Flow for reactive streams
- Enable `strictMode` in Kotlin compiler
