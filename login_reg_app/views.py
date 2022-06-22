from multiprocessing import context
from webbrowser import get
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "index.html")

def success(request):
    if not "user_id" in request.session:
        return redirect('/')
    else :
        context = {
            'user': User.objects.get(id = request.session['user_id']),
        }
    return render(request, "success.html", context)

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            email = request.POST['email']
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            newUser = User.objects.create(first_name = first_name, last_name = last_name, user_email=email, 
            password = pw_hash)
            newUser.save()
            request.session['user_id'] = newUser.id
            return redirect('/success')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            user_logged_in = User.objects.get(user_email=request.POST['email'])
            request.session['user_id'] = user_logged_in.id
            return redirect('/success')

def logout(request):
    del request.session['user_id']
    return redirect("/")