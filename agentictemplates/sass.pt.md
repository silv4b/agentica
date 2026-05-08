# Sass (SCSS)

## Comandos

- Compile: `sass src/styles.scss dist/styles.css`
- Watch: `sass --watch src/styles.scss dist/styles.css`

## Melhores Práticas

- Use `.scss` syntax (superset of CSS)
- Use variables (`$`) for design tokens
- Use `@mixin` and `@include` for reusable blocks
- Use `@use` for modular file imports (replaces `@import`)
- Organize with partials: `_variables.scss`, `_mixins.scss`, `_base.scss`
- Keep nesting to 3 levels max
- Use placeholder selectors (`%`) with `@extend` for DRY output
- Use `@function` for computed values
- Use `@each`, `@for`, `@while` for generating utility classes
- Enable `--style=compressed` for production builds
