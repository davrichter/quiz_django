"""
    views for quiz_app
"""
import io
import math

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.contrib import messages
from django.shortcuts import get_object_or_404

from PIL import Image

from . import forms
from . import models


# Create your views here.

class IndexView(ListView):
    model = models.Quiz
    template_name = 'quiz_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateQuizView(FormView):
    """view for creating a quiz"""
    template_name = 'quiz_app/create_quiz.html'
    form_class = forms.CreateQuizForm
    success_url = '/accounts/login/'

    def form_valid(self, form):
        title = self.request.POST['title']
        user = self.request.user

        thumbnail = self.request.FILES['thumbnail']

        if thumbnail.multiple_chunks():
            """if the image is larger than 2.5 megabyte return with an error message"""
            messages.add_message(self.request, messages.ERROR, "Images can't be larger than 2.5 Megabytes.")
            return HttpResponseRedirect(reverse('CreateQuizView'))

        quiz = models.Quiz.objects.create(
            title=title,
            user=user,
            thumbnail=thumbnail
        )

        quiz.save()

        return HttpResponseRedirect(reverse('IndexView'))

    def form_invalid(self, form):
        print(self.request.POST)

        return HttpResponseRedirect(reverse('IndexView'))


def quiz_view(request, quiz_id):
    """view for viewing a quiz"""
    quiz = get_object_or_404(models.Quiz, pk=quiz_id)
    questions = models.Question.objects.filter(quiz=quiz)

    return HttpResponse(render(request, 'quiz_app/show_quiz.html', context={
        'quiz': quiz,
        'questions': questions
    }))
