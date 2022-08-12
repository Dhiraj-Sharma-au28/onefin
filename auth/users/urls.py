from django.contrib import admin
from django.urls import path
from .views import RegisterView,LoginView,UserView,MoviesView


urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('collection',UserView.as_view()),
    path('movies',MoviesView.as_view())
]