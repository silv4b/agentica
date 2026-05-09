import json
import urllib.error
import urllib.request
from pathlib import Path

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import TechForm

BASE_DIR = Path(__file__).resolve().parent.parent

TECH_CONFIG_PATH = BASE_DIR / "tech_config.json"

with open(TECH_CONFIG_PATH, encoding="utf-8") as f:
    _TECH_DATA = json.load(f)

TECH_CONFIG = {}
for key, data in _TECH_DATA.items():
    cmd = {}
    for k in ("run", "test", "lint", "style"):
        cmd[k] = data[k]
    TECH_CONFIG[key] = cmd

TEMPLATES_DIR = BASE_DIR / "agentictemplates"


_translation_cache = {}


def _load_md(filename, lang="pt"):
    """Carrega o conteúdo de um arquivo Markdown, com fallback e tradução automática via Google Translator."""

    path_lang = TEMPLATES_DIR / lang / f"{filename}.md"
    if path_lang.exists():
        return path_lang.read_text(encoding="utf-8")

    path_en = TEMPLATES_DIR / "en" / f"{filename}.md"
    if not path_en.exists():
        return ""

    text = path_en.read_text(encoding="utf-8")

    cache_key = (filename, lang)
    if cache_key in _translation_cache:
        return _translation_cache[cache_key]

    try:
        from deep_translator import GoogleTranslator

        translated = GoogleTranslator(source="en", target=lang).translate(text)
        _translation_cache[cache_key] = translated
        path_lang.parent.mkdir(parents=True, exist_ok=True)
        path_lang.write_text(translated, encoding="utf-8")
        return translated
    except Exception:
        return text


def _normalize_tech(name):
    """Normaliza um nome de tecnologia removendo espaços, pontos e cerquilhas."""
    return name.strip().lower().replace(".", "").replace("#", "")


def _match_tech(raw_name):
    """Tenta corresponder um nome bruto a uma chave válida em TECH_CONFIG."""
    normalized = _normalize_tech(raw_name)
    for key in TECH_CONFIG:
        if normalized == key or normalized == key.replace(".", "").replace("#", ""):
            return key
    return None


def _parse_technologies(raw):
    """Converte uma string separada por vírgulas em uma lista de tecnologias."""
    result = []
    for t in raw.split(","):
        t = t.strip()
        if t:
            result.append(t)
    return result


def _pick(items, prefer_keyword):
    """Remove duplicatas mantendo a ordem e prioriza o item preferido no topo."""
    seen = set()
    result = []
    for item in items:
        if item.lower() not in seen:
            seen.add(item.lower())
            result.append(item)
    if result:
        result.sort(key=lambda x: (x.lower() != prefer_keyword.lower(), x))
    return result


def _tech_display_name(key: str) -> str:
    """Retorna o nome de exibição amigável de uma tecnologia a partir de sua chave."""
    return _TECH_DATA.get(key, {}).get("display_name", key.capitalize())


def _tech_devicon(key):
    """Retorna a classe CSS do Devicon para a tecnologia, ou fallback se não houver ícone."""
    return _TECH_DATA.get(key, {}).get("devicon", "devicon-love2d-plain")


def index(request):
    """Exibe a página inicial com o formulário de seleção de tecnologias."""
    form = TechForm()
    supported_techs = sorted(TECH_CONFIG.keys())
    tech_icons = {}
    for key in TECH_CONFIG:
        tech_icons[key] = _tech_devicon(key)
    supported_with_icons = []
    for t in supported_techs:
        supported_with_icons.append({"key": t, "icon": tech_icons[t]})
    return render(
        request,
        "generator/index.html",
        {
            "form": form,
            "supported_techs": supported_techs,
            "supported_with_icons": supported_with_icons,
            "tech_json": json.dumps(supported_techs),
            "tech_icons_json": json.dumps(tech_icons),
        },
    )


def result(request):
    """Processa o formulário POST e renderiza a página com o AGENTS.md gerado."""
    if request.method != "POST":
        form = TechForm()
        return render(request, "generator/index.html", {"form": form})

    form = TechForm(request.POST)
    if not form.is_valid():
        return render(request, "generator/index.html", {"form": form})

    lang = form.cleaned_data.get("language", "pt")

    agents_content, tech_list, matched, unmatched = _build_content(form.cleaned_data["technologies"], lang=lang)

    tech_icons = {}
    for key in TECH_CONFIG:
        tech_icons[key] = _tech_devicon(key)
    matched_with_icons = []
    for t in matched:
        matched_with_icons.append({"key": t, "icon": tech_icons[t]})

    return render(
        request,
        "generator/result.html",
        {
            "agents_content": agents_content,
            "tech_list": tech_list,
            "unmatched": unmatched,
            "matched": matched,
            "matched_with_icons": matched_with_icons,
            "lang": lang,
        },
    )


def download(request):
    """Gera e força o download do arquivo AGENTS.md como attachment."""
    if request.method != "POST":
        return HttpResponse(status=405)

    form = TechForm(request.POST)
    if not form.is_valid():
        return HttpResponse(b"Invalid form", status=400)

    lang = form.cleaned_data.get("language", "pt")
    agents_content, tech_list, _, _ = _build_content(form.cleaned_data["technologies"], lang=lang)

    filename = "AGENTS.md"
    response = HttpResponse(agents_content.encode("utf-8"), content_type="text/markdown; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@csrf_exempt
def create_gist(request):
    """Cria um Gist privado no GitHub com o conteúdo gerado, usando o token fornecido."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    content = body.get("content", "").strip()
    token = body.get("token", "").strip()
    description = body.get("description", "AGENTS.md — generated by Agentica")

    if not content:
        return JsonResponse({"error": "Content is required"}, status=400)
    if not token:
        return JsonResponse({"error": "GitHub token is required"}, status=400)

    payload = json.dumps(
        {
            "description": description,
            "public": False,
            "files": {
                "AGENTS.md": {
                    "content": content,
                }
            },
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        "https://api.github.com/gists",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Agentica/1.0",
            "Accept": "application/vnd.github+json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return JsonResponse(
                {
                    "url": data.get("html_url"),
                    "id": data.get("id"),
                }
            )
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return JsonResponse(
            {"error": f"GitHub API error ({e.code})", "detail": error_body},
            status=e.code,
        )
    except urllib.error.URLError as e:
        return JsonResponse({"error": f"Network error: {e.reason}"}, status=502)


def _build_content(raw_techs, lang="pt"):
    """Monta o conteúdo completo do AGENTS.md combinando os templates das tecnologias selecionadas."""
    tech_names = _parse_technologies(raw_techs)

    matched = []
    unmatched = []
    for name in tech_names:
        key = _match_tech(name)
        if key:
            matched.append(key)
        else:
            unmatched.append(name)

    matched = _pick(matched, matched[0] if matched else "")

    parts = []

    general = _load_md("general", lang=lang)
    if general:
        parts.append(general)

    for key in matched:
        content = _load_md(key, lang=lang)
        if content:
            parts.append(content)

    if matched:
        tech_names = []
        for t in matched:
            tech_names.append(_tech_display_name(t))
        tech_list = ", ".join(tech_names)
    else:
        tech_list = ", ".join(unmatched) if unmatched else "Nenhuma"

    agents_content = "\n---\n\n".join(parts)
    agents_content += "\n<!-- Feito com Agentica -->" if lang == "pt" else "\n<!-- Build with Agentica -->"

    return agents_content, tech_list, matched, unmatched
