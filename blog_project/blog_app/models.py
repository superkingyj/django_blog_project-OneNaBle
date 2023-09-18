from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField  
from django_summernote import fields as summer_fields

class User(models.Model):
    user_pwd = models.CharField(max_length=20)
    user_email = models.CharField(max_length=100)
    user_name = models.CharField(max_length=20)
    user_login_date = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    DAILY = 0
    COOKING = 1
    TRAVEL = 2
    MOVIE = 3
    IT = 4
    CATEGORY_CHOICES= [ (DAILY, "일상"), (COOKING, "요리"), (TRAVEL, "여행"), (MOVIE, "영화"), (IT, "IT")]
    category_name = models.IntegerField(choices=CATEGORY_CHOICES, default=DAILY)
    def __str__(self):
        return f"{self.category_name}"
    

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    summer_fields = summer_fields.SummernoteTextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    tags = ArrayField(models.CharField(max_length=300), blank=True, null=True)
    like_count = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    img = models.TextField(blank=True, null=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.TextField()
    chrmt_upload_date = models.DateTimeField(auto_now_add=True)
    like_cnt = models.IntegerField(default=0)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like_upload_date = models.DateTimeField(auto_now_add=True)