from .views import signin,register,home,quizset,exam
from django.urls import path

urlpatterns = [
    path("login",signin,name="auth-login"),
    path("register",register,name="auth-register"),
    path("",home,name="main-home-page"),
    path("quizset",quizset,name="quizset"),
    path("exam",exam,name="exam"),
]
