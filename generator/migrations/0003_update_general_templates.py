from django.db import migrations

from generator.template_data import TEMPLATES


def update_general_templates(apps, schema_editor):
    Template = apps.get_model("generator", "Template")
    for lang in ("en", "pt"):
        content = TEMPLATES[lang]["general"]
        Template.objects.filter(technology__isnull=True, language=lang).update(content=content)


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("generator", "0002_populate_initial_data"),
    ]

    operations = [
        migrations.RunPython(update_general_templates, reverse_func),
    ]
