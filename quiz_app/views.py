"""
    Views for quiz_app.
"""
import os

import PIL
from django.utils import datastructures
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
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

            if request.FILES['thumbnail']:
                try:
                    thumbnail = request.FILES['thumbnail']

                    if thumbnail.multiple_chunks():
                        """if the image is larger than 2.5 megabyte return with an error message"""
                        messages.add_message(request, messages.ERROR, "Images can't be larger than 2.5 Megabytes.")
                        return HttpResponseRedirect(reverse('IndexView'))
                    else:
                        try:
                            os.remove(f"{os.getcwd()}{settings.MEDIA_URL}{quiz.thumbnail}")
                        except FileNotFoundError:
                            pass

                        quiz.thumbnail = thumbnail

                except datastructures.MultiValueDictKeyError:
                    pass

            try:
                quiz.save()

            except PIL.UnidentifiedImageError:
                messages.add_message(request, messages.ERROR, "Unknown filetype.")
                return HttpResponseRedirect(reverse('IndexView'))

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
    options = []

    for i in range(0, len(questions)):
        options.append(models.Option.objects.filter(Question=questions[i]))

    return HttpResponse(render(request, 'quiz_app/show_quiz.html', context={
        'quiz': quiz,
        'questions': questions,
        'options': options,
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


def edit_question(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)

    if get_object_or_404(models.Quiz, pk=question.quiz.id).user == request.user:
        if request.POST:
            question.title = request.POST["title"]
            print(request.POST["time"])
            question.time = int(request.POST["time"])

            question.save()

            return HttpResponseRedirect(reverse('IndexView'))

        else:
            return HttpResponse(render(request, 'quiz_app/edit_question.html', context={
                'question': question
            }))

    else:
        return render(request, 'quiz_app/no_permission.html')


def create_question(request, quiz_id):
    if request.user == (get_object_or_404(models.Quiz, pk=quiz_id)).user:
        if request.POST:
            question = models.Question.objects.create(
                time=request.POST["time"],
                title=request.POST["title"],
                quiz=get_object_or_404(models.Quiz, pk=quiz_id),
            )

            question.save()

            return HttpResponseRedirect(reverse('EditQuizView', args=(quiz_id,)))

        else:
            return HttpResponse(render(request, 'quiz_app/create_question.html', context={
                'quiz': get_object_or_404(models.Quiz, pk=quiz_id),
            }))
    else:
        return render(request, 'quiz_app/no_permission.html')


def delete_question(request, question_id):
    question = get_object_or_404(models.Question, pk=question_id)

    if get_object_or_404(models.Quiz, pk=question.quiz.id).user == request.user:
        question.delete()

        return HttpResponseRedirect(reverse('EditQuizView', args=(question.quiz.id,)))
    else:
        return render(request, 'quiz_app/no_permission.html')


def edit_option(request, option_id):
    question = get_object_or_404(models.Question, pk=option_id)

    if get_object_or_404(models.Quiz, pk=question.quiz.id).user == request.user:
        if request.POST:
            question.title = request.POST["title"]
            print(request.POST["time"])
            question.time = int(request.POST["time"])

            question.save()

            return HttpResponseRedirect(reverse('IndexView'))

        else:
            return HttpResponse(render(request, 'quiz_app/edit_question.html', context={
                'question': question
            }))

    else:
        return render(request, 'quiz_app/no_permission.html')


def create_option(request, question_id):
    if request.user == (get_object_or_404(models.Quiz, pk=question_id)).user:
        if request.POST:
            question = models.Question.objects.create(
                time=request.POST["time"],
                title=request.POST["title"],
                quiz=get_object_or_404(models.Quiz, pk=question_id),
            )

            question.save()

            return HttpResponseRedirect(reverse('EditQuizView', args=(question_id,)))

        else:
            return HttpResponse(render(request, 'quiz_app/create_question.html', context={
                'quiz': get_object_or_404(models.Quiz, pk=question_id),
            }))
    else:
        return render(request, 'quiz_app/no_permission.html')


def delete_option(request, option_id):
    question = get_object_or_404(models.Question, pk=option_id)

    if get_object_or_404(models.Quiz, pk=question.quiz.id).user == request.user:
        question.delete()

        return HttpResponseRedirect(reverse('EditQuizView', args=(question.quiz.id,)))
    else:
        return render(request, 'quiz_app/no_permission.html')
