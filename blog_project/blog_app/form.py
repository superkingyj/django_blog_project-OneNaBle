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
        

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'login-input'}),
        label='',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'login-input'}),
        label='',
    )


# class BlogPostForm(forms.ModelForm):
#     class Meta:
#         model = BlogPost
#         exclude = ['created_at']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['topic'].required = False
#         self.fields['publish'].required = False
#         self.fields['views'].required = False