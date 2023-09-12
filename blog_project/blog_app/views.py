from django.shortcuts import render
from .models import *
from .form import BlogForm

# Create your views here.
def board_client(request):
    queryset = BlogPost.objects.all()
    return render(request, 'board_client.html')

def login(request):
    return render(request, 'login.html')

def board_admin(request):
    queryset = BlogPost.objects.all()
    return render(request, 'board_admin.html')

def write(request):
    form = BlogForm()
    return render(request, 'board_write.html', {'form': form})

def board(request):    
    return render(request, 'board.html')
 