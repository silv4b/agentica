import json
import urllib.error
import urllib.request

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import TechForm
from .models import Technology, Template


def _get_tech_config():
    """Carrega configurações de tecnologia do banco."""
    return {t.key: t for t in Technology.objects.all()}


def _normalize_tech(name):
    """Normaliza um nome de tecnologia removendo espaços, pontos e cerquilhas."""
    return name.strip().lower().replace(".", "").replace("#", "")


def _match_tech(raw_name):
    """Tenta corresponder um nome bruto a uma chave válida de tecnologia."""
    normalized = _normalize_tech(raw_name)
    tech_config = _get_tech_config()
    for key in tech_config:
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
    tech = _get_tech_config().get(key)
    return tech.display_name if tech else key.capitalize()


def _tech_devicon(key):
    """Retorna a classe CSS do Devicon para a tecnologia, ou fallback se não houver ícone."""
    tech = _get_tech_config().get(key)
    return tech.devicon if tech else "devicon-love2d-plain"


def _load_md(filename):
    """Carrega o conteúdo de um template do banco (sempre em inglês)."""
    if filename == "general":
        tmpl = Template.objects.filter(technology__isnull=True, language="en").first()
    else:
        tmpl = Template.objects.filter(technology__key=filename, language="en").first()

    return tmpl.content if tmpl else ""


def index(request):
    """Exibe a página inicial com o formulário de seleção de tecnologias."""
    form = TechForm()
    techs = _get_tech_config()
    supported_techs = sorted(techs.keys())
    tech_icons = {key: t.devicon for key, t in techs.items()}
    supported_with_icons = [{"key": t.key, "icon": t.devicon} for t in techs.values()]
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

    agents_content, tech_list, matched, unmatched = _build_content(form.cleaned_data["technologies"])

    techs = _get_tech_config()
    matched_with_icons = [{"key": t, "icon": techs[t].devicon} for t in matched if t in techs]

    return render(
        request,
        "generator/result.html",
        {
            "agents_content": agents_content,
            "tech_list": tech_list,
            "unmatched": unmatched,
            "matched": matched,
            "matched_with_icons": matched_with_icons,
        },
    )


def download(request):
    """Gera e força o download do arquivo AGENTS.md como attachment."""
    if request.method != "POST":
        return HttpResponse(status=405)

    form = TechForm(request.POST)
    if not form.is_valid():
        return HttpResponse(b"Invalid form", status=400)

    agents_content, tech_list, _, _ = _build_content(form.cleaned_data["technologies"])

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


def _build_content(raw_techs):
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

    general = _load_md("general")
    if general:
        parts.append(general)

    for key in matched:
        content = _load_md(key)
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
    agents_content += "\n<!-- Build with Agentica -->"

    return agents_content, tech_list, matched, unmatched
