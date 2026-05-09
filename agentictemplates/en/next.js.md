# Next.js

## Commands

- Run: `npm run dev`
- Build: `npm run build`
- Test: `npm run test`
- Lint: `npm run lint`

## Code Style

- Use App Router by default
- Use Server Components where possible
- Keep client components minimal with `"use client"`
- Use Next.js built-in optimizations (Image, Link, fonts)
- Follow the file-based routing conventions

## Best Practices

- Fetch data in Server Components when possible
- Use `generateStaticParams` for static generation
- Use `loading.js` and `error.js` for each route segment
- Configure `next.config.js` for images, rewrites, and headers
- Use `next/dynamic` for lazy loading
- Implement `metadata` export for SEO
