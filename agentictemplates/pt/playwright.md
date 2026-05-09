# Playwright

## Comandos

- Testar: `npx playwright test`
- Modo UI: `npx playwright test --ui`
- Codegen: `npx playwright codegen`

## Melhores Práticas

- Use padrão page object para organização de testes
- Prefira locators em vez de seletores CSS/XPath
- Use `expect.toHaveScreenshot()` para testes visuais
- Execute testes em CI com `--shard` para execução paralela
- Use `test.use()` para configuração específica de projeto
- Use asserções web-first para confiabilidade
