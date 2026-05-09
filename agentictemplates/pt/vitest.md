# Vitest

## Comandos

- Testar: `npx vitest` ou `npm run test`
- Modo watch: `npx vitest`
- Cobertura: `npx vitest --coverage`
- Modo UI: `npx vitest --ui`

## Melhores Práticas

- Use configuração Vite compartilhada entre app e testes
- Use API `describe`/`it`/`expect` (compatível com Jest)
- Aproveite `vi.mock()` e `vi.spyOn()` para mocks
- Use `@vitest/coverage-v8` para cobertura rápida
- Escreva testes junto com arquivos de origem
