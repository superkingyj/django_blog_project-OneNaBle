from rest_framework import serializers
from .models import BlogPost, Comment, Like, User
from django_summernote import fields as summer_fields

class BlogPostSerializer(serializers.ModelSerializer):
    summer_fields = summer_fields.SummernoteTextField()
    
    class Meta:
        model = BlogPost
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['summer_fields'].requried = False

    def create(self, validated_data):
        return BlogPost.objects.create(**validated_data)
            

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
    def create(self, validated_data):
        return Like.objects.create(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'