# SQLite

## Melhores Práticas

- Use modo WAL para melhor concorrência
- Ative chaves estrangeiras com `PRAGMA foreign_keys = ON`
- Use `BEGIN`/`COMMIT` para operações em lote
- Prefira `INTEGER PRIMARY KEY` para auto-incremento de IDs
- Use `EXPLAIN QUERY PLAN` para otimização
- `VACUUM` regular para recuperar espaço
