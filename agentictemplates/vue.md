# Vue.js

## Commands

- Run: `npm run dev`
- Build: `npm run build`
- Test: `npm run test`
- Lint: `npm run lint`

## Code Style

- Use Composition API with `<script setup>`
- Use TypeScript when possible
- Keep components small and focused
- Use Pinia for state management (over Vuex)

## Best Practices

- Use `defineProps` and `defineEmits` for typed props/events
- Use `v-for` with `:key` (avoid index as key)
- Use computed properties over method calls in templates
- Use `async/await` with `<Suspense>` for async components
- Use composables for reusable logic
- Follow the Vue Style Guide (priority A and B rules)
