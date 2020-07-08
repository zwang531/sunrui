from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('my_app:index')
        else:
            messages.error(request, "用户名或密码不正确")
            return render(request, 'login/index.html')
    return render(request, 'login/index.html')


def logout_request(request):
    logout(request)
    return redirect('login:index')
