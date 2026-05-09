import json
from email.message import Message
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from django.test import TestCase
from django.urls import reverse

from generator.forms import TechForm
from generator.views import (
    TECH_CONFIG,
    _build_content,
    _load_md,
    _match_tech,
    _normalize_tech,
    _parse_technologies,
    _pick,
    _tech_display_name,
    _translation_cache,
)


class NormalizeTechTests(TestCase):
    def test_strips_whitespace_and_lowercases(self):
        """Remove espaços extras e converte para minúsculo."""
        assert _normalize_tech("  Python  ") == "python"

    def test_removes_dots(self):
        """Remove pontos do nome da tecnologia."""
        assert _normalize_tech("Next.js") == "nextjs"
        assert _normalize_tech(".NET") == "net"

    def test_removes_hashes(self):
        """Remove cerquilhas do nome da tecnologia."""
        assert _normalize_tech("C#") == "c"

    def test_removes_both_dots_and_hashes(self):
        """Remove pontos e cerquilhas simultaneamente."""
        assert _normalize_tech("  Next.JS  ") == "nextjs"

    def test_empty_string(self):
        """String vazia retorna string vazia."""
        assert _normalize_tech("") == ""

    def test_no_changes_for_already_normal(self):
        """Nome já normalizado não é alterado."""
        assert _normalize_tech("python") == "python"

    def test_mixed_case_with_symbols(self):
        """Mistura de maiúsculas, minúsculas, pontos e cerquilhas é normalizada."""
        assert _normalize_tech("  Type.Script#  ") == "typescript"


class MatchTechTests(TestCase):
    def test_exact_match(self):
        """Match exato com chave do TECH_CONFIG."""
        assert _match_tech("python") == "python"

    def test_case_insensitive_match(self):
        """Match ignora diferenças de maiúsculas e minúsculas."""
        assert _match_tech("PYTHON") == "python"

    def test_dot_normalization_to_exact_key(self):
        """Nome com ponto mantém a chave original com ponto."""
        assert _match_tech("next.js") == "next.js"

    def test_dot_normalization_to_normalized_key(self):
        """Nome sem ponto encontra a chave que contém ponto."""
        assert _match_tech("nextjs") == "next.js"

    def test_no_match_returns_none(self):
        """Tecnologia inexistente retorna None."""
        assert _match_tech("nonexistent_xyz") is None

    def test_whitespace_handling(self):
        """Espaços ao redor do nome são ignorados."""
        assert _match_tech("  Django  ") == "django"

    def test_empty_string_returns_none(self):
        """String vazia retorna None."""
        assert _match_tech("") is None

    def test_all_tech_config_keys_are_matchable_by_name(self):
        """Todas as chaves do TECH_CONFIG são encontráveis pelo próprio nome."""
        for key in TECH_CONFIG:
            assert _match_tech(key) == key

    def test_normalized_variant_matches(self):
        """Variação normalizada de chave com ponto é encontrável."""
        assert _match_tech("nextjs") == "next.js"


class ParseTechnologiesTests(TestCase):
    def test_simple_comma_separated(self):
        """Lista separada por vírgulas é convertida em lista de strings."""
        assert _parse_technologies("python, django, react") == ["python", "django", "react"]

    def test_with_extra_whitespace(self):
        """Espaços extras ao redor das vírgulas são ignorados."""
        assert _parse_technologies("  python  ,  django  ") == ["python", "django"]

    def test_single_value(self):
        """Valor único sem vírgulas retorna lista com um elemento."""
        assert _parse_technologies("python") == ["python"]

    def test_trailing_comma(self):
        """Vírgula no final é ignorada."""
        assert _parse_technologies("python, django,") == ["python", "django"]

    def test_empty_string(self):
        """String vazia retorna lista vazia."""
        assert _parse_technologies("") == []

    def test_only_whitespace_and_commas(self):
        """Apenas espaços e vírgulas retorna lista vazia."""
        assert _parse_technologies(" , , ") == []

    def test_leading_comma(self):
        """Vírgula no início é ignorada."""
        assert _parse_technologies(",python,django") == ["python", "django"]


