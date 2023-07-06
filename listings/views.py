from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login as login2,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from listings.models import Quiz, Answer, QuizSet, Question, UserQuizProgress


def results(request,score):

    return render(request,'listings/result.html',{'score':score})

def four0four(request,exception):

    return render(request,'listings/404.html',status=404)

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
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        #send to the error page
        return redirect('main-home-page')
    
    
    user_quiz, created = UserQuizProgress.objects.get_or_create(user=user, quiz=quiz)


    if created:

        current_question = user_quiz.get_current_question()

        return redirect('single-quiz', quiz_id=quiz.id, question_id=1)
    
    else:
        current_question = user_quiz.get_current_question()
        if not current_question:
            return redirect('results-quiz',score=user_quiz.score)
    
    

    # Otherwise, redirect to the quiz view
    return redirect('single-quiz', quiz_id=quiz.id, question_id=1)

@login_required
def quiz_view(request, quiz_id, question_id):


    user = request.user
    print(quiz_id)
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except Quiz.DoesNotExist:
        #send to the error page
        print("i am here hahaha")
        return redirect('main-home-page')

    try:
        userquiz = UserQuizProgress.objects.get(user=user,quiz=quiz)
    except UserQuizProgress.DoesNotExist:
        #send to the error page
        return redirect('main-home-page')
    

    
    
        # Check if all questions in the quiz are done
    # if quiz.check_completion():
    #     # If all questions are done, redirect to the score view
    #     return redirect('score_view', quiz_id=quiz_id)

    current_question = userquiz.get_next_question()
    if not current_question:
        return redirect('results-quiz',score=userquiz.score)
    current_question_index = userquiz.current_question_index


    questions = list(quiz.questions.all())


    if request.method == 'POST':
        # Verify answer and mark question as done here
        # You may need to adjust this to fit your answer submission form
        answer_id = request.POST.get('answer')
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            userquiz.mark_question_done()
            userquiz.save()
        # Check if the answer is correct
        userquiz.mark_question_done()
        userquiz.save()
        # Otherwise, redirect to the next question
        next_question = quiz.get_next_question()
        
        return redirect('single-quiz', quiz_id=quiz_id, question_id=5)

    return render(request, 'listings/question.html', {
        'quiz': quiz,
        'questions': questions,
        'current_question': current_question,
        'current_question_index': current_question_index,
    })


