from django.contrib import admin
from .models import User,Answer,Question,QuizCategories,Quiz,QuizSet,Exam,Caracteristics,UserQuizProgress


something = [User,Answer,Question,QuizCategories,Quiz,QuizSet,Exam,Caracteristics,UserQuizProgress]

for i in something:
    admin.site.register(i)