class PickTests(TestCase):
    def test_removes_duplicates_case_insensitive(self):
        """Remove duplicatas ignorando diferenças de caixa."""
        result = _pick(["python", "Python", "PYTHON", "django"], "python")
        assert result == ["python", "django"]

    def test_preferred_keyword_first(self):
        """Keyword preferida é posicionada no topo da lista."""
        result = _pick(["django", "python", "react"], "python")
        assert result[0] == "python"

    def test_empty_list(self):
        """Lista vazia retorna lista vazia."""
        assert _pick([], "python") == []

    def test_single_item(self):
        """Lista com um único item retorna o mesmo item."""
        assert _pick(["python"], "python") == ["python"]

    def test_preferred_not_in_list(self):
        """Keyword preferida ausente na lista não altera a ordem."""
        result = _pick(["django", "react"], "python")
        assert result == ["django", "react"]

    def test_all_same_ignoring_case(self):
        """Múltiplas variações de caixa do mesmo item são reduzidas a uma."""
        result = _pick(["python", "PYTHON", "Python"], "python")
        assert result == ["python"]

    def test_ordering_with_preferred(self):
        """Item preferido aparece primeiro, os demais mantêm ordem alfabética."""
        result = _pick(["react", "django", "python", "vue"], "python")
        assert result[0] == "python"

    def test_preferred_keyword_case_insensitive(self):
        """Match da keyword preferida ignora caixa."""
        result = _pick(["Django", "Python", "React"], "python")
        assert result[0] == "Python"


class TechDisplayNameTests(TestCase):
    def test_known_overrides(self):
        """Todos os overrides conhecidos retornam o nome de exibição esperado."""
        cases = {
            "next.js": "Next.js",
            "javascript": "JavaScript",
            "typescript": "TypeScript",
            "html": "HTML",
            "css": "CSS",
            "scss": "SCSS",
            "sass": "Sass",
            "fastapi": "FastAPI",
            "postgresql": "PostgreSQL",
            "mongodb": "MongoDB",
            "mysql": "MySQL",
            "springboot": "Spring Boot",
            "daisyui": "DaisyUI",
            "tailwind": "Tailwind CSS",
            "uv": "UV",
            "php": "PHP",
            "java": "Java",
            "go": "Go",
            "rust": "Rust",
            "vue": "Vue.js",
            "node": "Node.js",
            "flutter": "Flutter",
            "kotlin": "Kotlin",
            "rails": "Ruby on Rails",
            "svelte": "Svelte",
            "laravel": "Laravel",
            "docker": "Docker",
            "redis": "Redis",
            "spring": "Spring",
            "django": "Django",
            "react": "React",
            "python": "Python",
            "angular": "Angular",
            "aspnetcore": "ASP.NET Core",
            "astro": "Astro",
            "bash": "Bash",
            "blazor": "Blazor",
            "csharp": "C#",
            "cplusplus": "C++",
            "dart": "Dart",
            "elasticsearch": "Elasticsearch",
            "express": "Express",
            "flask": "Flask",
            "jest": "Jest",
            "jquery": "jQuery",
            "mariadb": "MariaDB",
            "nestjs": "NestJS",
            "nuxt.js": "Nuxt.js",
            "playwright": "Playwright",
            "ruby": "Ruby",
            "sqlite": "SQLite",
            "swift": "Swift",
            "vite": "Vite",
            "vitest": "Vitest",
        }
        for key, expected in cases.items():
            with self.subTest(key=key):
                assert _tech_display_name(key) == expected

    def test_unknown_key_falls_back_to_capitalize(self):
        """Chave desconhecida usa capitalize como fallback."""
        assert _tech_display_name("unknown") == "Unknown"

    def test_multiple_word_key(self):
        """Chave com underline é capitalizada parcialmente."""
        assert _tech_display_name("some_tech") == "Some_tech"

    def test_all_tech_config_keys_have_display_names(self):
        """Todas as chaves do TECH_CONFIG possuem nome de exibição não vazio."""
        for key in TECH_CONFIG:
            name = _tech_display_name(key)
            assert len(name) > 0


