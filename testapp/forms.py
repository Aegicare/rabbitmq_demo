from django import forms
from .models import Calcu


class SubmitForm(forms.ModelForm):
    class Meta:
        model = Calcu
        fields = [
            "n",
        ]
