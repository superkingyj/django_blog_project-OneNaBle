from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import action
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
    @action(methods=['get'], detail=False)
    def filter(self, request, *args, **kwargs):
        category_id = request.query_params['category']        
        queryset = BlogPost.objects.filter(category=category_id)
        serializer = BlogPostSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    # 좋아요 작성/삭제
    def create(self, request):
        queryset = Like.objects.filter(
            user=request.data['user'], 
            blog_post=request.data['blog_post'], 
            comment=request.data['comment']
        )
        
        # 이미 좋아요를 눌렀다면
        if queryset.exists():
            queryset.delete()
            return Response(status=204)
        # 좋아요를 누르지 않았다면
        else:
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        

def custom_login(request):
    # 이미 로그인 되어 있다면
    if request.user.is_authenticated:
        return redirect('board_client')
    
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

@login_required(login_url='login')
def write(request, blog_post_id=None):
    if request.user.is_authenticated:
        form = BlogPostForm()
        return render(request, 'board_write.html', {'form': form})

@login_required(login_url='login')
def board(request, blog_post_id):  
    if request.user.is_authenticated:
        blog_post = BlogPost.objects.get(pk=blog_post_id)
        blog_post.views += 1
        blog_post.save()
        related_posts = BlogPost.objects.filter(category=blog_post.category)
        comments = Comment.objects.filter(blog_post=blog_post_id)
        
        context = {
            'blog_post': blog_post, 
            'related_posts': related_posts, 
            'comments': comments
        }

        return render(request, 'board.html', context)