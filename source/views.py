from django.contrib.auth import authenticate, login
from .forms import SignUpForm, EmailAuthenticationForm
from django.shortcuts import redirect, render, redirect

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:home')  
    else:
        form = EmailAuthenticationForm()
    return render(request, 'registration/login.html', { 'form': form })
    

def signUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home:home')  # Redirect to user's profile page after successful signup.
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', { 'form': form })
