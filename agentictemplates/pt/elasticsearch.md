# Elasticsearch

## Melhores Práticas

- Planeje mapeamentos de índice cuidadosamente (evite mapeamento dinâmico em produção)
- Use aliases de índice para reindexação sem downtime
- Defina quantidade apropriada de shards para o tamanho do cluster
- Use Elasticsearch como mecanismo de busca, não como banco primário
- Monitore a saúde do cluster e alocação de shards
