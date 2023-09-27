from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import User
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def login(request):
    return render(request,'login.html')

@login_required(login_url='login')
@csrf_protect
def profile(request):
    cemail = User.objects.values_list('email',flat=True)
    if request.user.email in cemail:
        return redirect('home')
    else:
        if request.method =='POST':
            User.objects.create(
                name = request.POST.get('username'),
                email = request.user.email,
                phoneno = request.POST.get('phone'),
            )
            return redirect('home')

    return render(request,'profile.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    user = User.objects.get(email = request.user.email)
    username = user.name
    return render(request,'home.html',{'username':username})