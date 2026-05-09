# Go

## Comandos

- Executar: `go run .`
- Testar: `go test ./...`
- Linter: `golangci-lint run`
- Build: `go build ./...`
- Formatar: `gofmt -s -w .`

## Estilo de Código

- Follow Go idioms and conventions
- Use interfaces for abstraction (keep them small)
- Handle errors explicitly — never ignore them
- Use `gofmt` / `goimports` for formatting
- Use meaningful package names

## Melhores Práticas

- Use `context.Context` for cancellation and timeouts
- Use `errgroup` for concurrent operations
- Write table-driven tests
- Use `sync` package carefully (prefer channels)
- Structure apps following standard-layout or clean architecture
- Use `go mod` for dependency management
