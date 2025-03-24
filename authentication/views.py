# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm, SignUpForm
from apps.home.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            comp_name = form.cleaned_data.get("comp_name")
            comp_logo = form.cleaned_data.get("comp_logo")
            user = authenticate(username=username, password=raw_password)
            user.first_name = comp_name
            user.save()
            company_profile_create = company_profile(company = user)
            company_bank_create = bank_details(company = user)
            company_profile_create.save()
            company_bank_create.save()
            profile_pic = profile_picture(name = user)
            profile_pic.profile_image = comp_logo
            profile_pic.save()

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    # messages.success(request, "Log out Successfuly...!")
    return redirect("/")