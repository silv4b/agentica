<!-- markdownlint-disable MD060 MD040 -->
# Agentica Maker

Gera arquivos `AGENTS.md` com instruções personalizadas para ensinar agentes de IA a trabalhar com sua stack tecnológica.

## Funcionalidades

- **Seleção de tecnologias** — Autocomplete com 54 tecnologias suportadas
- **Idioma** — Geração em inglês (recomendado para melhor performance de agentes de IA)
- **Versões automáticas** — Detecta a versão mais recente de cada tecnologia (PyPI, npm, GitHub, RubyGems, Cargo)
- **Code Examples** — Exemplos de código bom/ruim para cada tecnologia
- **Boundaries** — Regras do que fazer/perguntar/nunca fazer para cada tecnologia
- **Copiar / Download** — Copie o resultado ou baixe como `AGENTS.md`
- **GitHub Gist** — Crie um gist privado diretamente pela interface
- **Modo edição** — Visualize e edite o conteúdo gerado antes de salvar

## Stack

| Tecnologia | Uso |
|---|---|
| **Django 6.0+** | Framework web |
| **Python 3.12+** | Linguagem |
| **Tailwind CSS** (CDN) | Estilização |
| **highlight.js** | Syntax highlight no resultado |
| **SQLite** | Banco de dados |

## Começando

```bash
git clone https://github.com/silv4b/agentica
cd agentica

uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Acesse `http://localhost:8000`.

## Como usar

1. Digite tecnologias no campo de busca (ex: `python`, `django`, `react`)
2. Pressione `Enter` ou `,` para adicionar cada uma
3. Clique em **Gerar AGENTS.md**
4. Copie, baixe ou publique no GitHub Gist
5. Use o modo **Visualizar/Editar** para ajustar o conteúdo

## Tecnologias suportadas (54)

```
Python, Django, FastAPI, Flask, UV, Node.js, Express, NestJS, Next.js,
Nuxt.js, React, Vue, Svelte, Angular, Astro, Vite, Vitest, Jest, Playwright,
TypeScript, JavaScript, jQuery, HTML, CSS, SCSS, Sass, Tailwind CSS, DaisyUI,
Go, Rust, Ruby, Rails, PHP, Laravel, Java, Kotlin, Spring, Spring Boot,
C#, ASP.NET Core, Blazor, Dart, Flutter, Swift, C++, Bash,
Docker, PostgreSQL, MySQL, MariaDB, MongoDB, Redis, Elasticsearch, SQLite
```

## Arquitetura

### Visão geral

O app usa **SQLite** como fonte única de verdade. As tecnologias e templates são gerenciados pelo ORM do Django. O conteúdo é populado via data migrations a partir de `generator/template_data.py`.

### Estrutura de diretórios

```
agentica-maker/
├── agentica/                  # Configuração do projeto Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
├── generator/                 # App Django principal
│   ├── views.py               # Lógica de geração
│   ├── models.py              # Technology + Template
│   ├── forms.py               # TechForm
│   ├── template_data.py       # Templates base (Markdown em Python)
│   ├── code_examples_data.py  # Code Examples + Boundaries por tecnologia
│   ├── version_fetcher.py     # Busca versões via API
│   ├── admin.py
│   ├── urls.py
│   └── templates/generator/
│       ├── index.html         # Página inicial com autocomplete
│       └── result.html        # Resultado com highlight e edição
├── templates/
│   └── base.html              # Base com nav, footer
├── tech_config.json           # Configuração (comandos, versão, ícone)
├── pyproject.toml
├── AGENTS.md                  # AGENTS.md deste projeto
└── README.md
```

### Fluxo de geração (`_build_content`)

1. **Parse**: string comma-separada → lista de tecnologias
2. **Match**: normaliza e busca no banco de dados (`Technology`)
3. **Separa**: `matched` (reconhecidas) e `unmatched` (não reconhecidas)
4. **Versões**: busca versão mais recente (cache de 1h via `version_fetcher.py`)
5. **Carrega**: template geral (`general`) + template de cada tecnologia
6. **Enriquece**: adiciona Code Examples + Boundaries dinamicamente
7. **Junta**: frontmatter + persona + comandos + templates + footer
8. **Renderiza**: `result.html` com o markdown final

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
uv run python manage.py migrate     # Migrações
uv run python manage.py test        # Rodar testes
uv run ruff check .                 # Lint
uv run ruff format .                # Formatar
```

## Licença

MIT
