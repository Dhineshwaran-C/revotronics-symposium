from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import User,Events,UserEvents,TeamEvents
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse

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
                year = request.POST.get('year'),
                department = request.POST.get('department'),
                section = request.POST.get('section'),
                regno = request.POST.get('regno')
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


@login_required(login_url='login')
@csrf_protect
def events(request):
    if request.method == 'POST':
        Events.objects.create(
            eventname = request.POST.get('event'),
            limit = request.POST.get('limit'),
        )
        return redirect('event')
    return render(request,'events.html')



@login_required(login_url='login')
def registration(request):
    team_event = Events.objects.filter(limit__gt=1)
    nonteam_event = Events.objects.filter(limit=1)
    teams = TeamEvents.objects.all()


    if request.method == 'POST':
        temp = User.objects.get(email = request.user.email)
        action = request.POST.get('action','')
        if action == 'action1':
            cemail = UserEvents.objects.values_list('email',flat=True)
            if request.user.email in cemail:
                userevent = UserEvents.objects.get(email = request.user.email)
                userevent.eventstatus.extend(request.POST.get('eventstatus1').split(','))
                userevent.save()
            else:
                userevent = UserEvents.objects.create(
                    email = request.user.email,
                    user = temp,
                    eventstatus = request.POST.get('eventstatus1').split(',')
                )
            return redirect('home')
        
        if action == 'action2':
            try:
                tempevent = request.POST.get('regteamevent')
                data = TeamEvents.objects.get(eventname = tempevent)
                if request.user.email in data.teammates:
                    return HttpResponse("You are already in this event",content_type='text/plain')
            except TeamEvents.DoesNotExist:
                TeamEvents.objects.create(
                    eventname = request.POST.get('regteamevent'),
                    teamname = request.POST.get('teamname'),
                    teammates = [request.user.email],
                    password = request.POST.get('pinpassword')
                )
                userevent = UserEvents.objects.get(email = request.user.email)
                userevent.eventstatus.append(request.POST.get('regteamevent'))
                userevent.save()
            return redirect('registration')
        
        if action == 'action3':
            try:
                tempevent = request.POST.get('regteamevent')
                data = TeamEvents.objects.get(eventname = tempevent)
                if request.user.email in data.teammates:
                    return HttpResponse("You are already in this event",content_type='text/plain')
            except TeamEvents.DoesNotExist:
                joinevent = request.POST.get('regteamevent')
                team = request.POST.get('teamnames')
                pinpassword = request.POST.get('pinpassword2')
                data = TeamEvents.objects.get(eventname=joinevent,teamname = team)
                if data.password == pinpassword:
                    data.teammates.append(request.user.email)
                    return redirect('registration')
                else:
                    return HttpResponse('Your password is wrong Try again',content_type='text/plain')
                




    return render(request,'registration.html',{'nonteam_event':nonteam_event,'team_event':team_event,'teams':teams})