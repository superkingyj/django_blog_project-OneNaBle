from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.

# Category 모델
class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# 태그 모델
class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Post 모델
class BlogPost(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField('Tag',blank=True)
    like=GenericRelation('Like',related_query_name='post')


# Like 모델
class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(BlogPost,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')  # 하나의 사용자가 같은 포스트에 여러 번 좋아요를 누르지 못하도록 합니당ㅇ

# Comment 모델
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    like=GenericRelation('Like',related_query_name='comment')

    def __str__(self):
        return f"Comment by {self.user.username}"

# Views 모델
class Views(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)