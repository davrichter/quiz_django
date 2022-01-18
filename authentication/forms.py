from django import forms


class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128)