class LoadMdTests(TestCase):
    def setUp(self):
        """Limpa o cache de tradução antes de cada teste."""
        _translation_cache.clear()

    def test_loads_pt_file_when_exists(self):
        """Arquivo .pt.md existente é carregado diretamente."""
        content = _load_md("general", lang="pt")
        assert "Recomendações Gerais" in content

    def test_loads_en_file_directly(self):
        """Idioma inglês carrega o arquivo base sem tradução."""
        content = _load_md("general", lang="en")
        assert "General Recommendations" in content

    def test_returns_empty_for_nonexistent_file(self):
        """Arquivo inexistente retorna string vazia."""
        content = _load_md("nonexistent_tech_abcdef")
        assert content == ""

    def test_en_returns_base_file_without_translation(self):
        """Idioma inglês retorna conteúdo do arquivo base."""
        content = _load_md("python", lang="en")
        assert "# Python" in content

    def test_pt_and_en_differ_when_both_exist(self):
        """Conteúdo em português e inglês são diferentes quando ambos existem."""
        pt_content = _load_md("general", lang="pt")
        en_content = _load_md("general", lang="en")
        assert pt_content != en_content

    def test_translation_path(self):
        """Fluxo de tradução é acionado quando apenas o arquivo base existe."""
        _translation_cache.clear()
        original_exists = Path.exists
        original_read_text = Path.read_text
        original_mkdir = Path.mkdir
        original_write_text = Path.write_text

        def controlled_exists(self):
            name = str(self)
            if "test_tech" in name:
                return "en" in self.parts
            return original_exists(self)

        def controlled_read_text(self, **kwargs):
            name = str(self)
            if "test_tech" in name:
                return "English test content"
            return original_read_text(self, **kwargs)

        def controlled_mkdir(self, **kwargs):
            if "test_tech" in str(self):
                return None
            return original_mkdir(self, **kwargs)

        def controlled_write_text(self, content, **kwargs):
            if "test_tech" in str(self):
                return None
            return original_write_text(self, content, **kwargs)

        with (
            patch.object(Path, "exists", controlled_exists),
            patch.object(Path, "read_text", controlled_read_text),
            patch.object(Path, "mkdir", controlled_mkdir),
            patch.object(Path, "write_text", controlled_write_text),
            patch("deep_translator.GoogleTranslator") as mock_gt,
        ):
            mock_gt.return_value.translate.return_value = "Conteúdo de teste"
            result = _load_md("test_tech", lang="pt")

        assert result == "Conteúdo de teste"
        mock_gt.return_value.translate.assert_called_once_with("English test content")

    def test_translation_is_cached(self):
        """Tradução é armazenada em cache e reutilizada na segunda chamada."""
        _translation_cache.clear()
        original_exists = Path.exists
        original_read_text = Path.read_text

        def controlled_exists(self):
            name = str(self)
            if "test_cache" in name:
                return "en" in self.parts
            return original_exists(self)

        def controlled_read_text(self, **kwargs):
            name = str(self)
            if "test_cache" in name:
                return "Cache test content"
            return original_read_text(self, **kwargs)

        with (
            patch.object(Path, "exists", controlled_exists),
            patch.object(Path, "read_text", controlled_read_text),
            patch.object(Path, "mkdir", return_value=None),
            patch.object(Path, "write_text", return_value=None),
            patch("deep_translator.GoogleTranslator") as mock_gt,
        ):
            mock_gt.return_value.translate.return_value = "Conteúdo em cache"

            result1 = _load_md("test_cache", lang="pt")
            assert result1 == "Conteúdo em cache"

            result2 = _load_md("test_cache", lang="pt")
            assert result2 == "Conteúdo em cache"
            assert mock_gt.return_value.translate.call_count == 1

    def test_translation_failure_returns_original_text(self):
        """Falha na API de tradução retorna o texto original em inglês."""
        _translation_cache.clear()
        original_exists = Path.exists
        original_read_text = Path.read_text

        def controlled_exists(self):
            name = str(self)
            if "test_fail" in name:
                return "en" in self.parts
            return original_exists(self)

        def controlled_read_text(self, **kwargs):
            name = str(self)
            if "test_fail" in name:
                return "Original English text"
            return original_read_text(self, **kwargs)

        with (
            patch.object(Path, "exists", controlled_exists),
            patch.object(Path, "read_text", controlled_read_text),
            patch("deep_translator.GoogleTranslator") as mock_gt,
        ):
            mock_gt.side_effect = Exception("Translation API unavailable")
            result = _load_md("test_fail", lang="pt")

        assert result == "Original English text"

    def test_pt_file_takes_precedence_over_base(self):
        """Arquivo .pt.md tem precedência sobre o arquivo base quando existe."""
        _translation_cache.clear()
        original_exists = Path.exists
        original_read_text = Path.read_text

        def controlled_exists(self):
            name = str(self)
            if "test_prec" in name:
                return name.endswith((".md", ".pt.md"))
            return original_exists(self)

        def controlled_read_text(self, **kwargs):
            name = str(self)
            if "test_prec" in name:
                return "Conteúdo PT" if "pt" in self.parts else "Base content"
            return original_read_text(self, **kwargs)

        with (
            patch.object(Path, "exists", controlled_exists),
            patch.object(Path, "read_text", controlled_read_text),
        ):
            result = _load_md("test_prec", lang="pt")

        assert result == "Conteúdo PT"


