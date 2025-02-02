from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views import View

from .forms import UserLoginForm, UserSignUpForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

# Create your views here.


def userLogout(request):
    logout(request)
    return redirect('home')


class UserDjangoLogin(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserDjangoSignUp(CreateView):
    form_class = UserSignUpForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('home')


class UserProfile(View):
    def get(self, request, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        form = UserSignUpForm(request.POST or None, instance=user)
        form.id = user.id

        context = {
            'form': form,
        }

        return render(request, 'user/profile.html', context)


class UserSave(View):

    def post(self, request):
        user = User.objects.get(pk=request.POST.get('id'))
        form = UserSignUpForm(request.POST, instance=user)

        if form.is_valid():
            user = form.save(commit=True)

        return redirect('home')

