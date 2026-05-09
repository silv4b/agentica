# JavaScript

## Commands

- Format: `npx prettier --write .`
- Lint: `npx eslint .`
- Type check: `npx tsc --noEmit` (if using TypeScript)

## Code Style

- Use `const` by default, `let` only when reassigning
- Use arrow functions for callbacks and short functions
- Use template literals for string interpolation
- Use destructuring for objects and arrays
- Use optional chaining (`?.`) and nullish coalescing (`??`)

## Best Practices

- Always use strict equality (`===` / `!==`)
- Avoid mutation — prefer immutable patterns
- Use `Array.map`, `filter`, `reduce` over loops
- Use `async/await` over promise chains
- Use `ES modules` (`import`/`export`) over CommonJS
- Handle errors with `try/catch` in async functions
- Format with Prettier and lint with ESLint
