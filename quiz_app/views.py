"""
    Views for quiz_app.
"""
import os

from django.db.models import QuerySet
from django.utils import datastructures
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.base import ContextMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404

from quiz_django import settings
from . import forms
from . import models


# Create your views here.

class IndexView(ListView):
    """Index view for showing some Quizzes."""
    model = models.Quiz
    template_name = 'quiz_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateQuizView(FormView):
    """A view for creating a quiz."""
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
        messages.add_message(self.request, messages.ERROR, "There was an unknown error. Please try again.")
        return HttpResponseRedirect(reverse('CreateQuizView'))


def edit_quiz_view(request, quiz_id):
    """A view for editing a quiz and its questions."""
    quiz = get_object_or_404(models.Quiz, pk=quiz_id)
    if quiz.user == request.user:
        if request.POST:
            if request.POST['title']:
                quiz.title = request.POST['title']

            try:
                if request.FILES['thumbnail']:
                    thumbnail = request.FILES['thumbnail']

                    if thumbnail.multiple_chunks():
                        """if the image is larger than 2.5 megabyte return with an error message"""
                        messages.add_message(request, messages.ERROR, "Images can't be larger than 2.5 Megabytes.")
                        return HttpResponseRedirect(reverse('CreateQuizView'))
                    else:
                        os.remove(f"{os.getcwd()}{settings.MEDIA_URL}{quiz.thumbnail}")
                        quiz.thumbnail = thumbnail
            except datastructures.MultiValueDictKeyError:
                pass

            quiz.save()

        else:
            questions = models.Question.objects.filter(quiz=quiz)
            options = models.Option.objects.filter(Question__in=questions)

            return render(request, 'quiz_app/edit_quiz.html', {
                'quiz': quiz,
                'questions': questions,
                'options': options
            })

    else:
        return render(request, 'quiz_app/no_permission.html')

    return HttpResponseRedirect(reverse('IndexView'))


def quiz_view(request, quiz_id):
    """A view for viewing a quiz."""
    quiz = get_object_or_404(models.Quiz, pk=quiz_id)
    questions = models.Question.objects.filter(quiz=quiz)

    return HttpResponse(render(request, 'quiz_app/show_quiz.html', context={
        'quiz': quiz,
        'questions': questions
    }))


def quiz_delete(request, quiz_id):
    """A view for deleting a quiz."""
    quiz = get_object_or_404(models.Quiz, pk=quiz_id)
    if quiz.user == request.user:
        os.remove(f"{os.getcwd()}{settings.MEDIA_URL}{quiz.thumbnail}")
        quiz.delete()

        messages.add_message(request, messages.SUCCESS, "Quiz has been deleted.")
        return HttpResponseRedirect(reverse('IndexView'))
    else:
        messages.add_message(request, messages.ERROR, "You have no permission to delete this Quiz.")
        return HttpResponseRedirect(reverse('IndexView'))


def edit_questions(request, quiz_id):
    quiz = get_object_or_404(models.Quiz, pk=quiz_id)
    questions = models.Question.objects.filter(quiz=quiz)

    for i in request.POST:
        if 'QUESTION' in i:
            current_question = get_object_or_404(models.Question, id=i[8:])
            current_question.title = request.POST[i]
            current_question.save()

        elif 'OPTION' in i:
            current_option = get_object_or_404(models.Option, id=i[6:])
            current_option.text = request.POST[i]
            current_option.save()

        else:
            pass

    return HttpResponseRedirect(reverse('IndexView'))

