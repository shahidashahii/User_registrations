from django.shortcuts import render
from django.http import HttpResponse
from app.forms import *
from django.core.mail import send_mail
# Create your views here.
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