# Ruby

## Comandos

- Executar: `ruby script.rb`
- Testar: `ruby -Ilib:test test/test_*.rb`
- Linter: `rubocop`
- Formatar: `rubocop -A`

## Estilo de Código

- Siga o Ruby Style Guide
- Use 2 espaços para indentação
- Prefira symbols em vez de strings para identificadores
- Use snake_case para métodos e variáveis
- Use `attr_reader`/`attr_accessor` em vez de getters/setters explícitos

## Melhores Práticas

- Prefira iteradores em vez de loops `for`
- Use atalho `&:method_name` para passes de bloco
- Use tratamento de exceções com `begin`/`rescue`/`ensure`
- Prefira `case`/`when` em vez de múltiplos `if`/`elsif`
