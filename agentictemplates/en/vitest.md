# Vitest

## Commands

- Test: `npx vitest` or `npm run test`
- Watch mode: `npx vitest`
- Coverage: `npx vitest --coverage`
- UI mode: `npx vitest --ui`

## Best Practices

- Use Vite config shared between app and tests
- Use `describe`/`it`/`expect` API (compatible with Jest)
- Leverage `vi.mock()` and `vi.spyOn()` for mocking
- Use `@vitest/coverage-v8` for fast coverage
- Write tests alongside source files
