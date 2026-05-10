import json
from pathlib import Path

from django.db import migrations

from generator.template_data import TEMPLATES

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TECH_CONFIG_PATH = BASE_DIR / "tech_config.json"


def load_tech_config(apps, schema_editor):
    Technology = apps.get_model("generator", "Technology")
    with open(TECH_CONFIG_PATH, encoding="utf-8") as f:
        data = json.load(f)
    objs = []
    for key, info in data.items():
        objs.append(
            Technology(
                key=key,
                display_name=info.get("display_name", key.capitalize()),
                run_command=info.get("run", ""),
                test_command=info.get("test", ""),
                lint_command=info.get("lint", ""),
                style_command=info.get("style", ""),
                devicon=info.get("devicon", ""),
            )
        )
    Technology.objects.bulk_create(objs)


def load_templates(apps, schema_editor):
    Technology = apps.get_model("generator", "Technology")
    Template = apps.get_model("generator", "Template")

    tech_map = {t.key: t for t in Technology.objects.all()}

    for lang in ("en", "pt"):
        for stem, content in TEMPLATES[lang].items():
            tech = tech_map.get(stem)
            Template.objects.create(
                technology=tech,
                language=lang,
                content=content,
            )


def reverse_func(apps, schema_editor):
    Technology = apps.get_model("generator", "Technology")
    Template = apps.get_model("generator", "Template")
    Template.objects.all().delete()
    Technology.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("generator", "0001_initial_models"),
    ]

    operations = [
        migrations.RunPython(load_tech_config, reverse_func),
        migrations.RunPython(load_templates, reverse_func),
    ]
