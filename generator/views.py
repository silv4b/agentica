import json
import urllib.error
import urllib.request
from datetime import datetime, timezone

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .code_examples_data import CODE_EXAMPLES
from .forms import TechForm
from .models import Technology, Template
from .version_fetcher import fetch_latest_version, get_version_label, needs_version_check


def _get_tech_config():
    return {t.key: t for t in Technology.objects.all()}


def _normalize_tech(name):
    return name.strip().lower().replace(".", "").replace("#", "")


def _match_tech(raw_name):
    normalized = _normalize_tech(raw_name)
    tech_config = _get_tech_config()
    for key in tech_config:
        if normalized == key or normalized == key.replace(".", "").replace("#", ""):
            return key
    return None


def _parse_technologies(raw):
    result = []
    for t in raw.split(","):
        t = t.strip()
        if t:
            result.append(t)
    return result


def _pick(items, prefer_keyword):
    seen = set()
    result = []
    for item in items:
        if item.lower() not in seen:
            seen.add(item.lower())
            result.append(item)
    if result:
        result.sort(key=lambda x: (x.lower() != prefer_keyword.lower(), x))
    return result


def _tech_display_name(key):
    tech = _get_tech_config().get(key)
    return tech.display_name if tech else key.capitalize()


def _tech_devicon(key):
    tech = _get_tech_config().get(key)
    return tech.devicon if tech else "devicon-love2d-plain"


def _load_md(filename):
    if filename == "general":
        tmpl = Template.objects.filter(technology__isnull=True, language="en").first()
    else:
        tmpl = Template.objects.filter(technology__key=filename, language="en").first()
    content = tmpl.content if tmpl else ""
    extra = CODE_EXAMPLES.get(filename)
    if extra:
        if extra.get("examples"):
            content += "\n\n" + extra["examples"]
        if extra.get("boundaries"):
            content += "\n\n" + extra["boundaries"]
    return content


def _append_regen_link(content, matched, request):
    if matched:
        techs = ",".join(matched)
        url = request.build_absolute_uri(f"/result/?tech={techs}")
        content += f"\n<!-- Regen: {url} -->"
    return content


def index(request):
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


def _render_result(request, agents_content, tech_list, matched, unmatched):
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


def result(request):
    if request.method == "GET":
        raw_techs = request.GET.get("tech", "").strip()
        if raw_techs:
            agents_content, tech_list, matched, unmatched = _build_content(raw_techs)
            agents_content = _append_regen_link(agents_content, matched, request)
            return _render_result(request, agents_content, tech_list, matched, unmatched)
        form = TechForm()
        return render(request, "generator/index.html", {"form": form})

    form = TechForm(request.POST)
    if not form.is_valid():
        return render(request, "generator/index.html", {"form": form})

    agents_content, tech_list, matched, unmatched = _build_content(form.cleaned_data["technologies"])
    agents_content = _append_regen_link(agents_content, matched, request)
    return _render_result(request, agents_content, tech_list, matched, unmatched)


def download(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    form = TechForm(request.POST)
    if not form.is_valid():
        return HttpResponse(b"Invalid form", status=400)

    agents_content, tech_list, matched, _ = _build_content(form.cleaned_data["technologies"])
    agents_content = _append_regen_link(agents_content, matched, request)

    filename = "AGENTS.md"
    response = HttpResponse(agents_content.encode("utf-8"), content_type="text/markdown; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@csrf_exempt
def download_raw(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    content = request.POST.get("content", "").strip()
    filename = request.POST.get("filename", "").strip() or "AGENTS.md"

    if not content:
        return HttpResponse(b"Content is required", status=400)

    response = HttpResponse(content.encode("utf-8"), content_type="text/markdown; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@csrf_exempt
def create_gist(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    content = body.get("content", "").strip()
    token = body.get("token", "").strip()
    filename = body.get("filename", "").strip() or "AGENTS.md"
    description = body.get("description", f"{filename} — generated by Agentica")

    if not content:
        return JsonResponse({"error": "Content is required"}, status=400)
    if not token:
        return JsonResponse({"error": "GitHub token is required"}, status=400)

    payload = json.dumps(
        {
            "description": description,
            "public": False,
            "files": {
                filename: {
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


def _ensure_versions(matched):
    config = _get_tech_config()
    now = datetime.now(tz=timezone.utc)
    for key in matched:
        tech = config.get(key)
        if tech and needs_version_check(tech):
            version = fetch_latest_version(tech.version_source)
            if version:
                Technology.objects.filter(pk=tech.pk).update(
                    latest_version=version,
                    version_checked_at=now,
                )
                tech.latest_version = version
                tech.version_checked_at = now


def _build_frontmatter(matched):
    config = _get_tech_config()
    labels = []
    for key in matched:
        tech = config.get(key)
        if tech:
            labels.append(get_version_label(tech))
    tech_str = ", ".join(labels) if labels else "this project"
    return f"---\nname: project-agent\ndescription: AI agent for {tech_str}\n---\n"


def _build_persona(matched):
    config = _get_tech_config()
    if matched:
        labels = []
        for key in matched:
            tech = config.get(key)
            labels.append(get_version_label(tech) if tech else key.capitalize())
        return f"You are an expert developer specializing in {', '.join(labels)}.\n"
    return "You are an expert developer.\n"


def _build_global_commands(matched):
    config = _get_tech_config()
    lines = []
    for key in matched:
        tech = config.get(key)
        if not tech:
            continue
        label = get_version_label(tech)
        if tech.run_command:
            lines.append(f"- Run ({label}): `{tech.run_command}`")
        if tech.test_command:
            lines.append(f"- Test ({label}): `{tech.test_command}`")
        if tech.lint_command:
            lines.append(f"- Lint ({label}): `{tech.lint_command}`")
    if lines:
        return "## Commands\n\n" + "\n".join(lines) + "\n"
    return ""


def _build_content(raw_techs):
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

    _ensure_versions(matched)

    parts = []

    frontmatter = _build_frontmatter(matched)
    if frontmatter:
        parts.append(frontmatter)

    persona = _build_persona(matched)
    if persona:
        parts.append(persona)

    global_commands = _build_global_commands(matched)
    if global_commands:
        parts.append(global_commands)

    general = _load_md("general")
    if general:
        parts.append(general)

    for key in matched:
        content = _load_md(key)
        if content:
            parts.append(content)

    if matched:
        config = _get_tech_config()
        tech_labels = []
        for t in matched:
            tech = config.get(t)
            tech_labels.append(get_version_label(tech) if tech else t.capitalize())
        tech_list = ", ".join(tech_labels)
    else:
        tech_list = ", ".join(unmatched) if unmatched else "Nenhuma"

    agents_content = "\n---\n\n".join(parts)
    agents_content += "\n\n<!-- Build with Agentica -->"

    return agents_content, tech_list, matched, unmatched
