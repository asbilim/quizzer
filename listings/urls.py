from .views import signin,register,home,quizset,exam,quiz_view,activate_quiz,results,reset_quiz
from django.urls import path

urlpatterns = [
    path("login",signin,name="auth-login"),
    path("register",register,name="auth-register"),
    path("",home,name="main-home-page"),
    path("quizset",quizset,name="quizset"),
    path("exam",exam,name="exam"),
    path("quiz/<int:quiz_id>/<int:question_id>",quiz_view,name="single-quiz"),
    path("quiz/<int:quiz_id>/",activate_quiz,name="activate-quiz"),
    path("results/<int:score>/<int:quiz>",results,name="results-quiz"),
    path("reset/<int:quiz_id>/",reset_quiz,name="reset-quiz"),

]
