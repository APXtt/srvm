from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'service/index.html')


def login(request):
    return render(request, 'service/login.html')


def home(request):
    return render(request, 'service/homepage.html')


def mypage(request):
    return render(request, 'service/mypage.html')
