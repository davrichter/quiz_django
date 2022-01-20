"""
    views for quiz_app
"""

from django.http import HttpResponseRedirect
from django.urls import reverse
# from django.views.generic.edit import FormView
from django.views.generic.list import ListView

# from . import forms
from . import models


# Create your views here.

class IndexView(ListView):
    model = models.Quiz
    template_name = 'quiz_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