class BuildContentTests(TestCase):
    def setUp(self):
        """Limpa o cache de tradução antes de cada teste."""
        _translation_cache.clear()

    @patch("generator.views._load_md")
    def test_build_content_with_multiple_techs(self, mock_load_md):
        """Conteúdo montado combina template geral com templates das tecnologias selecionadas."""
        mock_load_md.side_effect = lambda f, lang: {
            "general": "# General Recommendations",
            "python": "# Python Instructions",
            "django": "# Django Instructions",
        }.get(f, "")

        content, tech_list, matched, unmatched = _build_content("python, django")

        assert "# General Recommendations" in content
        assert "# Python Instructions" in content
        assert "# Django Instructions" in content
        assert "Feito com Agentica" in content
        assert tech_list == "Python, Django"
        assert matched == ["python", "django"]
        assert unmatched == []

    @patch("generator.views._load_md")
    def test_build_content_with_unmatched_techs(self, mock_load_md):
        """Tecnologias não reconhecidas são separadas como unmatched."""
        mock_load_md.side_effect = lambda f, lang: {
            "general": "# General",
            "python": "# Python",
        }.get(f, "")

        content, tech_list, matched, unmatched = _build_content("python, unknown_x, another_unknown")

        assert matched == ["python"]
        assert unmatched == ["unknown_x", "another_unknown"]

    @patch("generator.views._load_md")
    def test_build_content_empty_input(self, mock_load_md):
        """Entrada vazia resulta em listas matched e unmatched vazias."""
        mock_load_md.return_value = "# General"
        content, tech_list, matched, unmatched = _build_content("")
        assert matched == []
        assert unmatched == []

    @patch("generator.views._load_md")
    def test_build_content_all_unmatched(self, mock_load_md):
        """Quando nenhuma tecnologia é reconhecida, todas vão para unmatched."""
        mock_load_md.return_value = "# General"
        content, tech_list, matched, unmatched = _build_content("foo, bar, baz")
        assert matched == []
        assert unmatched == ["foo", "bar", "baz"]
        assert tech_list == "foo, bar, baz"

    @patch("generator.views._load_md")
    def test_build_content_passes_language_to_load_md(self, mock_load_md):
        """O parâmetro lang é repassado para _load_md em todas as chamadas."""
        mock_load_md.return_value = "# Content"
        _build_content("python", lang="en")
        for call_args in mock_load_md.call_args_list:
            _name, kwargs = call_args
            assert kwargs.get("lang") == "en"

    @patch("generator.views._load_md")
    def test_build_content_deduplicates_techs(self, mock_load_md):
        """Tecnologias duplicadas com variações de caixa são reduzidas a uma."""
        mock_load_md.side_effect = lambda f, lang: {
            "general": "# General",
            "python": "# Python",
        }.get(f, "")

        content, tech_list, matched, unmatched = _build_content("python, python, PYTHON, Python")
        assert matched == ["python"]
        assert tech_list == "Python"

    @patch("generator.views._load_md")
    def test_build_content_preserves_tech_order_with_preferred_first(self, mock_load_md):
        """A primeira tecnologia da lista é posicionada no topo, as demais em ordem alfabética."""
        mock_load_md.side_effect = lambda f, lang: {
            "general": "# General",
            "django": "# Django",
            "react": "# React",
            "python": "# Python",
        }.get(f, "")

        content, tech_list, matched, unmatched = _build_content("django, react, python")
        assert matched == ["django", "python", "react"]

    @patch("generator.views._load_md")
    def test_build_content_footer_present(self, mock_load_md):
        """O footer 'Feito com Agentica' está sempre presente no conteúdo gerado."""
        mock_load_md.return_value = "# Some content"
        content, tech_list, matched, unmatched = _build_content("python")
        assert "Feito com Agentica" in content

    @patch("generator.views._load_md")
    def test_build_content_removes_blank_template(self, mock_load_md):
        """Templates vazios são omitidos do conteúdo final."""
        mock_load_md.side_effect = lambda f, lang: {
            "general": "# General",
            "python": "",
        }.get(f, "")

        content, tech_list, matched, unmatched = _build_content("python, django")
        assert "# General" in content


