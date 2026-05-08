# TypeScript

## Comandos

- Verificação de tipos: `npx tsc --noEmit`
- Build: `npm run build`
- Linter: `npm run lint`

## Estilo de Código

- Use strict mode in `tsconfig.json`
- Prefer interfaces over types for object shapes
- Use generics where appropriate for reusable code
- Avoid `any` — use `unknown` when type is not known
- Use `as const` for literal types

## Melhores Práticas

- Enable `strict: true` and `noUncheckedIndexedAccess`
- Use `zod` or `io-ts` for runtime validation
- Use `satisfies` operator (TS 4.9+) for type validation
- Prefer discriminated unions over optional fields
- Use `Record<K, V>` over index signatures when possible
- Use `ts-reset` for improved type safety
