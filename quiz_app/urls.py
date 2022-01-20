""" quiz_django URL Configuration

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""

from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='IndexView')
]
