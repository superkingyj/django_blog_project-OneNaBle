from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import *
from .serializers import *

# ckeditor form
from .form import BlogForm

# user login, logout, register form
from django.contrib.auth import authenticate, login
from .form import CustomLoginForm


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
 
def board_client(request):
    return render(request, 'board_client.html')

def custom_login(request):
    # 이미 로그인 되어 있다면
    if request.user.is_authenticated:
        return redirect('board_admin')
    
    form = CustomLoginForm(data=request.POST or None)
    
    # 아이디 비밀번호를 입력했고
    if request.method == "POST":
        # 해당하는 유저가 있다면
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('board_admin')
            
    return render(request, 'login.html', {'form': form})
    

def board_admin(request):
    return render(request, 'board_admin.html')

def write(request):
    form = BlogForm()
    return render(request, 'board_write.html', {'form': form})

def board(request):    
    return render(request, 'board.html')
 