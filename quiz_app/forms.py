"""
    forms for the quit_app
"""

from django import forms


class CreateQuizForm(forms.Form):
    """form for validating the input while when the user creates a quiz"""
    title = forms.CharField(max_length=100)
    thumbnail = forms.ImageField()


class CreateQuestionForm(forms.Form):
    title = forms.CharField(max_length=200)
    time = forms.IntegerField()
