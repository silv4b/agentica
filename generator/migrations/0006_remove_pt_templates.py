from django.db import migrations


def remove_pt_templates(apps, schema_editor):
    Template = apps.get_model("generator", "Template")
    deleted, _ = Template.objects.filter(language="pt").delete()
    print(f"Removed {deleted} PT templates from database")


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("generator", "0005_fix_python_version_source"),
    ]

    operations = [
        migrations.RunPython(remove_pt_templates, reverse_func),
    ]
