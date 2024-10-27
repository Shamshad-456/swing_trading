# accounts/urls.py
from django.urls import path
from .views import create_user, update_user, delete_user

urlpatterns = [
    path('users/create/', create_user, name='create_user'),
    path('users/update/<int:user_id>/', update_user, name='update_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
]
