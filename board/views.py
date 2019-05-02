from django.shortcuts import render, redirect 
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import Profile, Trucker
import requests
import json
from .forms import ProfileForm, TruckerForm 
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/register/')
def board(request):
    truckers = Trucker.objects.all()
    return render(request, 'index.html')

def dashboard(request):
    current_user = request.user
    if request.method == 'POST':
        form = TruckerForm(request.POST, request.FILES)
        if form.is_valid():
            trucker = form.save(commit=False)
            trucker.user=current_user
            trucker.save()
        return redirect('board')

    else:
        form = TruckerForm()
    return render(request, 'dashboard.html', {"form": form})


@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user=current_user
            profile.bio=form.cleaned_data['bio']
            profile.photo = form.cleaned_data['profile_photo']
            profile.user=current_user
            
            profile.save()
        return redirect('board')

    else:
        form = ProfileForm()
    return render(request, 'profile.html', {"form": form})


@login_required(login_url='/accounts/login/')
def view_profile(request, id):

    profile=Profile.objects.get(user_id=id)
    return render(request, 'view_profile.html',{"profile":profile},)



def maps(request):
    ip_address = request.META.get('http://api.ipstack.com/105.178.36.183', '')
    response = requests.get('http://api.ipstack.com/105.178.36.183?access_key=bf3dc84257db3e7928449bb12f3d5588&format=1')
    geodata = response.json()
    return render(request, 'core/maps.html', {
        'ip': '105.178.36.183',
        'country': 'Rwanda',
        'latitude': -1.9536,
        'longitude': 30.0606,
        'api_key': 'AIzaSyAGB0lhvVsO4ywn5RGjdLjWBVW9JyaVRTI'  

        # 
    })