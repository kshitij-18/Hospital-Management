from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from . forms import RegistrationForm, VaccinationAdd
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, 'myapp/index.html')


def register_request(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(
                request, f'User with {username} created successfully')
            return redirect('homepage')
    else:
        form = RegistrationForm()
    stuff_for_frontend = {
        'form': form
    }
    return render(request, 'myapp/register.html', stuff_for_frontend)


def login_request(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome {user.username}")
            return redirect('homepage')
    else:
        form = AuthenticationForm()
    frontend = {
        'form': form
    }
    return render(request, 'myapp/login.html', frontend)


def logout_request(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You need to Login First')
        return redirect('login')
    logout(request)
    return render(request, 'myapp/logout.html')


def add_vaccines(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login First")
        return redirect('login')
    if request.method == 'POST':
        form = VaccinationAdd(data=request.POST)
        vaccine_name = request.POST.get('vaccination')
        request.user.vaccinations.create(vaccine_name=vaccine_name)
        return redirect('homepage')
    else:
        form = VaccinationAdd()
    front = {
        'form': form
    }
    return render(request, 'myapp/vaccination_add.html', front)


def vaccine_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login First")
        return redirect('login')
    else:
        front = {
            'user_vaccines': request.user.vaccinations.order_by("-taken_on")
        }
        return render(request, 'myapp/vaccine_list.html', front)
