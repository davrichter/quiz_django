from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormView

from . import forms
from . import models


# Create your views here.

class CreateQuizView(FormView):
    template_name = 'registration/create_user.html'
    form_class = forms.CreateQuizForm
    success_url = '/accounts/login/'

    def form_valid(self, form):
        return HttpResponseRedirect(reverse('login'))
