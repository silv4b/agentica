# Vue.js

## Comandos

- Executar: `npm run dev`
- Build: `npm run build`
- Testar: `npm run test`
- Linter: `npm run lint`

## Estilo de Código

- Use Composition API with `<script setup>`
- Use TypeScript when possible
- Keep components small and focused
- Use Pinia for state management (over Vuex)

## Melhores Práticas

- Use `defineProps` and `defineEmits` for typed props/events
- Use `v-for` with `:key` (avoid index as key)
- Use computed properties over method calls in templates
- Use `async/await` with `<Suspense>` for async components
- Use composables for reusable logic
- Follow the Vue Style Guide (priority A and B rules)
