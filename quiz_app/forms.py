"""
    forms for the quit_app
"""

from django import forms

from authentication.models import User


class CreateQuizForm(forms.Form):
    """form for validating the input while when the user creates a quiz"""
    title = forms.CharField(max_length=100)
    thumbnail = forms.ImageField()


class CreateQuestionForm(forms.Form):
    title = forms.CharField(max_length=200)
    time = forms.IntegerField(
        verbose_name="Time to solve the question",
        name="Time",
        null=True
    )
