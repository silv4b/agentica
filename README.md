<!-- markdownlint-disable MD060 MD040 -->
# Agentica Maker

O Agentica é um gerador arquivos `AGENTS.md` base para seus projetos, com instruções personalizadas que ensinam agentes de IA a trabalhar com sua stack.

## Funcionalidades

- **Seleção de tecnologias** — Autocomplete com ~30 tecnologias suportadas (Python, Django, React, Docker, etc.)
- **Idioma PT/EN** — O conteúdo é gerado em inglês por padrão ou traduzido para português via Google Translate com cache em disco
- **Copiar / Download** — Copie o resultado para a área de transferência ou baixe como `AGENTS.md`
- **GitHub Gist** — Crie um gist privado diretamente pela interface com seu token do GitHub
- **Highlight de sintaxe** — Código destacado com highlight.js + numeração de linhas

## Stack

| Tecnologia | Uso |
|---|---|
| **Django 6.0+** | Framework web |
| **Python 3.12+** | Linguagem |
| **deep-translator** | Tradução automática EN → PT |
| **Tailwind CSS** (CDN) | Estilização |
| **highlight.js** | Syntax highlight no resultado |
| **SQLite** | Banco (apenas para admin do Django) |

## Começando

```bash
# Clonar
git clone https://github.com/silv4b/agentica
cd agentica

# Sincronizar dependências (usa UV)
uv sync

# Rodar
uv run python manage.py runserver
```

Acesse `http://localhost:8000`.

## Como usar

1. Digite tecnologias no campo de busca (ex: `python`, `django`, `react`)
2. Pressione `Enter` ou `,` para adicionar cada uma
3. Escolha o idioma: **PT** ou **EN**
4. Clique em **Gerar AGENTS.md**
5. Copie, baixe ou publique no GitHub Gist

## Tecnologias suportadas (até o momento)

Python, Django, FastAPI, React, Next.js, Node.js, TypeScript, Docker, PostgreSQL, Redis, Tailwind CSS, DaisyUI, Flutter, Go, Rust, Vue, Svelte, Spring, Kotlin, Rails, Laravel, UV, JavaScript, PHP, Java, Spring Boot, MySQL, MongoDB, HTML, CSS, SCSS, Sass.

## Arquitetura

### Visão geral

O app não usa banco de dados para dados de usuário. Todo o conteúdo vem de arquivos Markdown em `agentictemplates/` combinados conforme as tecnologias selecionadas.

### Estrutura de diretórios

```
agentica-maker/
├── agentica/                  # Configuração do projeto Django
│   ├── settings.py
│   ├── urls.py                # Rotas raiz (admin + generator)
│   ├── wsgi.py / asgi.py
├── agentictemplates/          # Templates Markdown
│   ├── general.md             # Recomendações gerais (inglês)
│   ├── python.md              # Comandos + estilo Python
│   ├── django.md              # Comandos + boas práticas Django
│   ├── ...                    # ~30 tecnologias
│   └── *.pt.md                # Versões em português (cache)
├── generator/                 # App Django principal
│   ├── views.py               # Lógica: index, result, download, gist
│   ├── forms.py               # TechForm (technologies + language)
│   ├── urls.py                # Rotas do app
│   ├── templates/generator/
│   │   ├── index.html         # Página inicial com autocomplete
│   │   └── result.html        # Página de resultado com highlight
├── templates/
│   └── base.html              # Base com nav, footer, tema
├── pyproject.toml             # Dependências (UV)
├── AGENTS.md                  # AGENTS.md deste projeto
└── README.md
```

### Fluxo de geração (`_build_content`)

1. **Parse**: string comma-separada → lista de tecnologias
2. **Match**: cada tecnologia é normalizada e buscada em `TECH_CONFIG`
3. **Separa**: `matched` (reconhecidas) e `unmatched` (não reconhecidas)
4. **Carrega**: `general.md` + template de cada tecnologia no idioma escolhido
5. **Junta**: todas as partes concatenadas com `\n\n---\n\n`
6. **Renderiza**: `result.html` com o markdown final

### API Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Página inicial |
| `POST` | `/result/` | Gera AGENTS.md e exibe resultado |
| `POST` | `/download/` | Download do arquivo AGENTS.md |
| `POST` | `/create-gist/` | Cria gist privado no GitHub |

## Comandos

```bash
uv run python manage.py runserver   # Iniciar servidor
uv run python manage.py check       # Verificar projeto
uv run python manage.py test        # Rodar testes
uv run ruff check .                 # Lint
uv run ruff format .                # Formatar
```

## Licença

MIT
