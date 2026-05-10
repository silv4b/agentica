from django.db import migrations


def fix_python_version_source(apps, schema_editor):
    Technology = apps.get_model("generator", "Technology")
    Technology.objects.filter(key="python").update(version_source="github:python/cpython")


def reverse_func(apps, schema_editor):
    Technology = apps.get_model("generator", "Technology")
    Technology.objects.filter(key="python").update(version_source="pypi:python")


class Migration(migrations.Migration):
    dependencies = [
        ("generator", "0004_populate_version_sources"),
    ]

    operations = [
        migrations.RunPython(fix_python_version_source, reverse_func),
    ]