class IndexViewTests(TestCase):
    def test_index_get_returns_200(self):
        """GET / retorna status 200."""
        response = self.client.get(reverse("index"))
        assert response.status_code == 200

    def test_index_uses_correct_template(self):
        """GET / utiliza o template index.html."""
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "generator/index.html")

    def test_index_contains_tech_json(self):
        """O contexto da view contém a lista de tecnologias em JSON."""
        response = self.client.get(reverse("index"))
        assert "tech_json" in response.context

    def test_index_contains_form(self):
        """O contexto da view contém o formulário TechForm."""
        response = self.client.get(reverse("index"))
        assert "form" in response.context

    def test_index_contains_supported_techs(self):
        """O contexto da view contém a lista de tecnologias suportadas."""
        response = self.client.get(reverse("index"))
        assert "supported_techs" in response.context


class ResultViewTests(TestCase):
    def test_result_get_returns_index_page(self):
        """GET /result/ redireciona para a página inicial com o formulário."""
        response = self.client.get(reverse("result"))
        assert response.status_code == 200
        self.assertTemplateUsed(response, "generator/index.html")

    def test_result_post_invalid_form(self):
        """POST /result/ com formulário inválido renderiza index com erros."""
        response = self.client.post(reverse("result"), {})
        assert response.status_code == 200
        self.assertTemplateUsed(response, "generator/index.html")

    @patch("generator.views._load_md")
    def test_result_post_valid_pt(self, mock_load_md):
        """POST /result/ válido com idioma pt renderiza result.html com lang='pt'."""
        mock_load_md.side_effect = lambda f, lang: {
            "general": "# General",
            "python": "# Python",
        }.get(f, "")

        response = self.client.post(
            reverse("result"),
            {
                "technologies": "python",
                "language": "pt",
            },
        )
        assert response.status_code == 200
        self.assertTemplateUsed(response, "generator/result.html")
        assert response.context["lang"] == "pt"

    @patch("generator.views._load_md")
    def test_result_post_valid_en(self, mock_load_md):
        """POST /result/ válido com idioma en renderiza result.html com lang='en'."""
        mock_load_md.side_effect = lambda f, lang: {
            "general": "# General",
            "python": "# Python",
        }.get(f, "")

        response = self.client.post(
            reverse("result"),
            {
                "technologies": "python",
                "language": "en",
            },
        )
        assert response.status_code == 200
        assert response.context["lang"] == "en"

    @patch("generator.views._load_md")
    def test_result_shows_matched_and_unmatched(self, mock_load_md):
        """O contexto da view diferencia tecnologias reconhecidas de não reconhecidas."""
        mock_load_md.side_effect = lambda f, lang: {
            "general": "# General",
            "python": "# Python",
        }.get(f, "")

        response = self.client.post(
            reverse("result"),
            {
                "technologies": "python, unknown_tech",
                "language": "pt",
            },
        )
        assert response.context["matched"] == ["python"]
        assert response.context["unmatched"] == ["unknown_tech"]

    def test_result_missing_technologies_field(self):
        """POST /result/ sem o campo technologies renderiza index com erros."""
        response = self.client.post(reverse("result"), {"language": "pt"})
        assert response.status_code == 200
        self.assertTemplateUsed(response, "generator/index.html")


