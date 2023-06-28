from .views import signin,register,home
from django.urls import path

urlpatterns = [
    path("login",signin,name="auth-login"),
    path("register",register,name="auth-register"),
    path("",home,name="main-home-page"),
]
