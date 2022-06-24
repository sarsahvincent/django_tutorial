import email
from fractions import Fraction
import re
from django.shortcuts import render, redirect
from requests import request
from .models import Feature
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def index(request):
    features = Feature.objects.all()
    feature1 = Feature()
    feature1.id = 0
    feature1.name = 'Fast'
    feature1.details = 'this is to test the details of the page'
    return render(request, 'index.html', {'features': features})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Used')
                return redirect('register')
            else:
                user = User.objects.create(
                    username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')


def counter(request):
    words = request.POST['words']
    word_len = len(words.split())
    return render(request, 'counter.html', {'amount': word_len})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentails invalid')
            return redirect('login')

    else:
        return render(request, 'login.html')
