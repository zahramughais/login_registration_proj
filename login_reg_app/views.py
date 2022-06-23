from distutils.command.upload import upload
from hashlib import new
from multiprocessing import context
from webbrowser import get
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "index.html")

def books(request):
    if not "user_id" in request.session:
        return redirect('/')
    else :
        context = {
            'user': User.objects.get(id = request.session['user_id']),
            'books': Book.objects.all()
        }
    return render(request, "books.html", context)

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
            return redirect('/books')

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
            return redirect('/books')

def logout(request):
    del request.session['user_id']
    return redirect("/")

def upload_b(request):
    if request.method == "POST":
        errors = Book.objects.uploading_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/books")
        else:
            title = request.POST['title']
            desc = request.POST['desc']
            user = User.objects.get(id = request.session['user_id'])
            newBook = Book.objects.create(title = title, desc = desc, uploaded_by= user)
            newBook.users_who_like.add(user)
            newBook.save()
            return redirect('/books')

def Add_like(request, id):
    user = User.objects.get(id = request.session['user_id'])
    book = Book.objects.get(id = id)
    book.users_who_like.add(user)
    return redirect ('/books')

def book_dis(request, id):
    book = Book.objects.get(id = id)
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'book': book,
        'user': user
    }
    return render(request, "show.html", context)

def rem_like(request, id):
    user = User.objects.get(id = request.session['user_id'])
    book = Book.objects.get(id = id)
    book.users_who_like.remove(user)
    return redirect ('/books')

def del_book(request, id):
    book = Book.objects.get(id = id)
    upload_user = book.uploaded_by.id
    logged_user = User.objects.get(id = request.session['user_id']).id
    if upload_user == logged_user:
        book.delete()
    return redirect ('/books')

def edit_book(request,id):
    if request.method == "POST":
        errors = Book.objects.uploading_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("../books/"+id)
        else:
            book = Book.objects.get(id = id)
            upload_user = book.uploaded_by.id
            logged_user = User.objects.get(id = request.session['user_id']).id
            book.title = request.POST['title']
            book.desc = request.POST['desc']
            book.save()
            return redirect ('../books/'+id)