from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import ArrayField  


class User(models.Model):
    user_pwd = models.CharField(max_length=20)
    user_email = models.CharField(max_length=100)
    user_name = models.CharField(max_length=20)
    user_login_date = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    category_name = models.CharField(max_length=30)

class BlogPost(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField(blank=True,null=True)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    tags = ArrayField(models.CharField(max_length=300), blank=True, null=True)
    like_count = models.IntegerField()
    status = models.BooleanField(default=False)
    imag = models.TextField()


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_Post_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.TextField()
    chrmt_upload_date = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_Post_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like_upload_date = models.DateTimeField(auto_now_add=True)