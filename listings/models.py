from django.db import models
from django.contrib.auth.models import AbstractUser

# Constants for choices
QUESTION_TYPES = (
    ('MC', 'Multiple Choice'),
    ('TF', 'True/False'),
    ('SA', 'Short Answer'),
)

DIFFICULTY_LEVELS = (
    ('E', 'Easy'),
    ('M', 'Medium'),
    ('H', 'Hard'),
)

# User model
class User(AbstractUser):
    """
    Custom User model, extends from Django's Abstract User.
    A user can take multiple exams and quizzes.
    """
    exams = models.ManyToManyField('Exam',related_name="user_exams")
    quizzes = models.ManyToManyField('Quiz')

    def __str__(self):
        return self.username

# Quiz related models
class QuizCategories(models.Model):
    """
    Model representing different categories a quiz can belong to.
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Answer(models.Model):
    """
    Model representing a possible answer to a question. 
    """
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} {'correct' if self.is_correct else 'not correct'}"

class Question(models.Model):
    """
    Model representing a question in the quiz.
    """
    text = models.CharField(max_length=3000)
    question_type = models.CharField(max_length=2, choices=QUESTION_TYPES)
    category = models.ForeignKey(QuizCategories, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answers = models.ManyToManyField(Answer, blank=True)
    is_done = models.BooleanField(default=True)

    def __str__(self):
        return self.text

class Quiz(models.Model):
    """
    Model representing a quiz. A quiz is a set of questions.
    """
    name = models.CharField(max_length=50)
    question_time = models.IntegerField(default=60)
    questions = models.ManyToManyField(Question)
    question_value = models.IntegerField()
    description = models.TextField(blank=True)
    final_score = models.IntegerField(blank=True)
    image = models.ImageField(blank=True, upload_to="media/quiz/")
    difficulty_level = models.CharField(max_length=1, choices=DIFFICULTY_LEVELS, blank=True)

    def __str__(self):
        return self.name

# Exam related models
class Exam(models.Model):
    """
    Model representing an exam. An exam is a set of quizzes.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quizzes = models.ManyToManyField(Quiz)
    created_at = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField()
    has_passed = models.BooleanField(default=False)
    is_graded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} took exam on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class Caracteristics(models.Model):
    """
    Model representing the characteristics of a QuizSet.
    """
    CARACTERISTICS_CHOICES = [
        ('1', 'Easy'),
        ('2', 'Medium'),
        ('3', 'Hard'),
        ('4', 'Science'),
        ('5', 'Mathematics'),
        ('6', 'History'),
        ('7', 'Geography'),
        ('8', 'Literature'),
        ('9', 'Physics'),
        ('10', 'Chemistry'),
        ('11', 'Biology'),
        ('12', 'Computer Science'),
        ('13', 'Art'),
        ('14', 'Music'),
        ('15', 'Sports'),
        ('16', 'Networking'),
        ('15', 'Database'),
    ]

    caracteristics = models.CharField(
        max_length=2,
        choices=CARACTERISTICS_CHOICES,
        default='1',
    )

    def __str__(self):
        return self.get_caracteristics_display()

class QuizSet(models.Model):
    """
    Model representing a set of quizzes. 
    This can be used to group several quizzes together for an event or a particular study topic.
    """
    name = models.CharField(max_length=50)
    quizzes = models.ManyToManyField(Quiz)
    exams = models.ManyToManyField(Exam)
    description = models.TextField(blank=True)
    # Add a foreign key to Caracteristics
    caracteristics = models.ManyToManyField(Caracteristics)

    def __str__(self):
        return self.name

