# MariaDB

## Melhores Práticas

- Use InnoDB como mecanismo de armazenamento
- Indexe colunas usadas em cláusulas WHERE e JOIN
- Use `EXPLAIN` para analisar performance de consultas
- Backups regulares com `mariadb-dump`
- Use pooling de conexão em produção
- Monitore o log de queries lentas
