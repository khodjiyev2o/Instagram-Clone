from django.forms import ValidationError
from django.shortcuts import render
from .forms  import RegistrationForm
from .decorators import unauthenticated_user
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def loginpage(request):
    return render(request,'users/login.html',{})


@unauthenticated_user
def register(request):
    form = RegistrationForm()
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
      

        if form.is_valid():
            user = form.save()
        else:
            messages.error(request,"Please enter correct credentials")

           
            return HttpResponseRedirect('/main')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {"forms": form})