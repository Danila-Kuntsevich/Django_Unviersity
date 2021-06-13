from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserForm
from .models import MainCycle
from .serializres import UserSerializer, UserDetailSerializer
from rest_framework import generics


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

def index(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) > 0:
        mainCycle = MainCycle.objects.filter(user=request.user)[0]
        return render(request, 'index.html', {'user':user[0], 'mainCycle':mainCycle})
    else:
        return render(request, 'login.html')

def callClick(request):
    user = User.objects.filter(id=request.user.id)
    mainCycle = MainCycle.objects.filter(user=request.user)[0]
    mainCycle.Click()
    mainCycle.save()
    return HttpResponse(mainCycle.coinsCount)

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            mainCycle = MainCycle()
            mainCycle.user = user
            mainCycle.save()
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return redirect('index')


def user_logout(request):
    logout(request)
    return redirect('login')


def user_registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration.html', {'invalid':True, 'form': form})
    else:
        form = UserForm()
        return render(request, 'registration.html', {'invalid':False, 'form': form})
