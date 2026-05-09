# SCSS (Sass)

## Comandos

- Compile: `sass src/styles.scss dist/styles.css`
- Watch: `sass --watch src/styles.scss dist/styles.css`

## Melhores Práticas

- Use SCSS syntax over indented Sass syntax
- Use variables (`$`) for colors, fonts, and spacing
- Use nesting sparingly (max 3 levels deep)
- Use `@mixins` for reusable style blocks
- Use `@extend` carefully — prefer mixins
- Use partials (`_partial.scss`) and `@use` for modularity
- Use `@use` over `@import` (deprecated)
- Organize files: base, components, layouts, pages, themes
- Use maps (`$map: (...)`) for grouped values
- Avoid heavy computation in SCSS — do it in JS when possible
