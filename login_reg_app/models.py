from distutils import errors
from operator import mod
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        check_email = User.objects.filter(user_email=postData['email'])
        if len(check_email) > 0:
            errors['email_c'] = "Email is alreay registered"
            return errors
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Invalid email address!"
        if len(postData['fname']) < 2:
            errors["fname"] = "First name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData["password"] != postData['cpass']:
            errors["cpass"] = "Password and conformation Password does not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        check_user = User.objects.filter(user_email=postData['email'])
        if len(check_user) == 0:
            errors['email_e'] = "Login Failed: Your email or password is incorrect"
        elif check_user[0].user_email != postData['email']:
            errors['email'] = "Login Failed: Your email or password is incorrect"
        elif not bcrypt.checkpw(postData['password'].encode(), check_user[0].password.encode()):
            errors["password"] = "Login Failed: Your email or password is incorrect"
        return errors
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def uploading_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors["title"] = "Title is required"
        if len(postData['desc']) < 5:
            errors["desc"] = "Description should be at least 5 characters"
        return errors
        
class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="uploaded_books", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()