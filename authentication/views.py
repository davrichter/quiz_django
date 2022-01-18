from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormView

from . import forms
from . import models


# Create your views here.

class CreateUserView(FormView):
    template_name = 'registration/create_user.html'
    form_class = forms.CreateUserForm
    success_url = '/accounts/login/'

    def form_valid(self, form):
        username = self.request.POST["username"]
        password = self.request.POST["password"]

        user = models.User.objects.create_user(username=username, password=password)
        user.save()

        return HttpResponseRedirect(reverse('login'))
