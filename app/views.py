from django.shortcuts import render
from django.http import HttpResponse
from app.forms import *
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
# Create your views here.

from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def home(request):

    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    
    return render(request,'home.html')




def registration(request):
    UFO=UserForm()
    PFO=ProfileForm()
    d={'UFO':UFO,'PFO':PFO}

    if request.method=="POST" and request.FILES:
        UFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)

        if UFD.is_valid() and PFD.is_valid():
            NSUFO=UFD.save(commit=False)
            password=UFD.cleaned_data['password']
            NSUFO.set_password(password)
            NSUFO.save()
            NSPFO=PFD.save(commit=False)
            NSPFO.username=NSUFO
            NSPFO.save()
            send_mail('Registration',
                      "Succefully Registration is Done",
                      'shahidayashu1999@gmail.com',
                      [NSUFO.email],
                      fail_silently=False

                      )


            
            return HttpResponse('Regsitration is Susssessfulll')
        else:
            return HttpResponse('Not valid')

    
    return render(request,'registration.html',d)

def user_login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password')
    return render(request,'user_login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))       

    return render(request,'user_login.html')

@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)

    d={'UO':UO,'PO':PO}


    return render(request,'display_profile.html',d)





