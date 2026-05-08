# Java

## Commands

- Build: `./mvnw clean package` or `./gradlew build`
- Run: `./mvnw exec:java` or `./gradlew run`
- Test: `./mvnw test` or `./gradlew test`
- Format: `./mvnw spotless:apply`

## Code Style

- Follow Oracle / Google Java Style Guide
- Use meaningful package names (`com.project.module`)
- Use interfaces for abstraction
- Use `var` only when type is obvious from context
- Use records (Java 16+) for immutable data carriers

## Best Practices

- Use Optional over null returns
- Use streams and lambdas for collection operations
- Use try-with-resources for auto-closable resources
- Use SLF4J with Logback for logging
- Write unit tests with JUnit 5 and Mockito
- Use Builder pattern for complex object construction
- Keep methods short and focused
