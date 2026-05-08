# Spring Boot

## Comandos

- Executar: `./mvnw spring-boot:run`
- Testar: `./mvnw test`
- Package: `./mvnw clean package -DskipTests`

## Estilo de Código

- Use constructor injection with `@RequiredArgsConstructor`
- Keep controllers thin — delegate business logic to services
- Use DTOs for API request/response objects
- Follow RESTful naming conventions

## Melhores Práticas

- Use `@Validated` for request validation with Jakarta Validation
- Use `@ControllerAdvice` for global exception handling
- Use Spring Data JPA with `@Query` for custom queries
- Use `@Transactional` at service layer boundaries
- Use `application.yml` with profile-specific configs
- Use `@SpringBootTest` for integration tests
- Enable Actuator for production monitoring
- Use MapStruct for entity-DTO mapping
