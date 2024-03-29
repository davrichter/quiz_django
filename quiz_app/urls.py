""" quiz_django URL Configuration

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='IndexView'),
    path('quiz/create/', views.CreateQuizView.as_view(), name='CreateQuizView'),
    path('quiz/edit/<int:quiz_id>/', views.edit_quiz_view, name='EditQuizView'),
    path('quiz/delete/<int:quiz_id>/', views.quiz_delete, name='DeleteQuiz'),
    path('quiz/view/<int:quiz_id>/', views.quiz_view, name='QuizView'),
    path('question/edit/<int:question_id>', views.edit_question, name='EditQuestionView'),
    path('question/create/<int:quiz_id>', views.create_question, name='CreateQuestionView'),
    path('question/delete/<int:question_id>', views.delete_question, name='DeleteQuestionView'),
]
