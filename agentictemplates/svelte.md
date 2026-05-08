# Svelte / SvelteKit

## Commands

- Run: `npm run dev`
- Build: `npm run build`
- Test: `npm run test`
- Lint: `npm run lint`

## Code Style

- Use SvelteKit for full-stack apps (file-based routing)
- Use reactive statements (`$:`) sparingly
- Keep components small
- Use stores for shared state
- Use TypeScript when possible

## Best Practices

- Use `load` functions in SvelteKit for server-side data fetching
- Use `+page.server.ts` for sensitive data operations
- Use form actions for mutations
- Use `$app/stores` for navigation and page info
- Use `{@html}` carefully and never with user input
- Use `svelte-check` for type checking
