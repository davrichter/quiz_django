from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.contrib import messages

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
        first_name = self.request.POST["first_name"]
        last_name = self.request.POST["last_name"]

        try:
            user = models.User.objects.create_user(username=username,
                                                   password=password,
                                                   first_name=first_name,
                                                   last_name=last_name)
            user.save()

            return HttpResponseRedirect(reverse('login'))
        except IntegrityError:
            messages.add_message(self.request, messages.ERROR, 'This username is already taken.')
            return HttpResponseRedirect(reverse('CreateUser'))


def view_user_profile(request, user_id):
    user = get_object_or_404(models.User, pk=user_id)

    return HttpResponse(render(request, 'registration/profile.html', context={'profile_user': user}))
