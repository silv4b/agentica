# Rust

## Comandos

- Executar: `cargo run`
- Testar: `cargo test`
- Linter: `cargo clippy`
- Build: `cargo build`
- Formatar: `cargo fmt`

## Estilo de Código

- Use the type system to enforce invariants
- Follow Rust naming conventions (snake_case, PascalCase)
- Use pattern matching extensively
- Prefer iterators over manual loops
- Use `Option` and `Result` instead of null/errors

## Melhores Práticas

- Use `cargo add` for dependencies
- Write documentation tests (`///`) for public APIs
- Use `thiserror` and `anyhow` for error handling
- Use `serde` for serialization
- Use `clap` for CLI argument parsing
- Leverage RAII for resource management
