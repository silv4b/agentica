# Spring Framework

## Comandos

- Executar: `./mvnw spring-boot:run`
- Testar: `./mvnw test`
- Build: `./mvnw clean package`

## Estilo de Código

- Use constructor injection (prefer `final` fields with `@RequiredArgsConstructor`)
- Keep controllers thin — delegate to services
- Use records for DTOs (Java 16+)
- Follow RESTful conventions for endpoints

## Melhores Práticas

- Use `@Validated` and `jakarta.validation` for input validation
- Use `@ExceptionHandler` for global error handling
- Use Spring Data JPA with `@Query` for complex queries
- Use `@Transactional` at the service layer
- Use `application.yml` profiles per environment
- Write integration tests with `@SpringBootTest`
