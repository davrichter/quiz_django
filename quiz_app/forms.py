"""
    forms for the quit_app
"""

from django import forms

from authentication.models import User


class CreateQuizForm(forms.Form):
    """form for validating the input while when the user creates a quiz"""
    title = forms.CharField(max_length=100)
    user = forms.ModelChoiceField(queryset=User)
