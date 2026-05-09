# Express

## Commands

- Run: `node --watch .` or `npm run dev`
- Test: `npm run test`
- Lint: `npm run lint`

## Code Style

- Use async/await for route handlers
- Use ES modules (type: "module" in package.json)
- Structure with routes, controllers, services pattern

## Best Practices

- Use `helmet` and `cors` middleware for security
- Implement centralized error handling middleware
- Use `express-validator` or `joi` for request validation
- Rate limiting with `express-rate-limit`
- Use compression middleware for responses
- Structure code in layers (routes → controllers → services)
