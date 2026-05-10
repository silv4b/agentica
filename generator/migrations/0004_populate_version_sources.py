import json
from pathlib import Path

from django.db import migrations

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def populate_version_sources(apps, schema_editor):
    Technology = apps.get_model("generator", "Technology")
    path = BASE_DIR / "tech_config.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for key, info in data.items():
        version_source = info.get("version_source", "")
        if version_source:
            Technology.objects.filter(key=key).update(version_source=version_source)


def reverse_func(apps, schema_editor):
    Technology = apps.get_model("generator", "Technology")
    Technology.objects.all().update(version_source="", latest_version="", version_checked_at=None)


class Migration(migrations.Migration):
    dependencies = [
        ("generator", "0003_technology_latest_version_and_more"),
    ]

    operations = [
        migrations.RunPython(populate_version_sources, reverse_func),
    ]
