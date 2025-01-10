from django.urls import path
from .views import login, register
urlpatterns = [
    path('login/',login,name='user_login'),
    path('register/',register,name='user_register'),
]
