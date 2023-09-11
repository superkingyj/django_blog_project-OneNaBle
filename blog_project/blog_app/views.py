from django.shortcuts import render
from .models import *

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
    return render(request, 'write.html')

def board(request):    
    return render(request, 'board.html')
 