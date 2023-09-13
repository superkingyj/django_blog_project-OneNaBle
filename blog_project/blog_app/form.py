from django import forms
from .models import BlogPost
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = BlogPost
        fields = ['content']
        
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']