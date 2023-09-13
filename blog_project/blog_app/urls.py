from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

post_list = views.BlogPostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

post_detail = views.BlogPostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})


router = DefaultRouter()
router.register(r"post", views.BlogPostViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/post", post_list),
    path("api/post/<int:pk>", post_detail),
    
    path("", views.board_client, name="board_client"),
    path("login", views.custom_login, name="login"),
    path("board-admin", views.board_admin, name="board_admin"),
    path("write", views.write, name="write"),
    path("board", views.board, name="board"),
]
