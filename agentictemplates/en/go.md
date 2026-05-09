# Go

## Commands

- Run: `go run .`
- Test: `go test ./...`
- Lint: `golangci-lint run`
- Build: `go build ./...`
- Format: `gofmt -s -w .`

## Code Style

- Follow Go idioms and conventions
- Use interfaces for abstraction (keep them small)
- Handle errors explicitly — never ignore them
- Use `gofmt` / `goimports` for formatting
- Use meaningful package names

## Best Practices

- Use `context.Context` for cancellation and timeouts
- Use `errgroup` for concurrent operations
- Write table-driven tests
- Use `sync` package carefully (prefer channels)
- Structure apps following standard-layout or clean architecture
- Use `go mod` for dependency management
