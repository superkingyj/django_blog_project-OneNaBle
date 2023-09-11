from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.board_client, name="board_client"),
    path("login", views.login, name="login"),
    path("board-admin", views.board_admin, name="board_admin"),
    path("write", views.write, name="write"),
    path("board", views.board, name="board"),
]
