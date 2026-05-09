# Jest

## Comandos

- Testar: `npx jest` ou `npm run test`
- Modo watch: `npx jest --watch`
- Cobertura: `npx jest --coverage`

## Melhores Práticas

- Use blocos `describe`/`it` para organização de testes
- Prefira matchers `toBe` e `toEqual`
- Use `jest.fn()` para mocks simples
- Use `jest.spyOn()` para mocks parciais
- Escreva testes junto com arquivos de implementação