class DownloadViewTests(TestCase):
    def test_download_get_returns_405(self):
        """GET /download/ retorna 405 Method Not Allowed."""
        response = self.client.get(reverse("download"))
        assert response.status_code == 405

    def test_download_post_invalid_form_returns_400(self):
        """POST /download/ com formulário inválido retorna 400."""
        response = self.client.post(reverse("download"), {})
        assert response.status_code == 400

    @patch("generator.views._load_md")
    def test_download_post_valid(self, mock_load_md):
        """POST /download/ válido retorna arquivo com Content-Disposition attachment."""
        mock_load_md.side_effect = lambda f, lang: {
            "general": "# General",
            "python": "# Python",
        }.get(f, "")

        response = self.client.post(
            reverse("download"),
            {
                "technologies": "python",
                "language": "pt",
            },
        )
        assert response.status_code == 200
        assert response["Content-Disposition"] == 'attachment; filename="AGENTS.md"'
        assert response["Content-Type"] == "text/markdown; charset=utf-8"

    @patch("generator.views._load_md")
    def test_download_contains_content(self, mock_load_md):
        """O conteúdo baixado inclui o footer do Agentica Maker."""
        mock_load_md.side_effect = lambda f, lang: {
            "general": "# General",
            "python": "# Python",
        }.get(f, "")

        response = self.client.post(
            reverse("download"),
            {
                "technologies": "python",
                "language": "pt",
            },
        )
        content = response.content.decode("utf-8")
        assert "Feito com Agentica" in content


