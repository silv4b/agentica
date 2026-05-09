from django import forms

LANG_CHOICES = [
    ("pt", "Português"),
    ("en", "English"),
]


class TechForm(forms.Form):
    """Formulário para entrada de tecnologias e idioma pelo usuário."""

    technologies = forms.CharField(
        label="Tecnologias",
        widget=forms.HiddenInput(),
    )
    language = forms.ChoiceField(
        choices=LANG_CHOICES,
        initial="pt",
        widget=forms.HiddenInput(),
    )
