from django.contrib import admin

from .models import Technology, Template


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ["key", "display_name", "run_command"]
    search_fields = ["key", "display_name"]
    ordering = ["key"]


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ["tech_label", "language", "updated_at"]
    list_filter = ["language", "technology"]
    search_fields = ["technology__key", "technology__display_name"]

    @admin.display(description="Technology")
    def tech_label(self, obj):
        return str(obj)
