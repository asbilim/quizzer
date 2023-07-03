from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login as login2,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from listings.models import Quiz,Answer,QuizSet,Question

def home(request):

    all_quizzes = Quiz.objects.all()
    print(all_quizzes[0])
    return render(request, 'listings/home.html',{"quizzes":all_quizzes})

def quizset(request):

    return render(request, 'listings/quizset.html')

def exam(request):

    return render(request, 'listings/exams.html')


def signin(request):

    if request.user.is_authenticated:

        return redirect('main-home-page')

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        if len(username) and len(password):

            user = authenticate(username=username, password=password)
            if user is not None:
                login2(request, user)
                return redirect('main-home-page')
        
    
    return render(request,'listings/auth/login.html')


def register(request):

    if request.user.is_authenticated:

        return redirect('main-home-page')
    
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']
        User = get_user_model()

        if confirm != password:
            return render(request,'listings/auth/register.html')
        
        user = User.objects.create(username=username, password=password)

        if user:
            login2(request, user)
            return redirect('main-home-page')

    
    return render(request,'listings/auth/register.html')


def signout(request):

    if request.user.is_authenticated:

        logout(request)
        return redirect('auth-login')


@login_required
def activate_quiz(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    # Check if the user is already assigned to this quiz
    if quiz not in user.quizzes.all():
        # If not, assign the quiz to the user
        user.quizzes.add(quiz)

    # Check if all questions in the quiz are done
    if quiz.check_completion():
        # If all questions are done, redirect to the score view
        return redirect('score_view', quiz_id=quiz_id)

    # Otherwise, redirect to the quiz view
    return redirect('single-quiz', quiz_id=quiz_id, question_id=1)

@login_required
def quiz_view(request, quiz_id, question_id):
    user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    # Ensure the quiz is assigned to the user
    if quiz not in user.quizzes.all():
        return redirect('main-home-page')  # Or however you want to handle this case

    questions = list(quiz.questions.all())

    if question_id is None:
        current_question_index = 0
        current_question = questions[current_question_index]
    else:
        current_question = get_object_or_404(Question, pk=question_id)
        if current_question not in questions:
            return render(request, '404.html')  # Or however you want to handle this case
        current_question_index = questions.index(current_question)

    if request.method == 'POST':
        # Verify answer and mark question as done here
        # You may need to adjust this to fit your answer submission form
        answer_id = request.POST.get('answer_id')
        answer = get_object_or_404(Answer, pk=answer_id)

        # Check if the answer is correct
        if answer in current_question.answers.all() and answer.is_correct:
            # If the answer is correct, mark the question as done
            current_question.is_done = True
            current_question.save()

        # Check if all questions in the quiz are done
        if quiz.check_completion():
            # If all questions are done, redirect to the score view
            return redirect('score_view', quiz_id=quiz_id)
        
        # Otherwise, redirect to the next question
        next_question = quiz.get_next_question()
        return redirect('quiz_view', quiz_id=quiz_id, question_id=next_question.id)

    return render(request, 'listings/question.html', {
        'quiz': quiz,
        'questions': questions,
        'current_question': current_question,
        'current_question_index': current_question_index,
    })


