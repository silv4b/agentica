# MySQL

## Comandos

- Connect: `mysql -u user -p database`
- Dump: `mysqldump -u user database > dump.sql`
- Import: `mysql -u user database < dump.sql`

## Melhores Práticas

- Use InnoDB as the storage engine
- Use indexes on columns used in WHERE, JOIN, and ORDER BY
- Use `EXPLAIN` to analyze slow queries
- Use `VARCHAR` for variable-length strings, `CHAR` for fixed
- Use `UUID_SHORT()` or `AUTO_INCREMENT` for primary keys
- Use foreign keys for referential integrity
- Write database migrations for schema changes
- Use connection pooling in your application
- Set appropriate `innodb_buffer_pool_size` for performance
