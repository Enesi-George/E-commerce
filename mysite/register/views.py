from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was successfully created')
            return redirect("/login")
    else:
         form = RegisterForm()
    
    return render(request, "register/register.html", {"form":form})

def loginpage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/store')
        else:
            messages.info(request, 'Username or Password is incorrect')
        
    context={}
    return render(request,'registration/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/login')