class CreateGistViewTests(TestCase):
    def test_create_gist_get_returns_405(self):
        """GET /create-gist/ retorna 405 Method Not Allowed."""
        response = self.client.get(reverse("create_gist"))
        assert response.status_code == 405

    def test_create_gist_invalid_json(self):
        """POST /create-gist/ com JSON inválido retorna 400."""
        response = self.client.post(
            reverse("create_gist"),
            data="not json",
            content_type="application/json",
        )
        assert response.status_code == 400
        assert "Invalid JSON" in response.json()["error"]

    def test_create_gist_missing_content(self):
        """POST /create-gist/ sem campo content retorna 400."""
        response = self.client.post(
            reverse("create_gist"),
            data=json.dumps({"token": "abc123"}),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert "Content is required" in response.json()["error"]

    def test_create_gist_empty_content(self):
        """POST /create-gist/ com content vazio retorna 400."""
        response = self.client.post(
            reverse("create_gist"),
            data=json.dumps({"content": "  ", "token": "abc123"}),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert "Content is required" in response.json()["error"]

    def test_create_gist_missing_token(self):
        """POST /create-gist/ sem campo token retorna 400."""
        response = self.client.post(
            reverse("create_gist"),
            data=json.dumps({"content": "some content"}),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert "GitHub token is required" in response.json()["error"]

    def test_create_gist_empty_token(self):
        """POST /create-gist/ com token vazio retorna 400."""
        response = self.client.post(
            reverse("create_gist"),
            data=json.dumps({"content": "content", "token": "  "}),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert "GitHub token is required" in response.json()["error"]

    @patch("generator.views.urllib.request.urlopen")
    def test_create_gist_success(self, mock_urlopen):
        """POST /create-gist/ válido retorna URL e ID do Gist criado."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(
            {
                "html_url": "https://gist.github.com/abc123",
                "id": "abc123",
            }
        ).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        response = self.client.post(
            reverse("create_gist"),
            data=json.dumps({"content": "test content", "token": "ghp_valid123"}),
            content_type="application/json",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == "https://gist.github.com/abc123"
        assert data["id"] == "abc123"

    @patch("generator.views.urllib.request.urlopen")
    def test_create_gist_sends_correct_payload(self, mock_urlopen):
        """A requisição para a API do GitHub contém os dados corretos (Bearer token, content, AGENTS.md)."""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(
            {
                "html_url": "https://gist.github.com/abc",
                "id": "abc",
            }
        ).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        self.client.post(
            reverse("create_gist"),
            data=json.dumps({"content": "my content", "token": "ghp_token"}),
            content_type="application/json",
        )

        call_args = mock_urlopen.call_args[0][0]
        sent_payload = json.loads(call_args.data)
        assert sent_payload["files"]["AGENTS.md"]["content"] == "my content"
        assert sent_payload["public"] is False
        assert call_args.headers["Authorization"] == "Bearer ghp_token"
        assert call_args.method == "POST"

    @patch("generator.views.urllib.request.urlopen")
    def test_create_gist_http_error(self, mock_urlopen):
        """Erro HTTP da API do GitHub (ex: 401) é tratado e retornado ao usuário."""
        fp_mock = MagicMock()
        fp_mock.read.return_value = b'{"message": "Bad credentials"}'
        mock_urlopen.side_effect = HTTPError(
            url="https://api.github.com/gists",
            code=401,
            msg="Unauthorized",
            hdrs=Message(),
            fp=fp_mock,
        )

        response = self.client.post(
            reverse("create_gist"),
            data=json.dumps({"content": "test", "token": "bad_token"}),
            content_type="application/json",
        )
        assert response.status_code == 401
        assert "GitHub API error" in response.json()["error"]

    @patch("generator.views.urllib.request.urlopen")
    def test_create_gist_network_error(self, mock_urlopen):
        """Erro de rede ao contactar a API do GitHub retorna 502."""
        mock_urlopen.side_effect = URLError(reason="Connection refused")

        response = self.client.post(
            reverse("create_gist"),
            data=json.dumps({"content": "test", "token": "valid_token"}),
            content_type="application/json",
        )
        assert response.status_code == 502
        assert "Network error" in response.json()["error"]


class TechFormTests(TestCase):
    def test_form_valid(self):
        """Formulário é válido com tecnologias e idioma pt."""
        form = TechForm(data={"technologies": "python, django", "language": "pt"})
        assert form.is_valid()

    def test_form_valid_en(self):
        """Formulário é válido com tecnologias e idioma en."""
        form = TechForm(data={"technologies": "python", "language": "en"})
        assert form.is_valid()

    def test_form_missing_technologies(self):
        """Formulário sem tecnologias é inválido."""
        form = TechForm(data={"language": "pt"})
        assert not form.is_valid()

    def test_form_invalid_language(self):
        """Formulário com idioma inválido (de) é inválido."""
        form = TechForm(data={"technologies": "python", "language": "de"})
        assert not form.is_valid()

    def test_form_empty_technologies_is_invalid(self):
        """Formulário com tecnologias vazias é inválido."""
        form = TechForm(data={"technologies": "", "language": "pt"})
        assert not form.is_valid()

    def test_form_initial_language_is_pt(self):
        """O valor inicial do campo language é 'pt'."""
        form = TechForm()
        assert form.fields["language"].initial == "pt"


class URLTests(TestCase):
    def test_index_url_resolves(self):
        """Rota / resulta em reverse('index')."""
        assert reverse("index") == "/"

    def test_result_url_resolves(self):
        """Rota /result/ resulta em reverse('result')."""
        assert reverse("result") == "/result/"

    def test_download_url_resolves(self):
        """Rota /download/ resulta em reverse('download')."""
        assert reverse("download") == "/download/"

    def test_create_gist_url_resolves(self):
        """Rota /create-gist/ resulta em reverse('create_gist')."""
        assert reverse("create_gist") == "/create-gist/"

    def test_index_status_code(self):
        """GET / retorna status 200."""
        response = self.client.get("/")
        assert response.status_code == 200

    def test_unknown_url_returns_404(self):
        """Rota inexistente retorna 404."""
        response = self.client.get("/nonexistent-page/")
        assert response.status_code == 404
