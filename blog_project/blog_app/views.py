from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from .models import *
import re
import json

# blog post form
from .form import BlogPostForm

# user login, logout, register form
from django.contrib.auth import authenticate, login
from .form import CustomLoginForm

# AI
from django.http import JsonResponse
import openai

# haystack
from haystack.query import SearchQuerySet
from django.http import JsonResponse


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all().order_by("-views")
    serializer_class = BlogPostSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def list(self, request):
        queryset = BlogPost.objects.all().filter(status="True").order_by("-views")
        serializer = BlogPostSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def create(self, request):
        content = request.data["content"]
        pattern = re.compile("[\"'](\/[^\"']*?)[\"']")
        img = pattern.findall(content)[0]

        data = {
            "user": request.data["user"],
            "title": request.data["title"],
            "content": content,
            "summer_fields": content,
            "category": request.data["category"],
            "img": img,
            "tags": [],  # TODO: 수정
            "status": request.data["status"],
        }

        serializer = BlogPostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    @action(methods=["get"], detail=False)
    def filter(self, request, *args, **kwargs):
        category_id = request.query_params["category"]
        queryset = BlogPost.objects.filter(category=category_id)
        serializer = BlogPostSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["get"], detail=False)
    def temp_post(self, request):
        queryset = BlogPost.objects.filter(status="False").first()
        serializer = BlogPostSerializer(queryset)
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
        like_queryset = Like.objects.filter(
            user=request.data["user"],
            blog_post=request.data["blog_post"],
            comment=request.data["comment"],
        )

        if like_queryset.exists():
            like_queryset.delete()
            comment_queryset = Comment.objects.get(id=request.data["comment"])
            comment_queryset.like_cnt -= 1
            comment_queryset.save()
            data = {"like_cnt": comment_queryset.like_cnt}
            return Response(data=json.dumps(data), status=204)
        else:
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                comment_queryset = Comment.objects.get(id=request.data["comment"])
                comment_queryset.like_cnt += 1
                comment_queryset.save()
                data = {"like_cnt": comment_queryset.like_cnt}
                return Response(data=json.dumps(data), status=201)
            return Response(serializer.errors, status=400)


def custom_login(request):
    # 이미 로그인 되어 있다면
    if request.user.is_authenticated:
        return redirect("board_client")

    form = CustomLoginForm(data=request.POST or None)

    # 아이디 비밀번호를 입력했고
    if request.method == "POST":
        # 해당하는 유저가 있다면
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("blog_app:board_client")

    return render(request, "login.html", {"form": form})


# 메인 화면
def board_client(request):
    return render(request, "board_client.html")


@login_required(login_url="blog_app:login")
def write(request, blog_post_id=None):
    if request.user.is_authenticated:
        form = BlogPostForm()
        return render(request, "board_write.html", {"form": form})


@login_required(login_url="blog_app:login")
def board(request, blog_post_id):
    if request.user.is_authenticated:
        blog_post = BlogPost.objects.get(pk=blog_post_id)
        blog_post.views += 1
        blog_post.save()

        related_posts = BlogPost.objects.filter(
            category=blog_post.category, status="True"
        ).order_by("-id")
        comments = Comment.objects.filter(blog_post=blog_post_id)
        previous_post = (
            BlogPost.objects.filter(id__lt=blog_post_id, status="True").order_by("-id").first()
        )
        next_post = (
            BlogPost.objects.filter(id__gt=blog_post_id, status="True").order_by("id").first()
        )

        context = {
            "blog_post": blog_post,
            "related_posts": related_posts,
            "comments": comments,
            "previous_post": previous_post,
            "next_post": next_post,
        }

        return render(request, "board.html", context)


# haystack
def search_view(request):
    query = request.GET.get("q")
    results = []

    if query:
        results = SearchQuerySet().filter(text=query)

    context = []
    for result in results:
        context.append(
            {
                "id": result.object.id,
                "title": result.title,
                "content": result.content,
                "img": result.object.img,
                "upload_date": result.object.upload_date,
            }
        )

    return JsonResponse(context, safe=False)


# Chat gpt API 사용
openai.api_key = "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"


# 글 자동완성 기능
def autocomplete(request):
    if request.method == "POST":
        # 제목 필드값 가져옴
        prompt = request.POST.get("title")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            # 반환된 응답에서 텍스트 추출해 변수에 저장
            message = response["choices"][0]["message"]["content"]
            print(message)
        except Exception as e:
            message = str(e)
        return JsonResponse({"message": message})
    return render(request, "autocomplete.html")


def logout(request):
    auth_logout(request)
    return redirect("blog_app:board_client")
