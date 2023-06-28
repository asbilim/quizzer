from django.shortcuts import render,redirect
from django.contrib.auth import login as login2,authenticate,logout
from django.contrib.auth import get_user_model
from listings.models import Quiz,Answer

def home(request):

    return render(request, 'listings/home.html')


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
    
