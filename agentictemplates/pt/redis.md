# Redis

## Comandos

- Connect: `redis-cli`
- Monitor: `redis-cli MONITOR`
- Info: `redis-cli INFO`

## Melhores Práticas

- Use Redis for caching, session storage, and pub/sub
- Set TTL (Time To Live) for all cached keys
- Use connection pooling in your application
- Handle connection failures gracefully with retries
- Use meaningful key naming conventions: `app:entity:id:field`
- Avoid storing large values — keep values under 10MB
- Use `SCAN` instead of `KEYS` in production
