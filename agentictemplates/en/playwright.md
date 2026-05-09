# Playwright

## Commands

- Test: `npx playwright test`
- UI mode: `npx playwright test --ui`
- Codegen: `npx playwright codegen`

## Best Practices

- Use page object model for test organization
- Prefer locators over CSS/XPath selectors
- Use `expect.toHaveScreenshot()` for visual testing
- Run tests in CI with `--shard` for parallel execution
- Use `test.use()` for project-specific configuration
- Use web-first assertions for reliability
