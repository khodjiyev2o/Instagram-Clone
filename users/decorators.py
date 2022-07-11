from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

def unauthenticated_user(view_funct):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')
        else:
            return view_funct(request, *args, **kwargs)

    return wrapper_func