from django.urls import path, include

from . import views

urlpatterns = [
    path('create_user/', views.CreateUserView.as_view(), name="CreateUser"),
    path('profile/<int:user_id>', views.view_user_profile, name="ViewUser"),
    path('profile/', views.view_user_profile, name="ViewUserNoParams"),
    path('', include('django.contrib.auth.urls')),
]
