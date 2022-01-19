from django import forms

from authentication.models import User


class CreateQuizForm(forms.Form):
    title = forms.CharField(max_length=100)
    user = forms.ModelChoiceField(queryset=User)
