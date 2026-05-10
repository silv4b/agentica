# LinkedIn Post

Já teve que ensinar um agente de IA a trabalhar no seu projeto?

Se você usa GitHub Copilot, Cursor, Windsurf ou qualquer assistente de código, sabe o quanto é importante que ele entenda as particularidades do seu projeto. Mas ninguém merece ficar escrevendo instrução manual toda vez, né?
Foi pensando nisso que criei o Agentica Maker — um gerador web de arquivos AGENTS.md.

O problema: Sem um arquivo de instruções, o agente de IA chuta comandos, formatação e até tecnologia errada. Cada framework tem seu jeito de rodar testes, formatar código, fazer lint... E o assistente precisava saber disso.

A solução: Você seleciona as tecnologias que usa (Python, Django, React, Docker, PostgreSQL, e +50 outras) e o Agentica gera na hora um AGENTS.md completinho, pronto pra colocar na raiz do repositório. Em português ou inglês.

Como funciona:

- Interface com autocomplete inteligente (~55 tecnologias suportadas)
- Geração instantânea do arquivo com recomendações específicas pra cada stack
- Dá pra copiar, baixar ou até criar um Gist privado no GitHub direto pela ferramenta
- Links compartilháveis pra mandar o resultado pra galera do time
Stack que usei:
- Python + Django 6.0 no backend
- JavaScript puro (zero frameworks!) no frontend
- Tailwind CSS e highlight.js pra deixar bonito
- UV pra gerenciar dependências (recomendo demais!)
- Testes com pytest (cobertura > 90%)

O detalhe mais legal? O próprio AGENTS.md desse projeto foi gerado pelo Agentica Maker. O projeto é open source e tá disponível no GitHub. Feedbacks são mais que bem-vindos!
