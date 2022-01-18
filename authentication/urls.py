from django.urls import path, include

from . import views

urlpatterns = [
    path('create_user/', views.CreateUserView.as_view(), name="CreateUser"),
    path('', include('django.contrib.auth.urls')),
]
