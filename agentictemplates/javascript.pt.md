# JavaScript

## Comandos

- Formatar: `npx prettier --write .`
- Linter: `npx eslint .`
- Verificação de tipos: `npx tsc --noEmit` (if using TypeScript)

## Estilo de Código

- Use `const` by default, `let` only when reassigning
- Use arrow functions for callbacks and short functions
- Use template literals for string interpolation
- Use destructuring for objects and arrays
- Use optional chaining (`?.`) and nullish coalescing (`??`)

## Melhores Práticas

- Always use strict equality (`===` / `!==`)
- Avoid mutation — prefer immutable patterns
- Use `Array.map`, `filter`, `reduce` over loops
- Use `async/await` over promise chains
- Use `ES modules` (`import`/`export`) over CommonJS
- Handle errors with `try/catch` in async functions
- Format with Prettier and lint with ESLint
