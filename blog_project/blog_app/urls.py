from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"post", views.BlogPostViewSet)
router.register(r"user", views.UserViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    
    path("", views.board_client, name="board_client"),
    path("login", views.login, name="login"),
    path("board-admin", views.board_admin, name="board_admin"),
    path("write", views.write, name="write"),
    path("board", views.board, name="board"),
]
