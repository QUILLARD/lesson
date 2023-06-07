from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from authapp.forms import UserLoginForm
from django.urls import reverse


def login(request):
    title = 'вход'
    login_form = UserLoginForm(data=request.POST)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))

    context = {
        'title': title,
        'login_form': login_form,
    }

    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    from django.urls import reverse
    return HttpResponseRedirect(reverse('index'))
