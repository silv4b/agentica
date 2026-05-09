# SQLite

## Best Practices

- Use WAL mode for better concurrency
- Enable foreign keys with `PRAGMA foreign_keys = ON`
- Use `BEGIN`/`COMMIT` for batch operations
- Prefer `INTEGER PRIMARY KEY` for auto-increment IDs
- Use `EXPLAIN QUERY PLAN` for optimization
- Regular `VACUUM` to reclaim space
