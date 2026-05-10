from django import forms


class TechForm(forms.Form):
    """Formulário para entrada de tecnologias."""

    technologies = forms.CharField(
        label="Tecnologias",
        widget=forms.HiddenInput(),
    )
