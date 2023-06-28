from django.contrib import admin
from .models import User,Answer,Question,QuizCategories,Quiz,QuizSet,Exam,Caracteristics


something = [User,Answer,Question,QuizCategories,Quiz,QuizSet,Exam,Caracteristics]

for i in something:
    admin.site.register(i)