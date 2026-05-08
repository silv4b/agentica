# Spring Boot

## Commands

- Run: `./mvnw spring-boot:run`
- Test: `./mvnw test`
- Package: `./mvnw clean package -DskipTests`

## Code Style

- Use constructor injection with `@RequiredArgsConstructor`
- Keep controllers thin — delegate business logic to services
- Use DTOs for API request/response objects
- Follow RESTful naming conventions

## Best Practices

- Use `@Validated` for request validation with Jakarta Validation
- Use `@ControllerAdvice` for global exception handling
- Use Spring Data JPA with `@Query` for custom queries
- Use `@Transactional` at service layer boundaries
- Use `application.yml` with profile-specific configs
- Use `@SpringBootTest` for integration tests
- Enable Actuator for production monitoring
- Use MapStruct for entity-DTO mapping
