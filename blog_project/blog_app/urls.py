from django.contrib.auth import views as auth_views
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

like_list = views.LikeViewSet.as_view({
    'post': 'create'
})

router = DefaultRouter()
router.register(r"post", views.BlogPostViewSet)
router.register(r"user", views.UserViewSet)
router.register(r"comment", views.CommentViewSet)
router.register(r"like", views.LikeViewSet)

app_name = 'blog_app'
urlpatterns = [
    path("api/", include(router.urls)),
    
    path("api/post", post_list, name="post_list"),
    path("api/post/<int:pk>", post_detail, name="post_detail"),
    path("api/like", like_list, name="like_list"),
    path('post/<int:post_id>/', views.board, name='post_title'),
    
    path("", views.board_client, name="board_client"),
    path("login/", views.custom_login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("write/", views.write, name="write"),
    path("write/<int:blog_post_id>", views.write, name="write_with_id"),
    path("board/<int:blog_post_id>", views.board, name="board"),

    # ai
    path('autocomplete/', views.autocomplete, name='autocomplete'),

    # haystack
    path('search', views.search_view, name='search_view'),
]
