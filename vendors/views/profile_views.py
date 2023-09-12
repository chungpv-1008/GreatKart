from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="/vendor/sign-in")
def profile(request):
    return render(request, 'home/profile.html')