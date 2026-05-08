# Node.js

## Commands

- Run: `npm run dev` or `node --watch .`
- Test: `npm run test`
- Lint: `npm run lint`
- Format: `npx prettier --write .`

## Code Style

- Use async/await over callbacks
- Use ES modules (type: "module" in package.json)
- Handle errors with proper error boundaries
- Use environment variables for configuration
- Prefer `fs/promises` over synchronous fs

## Best Practices

- Use a process manager (PM2) in production
- Implement proper error handling with custom error classes
- Use `helmet` and `cors` for security
- Structure code with layers (routes, controllers, services)
- Use `pino` or `winston` for structured logging
- Set `NODE_ENV=production` in production deployments
