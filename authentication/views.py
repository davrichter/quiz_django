from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.shortcuts import get_object_or_404

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

        if first_name and last_name:
            user = models.User.objects.create_user(username=username,
                                                   password=password,
                                                   first_name=first_name,
                                                   last_name=last_name)
            user.save()

        elif first_name:
            user = models.User.objects.create_user(username=username,
                                                   password=password,
                                                   first_name=first_name)
            user.save()

        elif last_name:
            user = models.User.objects.create_user(username=username,
                                                   password=password,
                                                   last_name=last_name)
            user.save()

        else:
            user = models.User.objects.create_user(username=username,
                                                   password=password,)
            user.save()

        return HttpResponseRedirect(reverse('login'))


def view_user_profile(request, user_id):
    user = get_object_or_404(models.User, pk=user_id)

    return HttpResponse(render(request, 'registration/profile.html', context={'profile_user': user}))
