from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import *
from .serializers import *

# ckeditor form
from .form import BlogForm

# user login, logout, register form
from django.contrib.auth import authenticate, login
from .form import UserForm


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def board_client(request):
    return render(request, 'board_client.html')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        user_name= request.POST.get('username')
        user_pwd= request.POST.get('password')
        user = authenticate(username=user_name, password=user_pwd)
        print(user_name, user_pwd, user)

        if user is not None:
            login(request,user=user)
            return redirect('board_admin')

        else:
            print('ID 혹은 비밀번호 오류입니다.')
            return redirect('login')

def board_admin(request):
    return render(request, 'board_admin.html')

def write(request):
    form = BlogForm()
    return render(request, 'board_write.html', {'form': form})

def board(request):    
    return render(request, 'board.html')
 