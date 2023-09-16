from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from .models import *
import re


# blog post form
from .form import BlogPostForm

# user login, logout, register form
from django.contrib.auth import authenticate, login
from .form import CustomLoginForm

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by('-views')
    serializer_class = BlogPostSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
        
    def create(self, request):
        content = request.data['content']
        pattern = re.compile('["\'](\/[^"\']*?)["\']')
        img = pattern.findall(content)[0]
        
        
        data = {
            "user": request.data['user'],
            "title": request.data['title'],
            "content": content,
            "summer_fields": content,
            "category": request.data['category'],
            "img": img,
            "tags": [], # TODO: 수정
            "status": request.data['status'],
        }
    
        serializer = BlogPostSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
 
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
                return redirect('board_client')
            
    return render(request, 'login.html', {'form': form})

# 메인 화면
def board_client(request):
    return render(request, 'board_client.html')

def board_admin(request):
    return render(request, 'board_admin.html')

def write(request, blog_post_id=None):
    form = BlogPostForm()
    return render(request, 'board_write.html', {'form': form})

def board(request, blog_post_id):  
    blog_post = BlogPost.objects.get(pk=blog_post_id)
    blog_post.views += 1
    blog_post.save()
    related_posts = BlogPost.objects.filter(category=blog_post.category)
    context = {
        'blog_post': blog_post, 
        'related_posts': related_posts, 
    }
    
    return render(request, 'board.html', context)