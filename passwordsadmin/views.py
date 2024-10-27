from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CreatePasswordForm
from .models import Password
from django.contrib.auth.decorators import login_required


def home(request):
    userName = request.user.username
    return render(request, 'home.html', {
        'userName': userName
    })


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('passwords')

            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Passwords do not match each other'
        })


@login_required
def passwords(request):
    owned_list = Password.objects.filter(user=request.user)
    received_list = Password.objects.filter(shared=True, sharedWith=request.user)
    return render(request, 'passwords.html', {
        'on_passwords_page': True,
        'owned_list': owned_list,
        'received_list': received_list
    })



@login_required
def create_password(request):
    if request.method == 'GET':
        return render(request, 'create_password.html', {
            'form': CreatePasswordForm,
        })
    else:
        try:
            form = CreatePasswordForm(request.POST)
            if form.is_valid():
                new_password = form.save(commit=False) 
                new_password.user = request.user
                new_password.shared = form.cleaned_data.get('shared', False)
                new_password.save()

                if new_password.shared:
                    new_password.sharedWith.set(form.cleaned_data['sharedWith'])
                form.save_m2m()

                return redirect('passwords')
            else:
                print('form errors', form.errors)
                return render(request, 'create_password.html', {
                    'form': CreatePasswordForm,
                    'error': 'Invalid data'
                })
        except ValueError:
            print('Invalid data', request.POST)
            print('form errors', form.errors)
            return render(request, 'create_password.html', {
                'form': CreatePasswordForm,
                'error': 'Invalid data'
            })


@login_required
def password_edit(request, password_id):
    if request.method == 'GET':
        password = get_object_or_404(Password, pk=password_id, user=request.user)
        return render(request, 'password_edit.html', {
            'password': password,
            'form': CreatePasswordForm(instance=password)
        })
    else:
        password = get_object_or_404(Password, pk=password_id, user=request.user)
        form = CreatePasswordForm(request.POST, instance=password)
        if form.is_valid():
            form.save()
            return redirect('passwords')
        else:
            return render(request, 'password_edit.html', {
                'password': password,
                'form': form
            })
        
@login_required
def password_detail(request, password_id):
    password = get_object_or_404(Password, pk=password_id, user=request.user)
    return render(request, 'password_detail.html', {
        'password': password
    })

def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username and/or password incorrect'
            })

        else:
            login(request, user)
            return redirect('passwords')
