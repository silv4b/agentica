# PostgreSQL

## Comandos

- Connect: `psql -U user -d database`
- Dump: `pg_dump -U user database > dump.sql`
- Restore: `psql -U user database < dump.sql`
- Migrate: Use ORM migration tools

## Melhores Práticas

- Use connection pooling (PgBouncer or built-in)
- Write migrations for all schema changes
- Use indexes for columns used in WHERE, JOIN, and ORDER BY
- Use `EXPLAIN ANALYZE` to debug slow queries
- Follow naming conventions: `snake_case` for tables and columns
- Use `UUID` or `BIGSERIAL` for primary keys
- Set `statement_timeout` to prevent runaway queries
