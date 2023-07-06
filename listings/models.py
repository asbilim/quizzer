from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.serializers import serialize,deserialize

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
    
    def get_completed_quizzes(self):
        """
        Returns all quizzes that the user has completed (all questions done).
        """
        return self.quizzes.filter(questions__is_done=True)

    def get_passed_exams(self):
        """
        Returns all exams that the user has passed.
        """
        return self.exams.filter(has_passed=True)

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
    is_done = models.BooleanField(default=False)
    is_correct = models.BooleanField(default=False,null=True,blank=True)

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
    final_score = models.IntegerField(blank=True,null=True)
    image = models.ImageField(blank=True, upload_to="media/quiz/")
    difficulty_level = models.CharField(max_length=1, choices=DIFFICULTY_LEVELS, blank=True)

    def __str__(self):
        return self.name
    
    def compute_score(self):
        """
        Computes the score of the quiz by summing the value of the questions that are done and correctly answered.
        Assumes question_value attribute on Question model.
        """
        total_score = 0
        for question in self.questions.filter(is_done=True):
            if question.answers.filter(is_correct=True).exists():
                total_score += question.question_value
        return total_score
    
    def check_completion(self):
        """
        Check if all questions in the quiz have been done.
        """
        return self.questions.filter(is_done=False).count() == 0

    def get_next_question(self):
        """
        Returns the next question in the quiz that needs to be done.
        """
        return self.questions.filter(is_done=False).first()


class UserQuizProgress(models.Model):
    """
    Model representing a user's progress in a quiz.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,null=True)
    current_question_index = models.IntegerField(default=0)
    is_done = models.BooleanField(default=False)
    is_correct = models.BooleanField(default=False, null=True, blank=True)
    questions = models.TextField(blank=True, null=True,default='')
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.name}'


    def get_current_question(self):
        # Retrieve the current question
        questions = list(self.quiz.questions.all())
        if self.current_question_index < len(questions):
            return questions[self.current_question_index]
        return None

    def get_unanswered_questions(self):
        return self.quiz.questions.filter(is_done=False)

    def get_correctly_answered_questions(self):
        return self.quiz.questions.filter(is_correct=True)

    def get_incorrectly_answered_questions(self):
        return self.quiz.questions.filter(is_done=True, is_correct=False)

    def get_score(self):
        return self.get_correctly_answered_questions().count()

    def get_total_questions(self):
        return self.quiz.questions.count()

    def get_progress(self):
        total_questions = self.get_total_questions()
        if total_questions == 0:
            return 0
        return 100 * self.quiz.questions.filter(is_done=True).count() / total_questions

    def is_complete(self):
        self.is_done

    def get_next_question(self):
        questions = list(self.quiz.questions.all())
        if self.current_question_index < len(questions):
            return questions[self.current_question_index]
        return None

    def mark_question_done(self):
        
        if self.current_question_index == len(list(self.quiz.questions.all())) - 1:
            self.score += self.quiz.question_value
            self.is_done = True
        self.current_question_index += 1
        self.save()

    def reset(self):
        self.current_question_index = 0
        self.score = 0
        self.save()
        self.initialize_questions()


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
        ('17', 'Front End'),
        ('18', 'Back End'),
        ('19', 'Full Stack'),
        ('20', 'Web Development'),
        ('21', 'Mobile Development'),
        ('22', 'Database'),
        ('23', 'API'),
        ('24', 'Open Source'),
        ('25', 'Security'),
        ('26', 'DevOps'),
        ('27', 'System Design'),
        ('28', 'Algorithms'),
        ('29', 'Data Structures'),
        ('30', 'Software Design'),
        ('31', 'Software Engineering'),
        ('32', 'Version Control'),
        ('33', 'Testing'),
        ('34', 'Debugging'),
        ('35', 'Cloud'),
        ('36', 'Programming Languages'),
        ('37', 'Problem Solving'),
        ('38', 'Game Development'),
        ('39', 'UI/UX'),
        ('40', 'Software Architecture'),
        ('17', 'JavaScript'),
        ('181', 'Python'),
        ('191', 'Java'),
        ('201', 'C++'),
        ('211', 'PHP'),
        ('221', 'HTML'),
        ('231', 'CSS'),
        ('241', 'SQL'),
        ('251', 'Ruby'),
        ('261', 'C#'),
        ('271', 'C'),
        ('281', 'React'),
        ('291', 'Angular'),
        ('301', 'jQuery'),
        ('311', 'Android'),
        ('321', 'iOS'),
        ('331', 'Swift'),
        ('341', 'Node.js'),
        ('351', 'ASP.NET'),
        ('361', 'Linux'),
        ('371', 'Shell'),
        ('381', 'Algorithms'),
        ('391', 'Data structures'),
        ('401', 'Programming fundamentals')

    ]

    caracteristics = models.CharField(
        max_length=5,
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
    exams = models.ManyToManyField(Exam,null=True,blank=True)
    description = models.TextField(blank=True)
    # Add a foreign key to Caracteristics
    caracteristics = models.ManyToManyField(Caracteristics)

    def __str__(self):
        return self.name
    
    def get_total_score(self):
        """
        Computes the total score of the QuizSet by summing the scores of all quizzes.
        """
        return sum([quiz.compute_score() for quiz in self.quizzes.all()])

    def get_average_score(self):
        """
        Computes the average score of the QuizSet.
        """
        total_score = self.get_total_score()
        return total_score / self.quizzes.count() if self.quizzes.count() > 0 else 0


