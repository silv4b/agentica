# Recomendações Gerais

Estas recomendações se aplicam a qualquer projeto, independentemente da pilha tecnológica.

## Git

- Escreva mensagens de commit claras e descritivas no modo imperativo
- Mantenha os commits pequenos e focados em uma única preocupação
- Use branches de funcionalidade e squash merges para pull requests
- Nunca commite segredos, credenciais ou arquivos `.env`
- Mantenha o `.gitignore` atualizado

## Documentação

- Mantenha um `README.md` com instruções de configuração, execução e deploy
- Documente decisões de arquitetura em uma pasta `ADR` ou `docs/`
- Use docstrings/comentários para APIs públicas e lógica complexa
- Mantenha um `CHANGELOG.md` seguindo keepachangelog.com

## Testes

- Escreva testes junto com as funcionalidades (TDD quando possível)
- Busque cobertura significativa, não 100% por si só
- Teste comportamento, não detalhes de implementação
- Use fixtures realistas e evite mocks quando testes de integração forem suficientes

## Segurança

- Valide e sanitize toda entrada do usuário
- Use consultas parametrizadas para prevenir injeção
- Mantenha as dependências atualizadas
- Siga o princípio do menor privilégio

## Qualidade de Código

- Mantenha funções pequenas e com propósito único
- Prefira legibilidade em vez de engenhosidade
- Evite aninhamento profundo — retorne cedo quando possível
- Use nomes significativos para variáveis, funções e classes
- Elimine código morto e imports não utilizados
