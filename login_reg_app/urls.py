from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('books', views.books),
    path('register', views.register),	   
    path('login', views.login),	 
    path('logout', views.logout),
    path('uploadBook', views.upload_b),
    path('likeBook/<id>', views.Add_like),
    path('books/<id>', views.book_dis),
    path('unlikeBook/<id>', views.rem_like),
    path ('deleteBook/<id>', views.del_book),
    path('editBook/<id>', views.edit_book),
]