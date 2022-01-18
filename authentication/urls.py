from django.urls import path, include

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # path('accounts/create_user', )
]
