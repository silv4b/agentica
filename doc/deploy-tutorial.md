<!-- markdownlint-disable MD040 MD036 -->

# Tutorial de Deploy — Agentica Maker

Passo a passo para preparar e fazer deploy do Agentica Maker em produção.

## Pré-requisitos

- Conta no [GitHub](https://github.com)
- Conta na plataforma de hospedagem escolhida (Railway, Render, Fly.io, PythonAnywhere, etc.)
- Domínio (opcional, mas recomendado)

---

## 1. Preparação do Projeto

### 1.1. Variáveis de ambiente

Crie `agentica/settings_prod.py` para configurações de produção:

```python
# agentica/settings_prod.py
from .settings import *
import os

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/db.sqlite3",  # Caminho customizado se usar volume persistente
    }
}

STATIC_ROOT = "/data/staticfiles"
STATIC_URL = "/static/"
```

> **Alternativa**: edite `settings.py` diretamente para ler `SECRET_KEY`, `DEBUG` e `ALLOWED_HOSTS` de variáveis de ambiente com fallback para desenvolvimento.

### 1.2. Gere uma SECRET_KEY forte

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Guarde o resultado — você vai usar como `DJANGO_SECRET_KEY` na plataforma de hospedagem.

### 1.3. Crie `requirements.txt`

O projeto usa **UV** com `pyproject.toml`, mas várias plataformas esperam `requirements.txt`:

```bash
uv export --no-dev --format requirements-constraints > requirements.txt
```

Adicione `gunicorn` no `pyproject.toml` (dependência de produção, não dev):

```toml
dependencies = [
    "django>=6.0.5",
    "ruff>=0.15.12",
    "gunicorn>=23.0.0",
]
```

Ou adicione manualmente no `requirements.txt` gerado.

### 1.4. Crie `runtime.txt` (para PythonAnywhere / Render)

```
python-3.12
```

### 1.5. Crie `Procfile` (para Railway / Render / Fly.io / Heroku)

```
web: gunicorn agentica.wsgi --bind 0.0.0.0:$PORT --workers 4
```

### 1.6. Crie `start.sh` (alternativa universal)

```bash
#!/usr/bin/env bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn agentica.wsgi --bind 0.0.0.0:${PORT:-8000} --workers 4
```

```bash
chmod +x start.sh
```

---

## 2. Configuração do Banco de Dados

**SQLite (padrão)** — funciona, mas **não é recomendado** para produção:

- Dados podem ser perdidos a cada deploy em plataformas efêmeras (Railway, Render free tier)
- Não suporta concorrência de escrita

**Recomendado: PostgreSQL**

Instale o driver:

```bash
uv add psycopg[binary]
```

Em `settings_prod.py`:

```python
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ["DATABASE_URL"],
        conn_max_age=600,
    )
}
```

Adicione `dj-database-url`:

```bash
uv add dj-database-url
```

---

## 3. Deploy em cada plataforma

### 3.1. Railway

1. Crie um novo projeto em [railway.app](https://railway.app)
2. Conecte seu repositório GitHub
3. Configure as variáveis de ambiente:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_SETTINGS_MODULE` → `agentica.settings`
   - `ALLOWED_HOSTS` → `.railway.app,seudominio.com`
   - `PORT` → `8000`
4. Adicione um volume persistente para SQLite (se não usar PostgreSQL):
   - Mount path: `/data`
5. Adicione um banco PostgreSQL (Recomendado)
6. Build command: `pip install -r requirements.txt`
7. Start command: `./start.sh`
8. Deploy

### 3.2. Render

1. Crie um **Web Service** em [render.com](https://render.com)
2. Conecte seu repositório GitHub
3. Preencha:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput`
   - **Start Command**: `gunicorn agentica.wsgi --bind 0.0.0.0:$PORT`
4. Adicione variáveis de ambiente:
   - `DJANGO_SECRET_KEY`
   - `DJANGO_SETTINGS_MODULE` → `agentica.settings`
   - `ALLOWED_HOSTS` → `.onrender.com,seudominio.com`
   - `PYTHON_VERSION` → `3.12.0`
5. Se for usar SQLite, ative o **Persistent Disk** (Render Blueprint) ou use PostgreSQL (recomendado)
6. Deploy

### 3.3. Fly.io

1. Instale a [CLI do Fly](https://fly.io/docs/hands-on/install-flyctl/)
2. `fly launch`
3. Edite `fly.toml`:

   ```toml
   [env]
     DJANGO_SECRET_KEY = "sua-chave"
     DJANGO_SETTINGS_MODULE = "agentica.settings"
     ALLOWED_HOSTS = ".fly.dev"
   ```

4. Adicione volume para SQLite ou use PostgreSQL (Fly Postgres):

   ```bash
   fly volumes create agentica_data --size 1
   ```

5. `fly deploy`

### 3.4. PythonAnywhere

1. Faça upload do código via git ou interface web
2. Crie um virtualenv e instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Na seção **Web**:
   - **WSGI configuration file**: aponte para `agentica/wsgi.py`
   - **Virtualenv**: selecione o que criou
4. Configure as variáveis de ambiente no arquivo WSGI ou via interface
5. Rode as migrações e collectstatic manualmente:

   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

---

## 4. Gunicorn + Nginx (VPS)

Se optar por um VPS (DigitalOcean, Linode, Hetzner):

```bash
# No servidor
sudo apt update && sudo apt install python3 python3-pip nginx

# Clone o projeto
git clone https://github.com/silv4b/agentica /opt/agentica
cd /opt/agentica

# Ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Migrações e estáticos
python manage.py migrate
python manage.py collectstatic

# Systemd service (/etc/systemd/system/agentica.service)
```

`/etc/systemd/system/agentica.service`:

```ini
[Unit]
Description=Agentica Maker
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/agentica
Environment=DJANGO_SECRET_KEY=sua-chave
Environment=DJANGO_SETTINGS_MODULE=agentica.settings
Environment=ALLOWED_HOSTS=seudominio.com
ExecStart=/opt/agentica/venv/bin/gunicorn agentica.wsgi --bind 0.0.0.0:8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Configure Nginx (`/etc/nginx/sites-available/agentica`):

```nginx
server {
    listen 80;
    server_name seudominio.com;

    location /static/ {
        alias /opt/agentica/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/agentica /etc/nginx/sites-enabled/
sudo systemctl daemon-reload
sudo systemctl enable --now agentica
sudo systemctl restart nginx
```

---

## 5. SSL (HTTPS)

### Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seudominio.com
```

### Railway / Render / Fly.io

Plataformas gerenciadas já fornecem SSL automaticamente nos subdomínios padrão. Para domínio customizado, configure o DNS e ative SSL no painel.

---

## 6. Checklist Final

Antes de ir ao ar:

- [ ] `SECRET_KEY` forte gerada e configurada como variável de ambiente
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` configurado com o domínio/IP
- [ ] Banco de dados PostgreSQL configurado (ou volume persistente para SQLite)
- [ ] `collectstatic` rodou e arquivos estáticos estão acessíveis
- [ ] Migrations aplicadas (`migrate`)
- [ ] Gunicorn rodando com workers suficientes (2-4 por CPU)
- [ ] SSL configurado e redirecionando HTTP → HTTPS
- [ ] Testes passando:

  ```bash
  uv run python manage.py test
  ```

- [ ] Lint limpo:

  ```bash
  uv run ruff check .
  ```

---

## 7. Manutenção

### Atualizar código

```bash
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart agentica   # VPS
# ou: git push (Railway/Render/Fly fazem deploy automático)
```

### Logs

```bash
# VPS
sudo journalctl -u agentica -f

# Railway
railway logs

# Render
render logs
```

### Backup (SQLite)

```bash
cp db.sqlite3 backups/$(date +%Y%m%d_%H%M%S).sqlite3
```

Com PostgreSQL, use `pg_dump` ou o backup automático da plataforma.

---

## 8. Custos Estimados (por mês)

| Plataforma | Free Tier | Mínimo pago |
|---|---|---|
| Railway | $5 crédito inicial | $5/mês |
| Render | 750h/mês (ideal) | $7/mês |
| Fly.io | $5 crédito/mês | $6/mês |
| PythonAnywhere | Sim (limitado) | $5/mês |
| VPS (Hetzner) | — | €4/mês |
| VPS (DigitalOcean) | — | $6/mês |

> **Recomendação inicial**: Render ou Fly.io — free tier suficiente para um projeto simples com PostgreSQL.

---

## 9. Troubleshooting Comum

| Problema | Causa | Solução |
|---|---|---|
| `DisallowedHost` | `ALLOWED_HOSTS` incompleto | Adicione o domínio/IP à lista |
| `400 Bad Request` | `ALLOWED_HOSTS` vazio com `DEBUG=False` | Configure `ALLOWED_HOSTS` |
| Estáticos não carregam | `collectstatic` não rodou | Rode `collectstatic` e verifique `STATIC_ROOT` |
| `500 Internal Server Error` | Erro no Python | Veja logs: `journalctl -u agentica` |
| Banco resetado a cada deploy | SQLite sem volume persistente | Migre para PostgreSQL ou adicione volume |
| `ModuleNotFoundError: gunicorn` | Gunicorn não instalado | Adicione ao `requirements.txt` |
| Conexão recusada | Firewall ou porta errada | Verifique se o serviço está rodando e a porta liberada |
