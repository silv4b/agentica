# Express

## Comandos

- Executar: `node --watch .` ou `npm run dev`
- Testar: `npm run test`
- Linter: `npm run lint`

## Estilo de Código

- Use async/await para handlers de rota
- Use ES modules (type: "module" no package.json)
- Estruture com padrão rotas, controladores, serviços

## Melhores Práticas

- Use middleware `helmet` e `cors` para segurança
- Implemente middleware centralizado de tratamento de erros
- Use `express-validator` ou `joi` para validação de requisições
- Rate limiting com `express-rate-limit`
- Use middleware de compressão para respostas
- Estruture código em camadas (rotas → controladores → serviços)
