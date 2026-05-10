from django.db import models


class Technology(models.Model):
    key = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    run_command = models.CharField(max_length=200, blank=True)
    test_command = models.CharField(max_length=200, blank=True)
    lint_command = models.CharField(max_length=200, blank=True)
    style_command = models.CharField(max_length=200, blank=True)
    devicon = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "technologies"
        ordering = ["key"]

    def __str__(self):
        """Retorna o nome de exibição da tecnologia."""
        return self.display_name


class Template(models.Model):
    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    language = models.CharField(max_length=5)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["language", "technology__key"]
        unique_together = [("technology", "language")]

    def __str__(self):
        """Retorna uma representação legível do template com tecnologia e idioma."""
        if self.technology:
            return f"{self.technology.key} ({self.language})"
        return f"general ({self.language})"
