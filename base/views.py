from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import User,UserEvents,TeamEvents,Userpayment
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.conf import settings


import qrcode
import yagmail

from instamojo_wrapper import Instamojo

from django.conf import settings

api = Instamojo(
    api_key=settings.API_KEY,
    auth_token = settings.AUTH_TOKEN,
    endpoint='https://test.instamojo.com/api/1.1/'
    )


#  Login
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'login.html')



#profile
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
                regno = request.POST.get('regno'),
                college = request.POST.get('college')
            )
            return redirect(reverse('payment'))

    return render(request,'profile.html')


#logout
def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    userdata = ''
    if request.user.is_authenticated:
        try:
            userdata = User.objects.get(email = request.user.email)
        except User.DoesNotExist:
            return redirect('logout')
    return render(request,'home.html',{'userdata':userdata})

#events
@login_required(login_url='login')
@csrf_protect


def errornotification(request,data,data2):
    return render(request,'errornotification.html',{'data':data,'data2':data2})

#registration
@login_required(login_url='login')
def registration(request):
    cemail = User.objects.values_list('email',flat=True)
    pemail = Userpayment.objects.values_list('email',flat=True)
    
    try:
        tempevent = 'Paper Presentation'
        data = UserEvents.objects.get(email = request.user.email)
        if tempevent in data.eventstatus:
            temp_data = 'You are already in this event'
            redirect_page = 'home'
            return errornotification(request,temp_data,redirect_page)
    except UserEvents.DoesNotExist:
        pass
    
    if request.user.email in pemail:
        cpemail = Userpayment.objects.get(email = request.user.email)
        if cpemail.is_paid:
            if request.user.email not in cemail:
                return redirect('profile')
            teams = TeamEvents.objects.all()

            if request.method == 'POST':
                temp = User.objects.get(email = request.user.email)
                action = request.POST.get('action')


                if action == 'action2':
                    teamnamecheck = request.POST.get('teamname')
                    teampasswordcheck = request.POST.get('pinpassword')
                    teamcheck = TeamEvents.objects.values_list('teamname',flat=True)
                    
                    if teamnamecheck == '' or teampasswordcheck == '':
                        temp_data = 'Teamname or Password is not given'
                        redirect_page = 'registration'
                        return errornotification(request,temp_data,redirect_page)
                    
                    if teamnamecheck in teamcheck:
                        temp_data = 'This Team name already exist'
                        redirect_page = 'registration'
                        return errornotification(request,temp_data,redirect_page)
                    else:
                        TeamEvents.objects.create(
                            eventname = request.POST.get('regteamevent'),
                            teamname = request.POST.get('teamname'),
                            teammates = [request.user.email],
                            password = request.POST.get('pinpassword')
                        )
                        joinevent = request.POST.get('regteamevent')
                        cemail = UserEvents.objects.values_list('email',flat=True)
                        if request.user.email in cemail:
                            userevent = UserEvents.objects.get(email = request.user.email)
                            userevent.eventstatus.append(joinevent)
                            userevent.save()
                        else:
                            userevent = UserEvents.objects.create(
                                email = request.user.email,
                                user = temp,
                                eventstatus = joinevent.split(',')
                            )
                        return redirect('registrationsuccess')
                
                elif action == 'action3':
                    joinevent = request.POST.get('regteamevent')
                    team = request.POST.get('teamnames')
                    teampasswordcheck = request.POST.get('pinpassword2')

                    try:
                        data = TeamEvents.objects.get(eventname=joinevent,teamname = team)
                    except TeamEvents.DoesNotExist:
                        temp_data = 'There is no team like that'
                        redirect_page = 'registration'
                        return errornotification(request,temp_data,redirect_page)
                    
                    if teampasswordcheck == '':
                        temp_data = 'Password is not given'
                        redirect_page = 'registration'
                        return errornotification(request,temp_data,redirect_page)

                    
                    length = 3

                    if len(data.teammates) < length:
        
                        pinpassword = int(request.POST.get('pinpassword2'))
                        password = data.password
                        if password == pinpassword:
                            data.teammates.append(request.user.email)
                            data.save()
                            cemail = UserEvents.objects.values_list('email',flat=True)
                            if request.user.email in cemail:
                                userevent = UserEvents.objects.get(email = request.user.email)
                                userevent.eventstatus.append(joinevent)
                                userevent.save()
                            else:
                                userevent = UserEvents.objects.create(
                                    email = request.user.email,
                                    user = temp,
                                    eventstatus = joinevent.split(',')
                                )
                            return redirect('registrationsuccess')
                        else:
                            temp_data = 'Your password is wrong Try again'
                            redirect_page = 'registration'
                            return errornotification(request,temp_data,redirect_page)
                    
                    else:
                        temp_data = 'The Team is already Full'
                        redirect_page = 'registration'
                        return errornotification(request,temp_data,redirect_page)
                    
        else:
            return redirect('payment')


    else:
        return redirect('payment')

    return render(request,'registration.html',{'teams':teams})


#payment
@login_required(login_url='login')
def payment(request):
    cemail = User.objects.values_list('email',flat=True)
    if request.user.email not in cemail:
        return redirect('profile')
    try:
        userdetails = User.objects.get(email = request.user.email)
        paymentdetails , _ = Userpayment.objects.get_or_create(
            user = userdetails,
            email = request.user.email,
        )
        if paymentdetails.is_paid:
            return redirect('alreadypaid')
        else:
            response = api.payment_request_create(
                amount = 10,
                purpose = 'Payment Process',
                buyer_name = 'Sam',
                email = 'abc@gmail.com',
                redirect_url = 'http://127.0.0.1:8000/paymentsuccess/'
            )
            paymentdetails.order_id = response['payment_request']['id']
            paymentdetails.instamojo_response = response
            paymentdetails.save()

        return render(request,"payment.html",{'payment_url':response['payment_request']['longurl']})

    except Exception as e:
        print(e)





#paymentsuccess
@login_required(login_url='login')
def paymentsuccess(request):

    payment_request_id = request.GET.get('payment_request_id')
    try:
        paymentdetails = Userpayment.objects.get(order_id = payment_request_id)
    except Userpayment.DoesNotExist:
        temp_data = 'You are not allowed here'
        redirect_page = 'home'
        return errornotification(request,temp_data,redirect_page)
    if paymentdetails.is_paid == False:
        paymentdetails.payment_id = request.GET.get('payment_id')
        paymentdetails.is_paid = True
        paymentdetails.save()

        user = User.objects.get(email = request.user.email)

        id = user.unique_id

        qrfeatures = qrcode.QRCode(version=1,box_size=40,border=3)

        qr = qrcode.make(id)
        qr.save('qrimages/'+user.email+'.png')




        content = """
        <html>
        <body>
        <h1 style="color:purple;"><b>REVOTRONICS</b></h1>
        <h2 style="font-family:sans-serif;color:blue">Thank you for registering for Revotronics.</h2><br>
        <h3 style="font-family:sans-serif;">Please find the QR code attached to this email for check-in on the day of symposium. Stay tuned for further updates.</h3>
        <h3 style="font-family:sans-serif;">Get, Set, REV!</h3>
        <h3 style="font-family:sans-serif;">Best Regards,</h3>
        <h3 style="font-family:sans-serif;color:purple">Team Revotronics.</h3>
        </body>
        </html>
        """

        yag = yagmail.SMTP('revotronics23@gmail.com','xxux jqja ouct swkk')
        yag.send(user.email,'Revotronics Payment Successful',content,'qrimages/'+user.email+'.png')
        yag.close()

    else:
        return redirect('alreadypaid')

    return render(request,'paymentsuccess.html')
    

#alreadypaid
@login_required(login_url='login')
def alreadypaid(request):
    try:
        userpaymentdata = Userpayment.objects.get(email = request.user.email)
        if userpaymentdata.is_paid:
            return render(request,'alreadypaid.html')
        else:
            temp_data = 'You are not allowed here'
            redirect_page = 'home'
            return errornotification(request,temp_data,redirect_page)
    except Userpayment.DoesNotExist:
        temp_data = 'You are not allowed here'
        redirect_page = 'home'
        return errornotification(request,temp_data,redirect_page)
    


@login_required(login_url='login')
def registrationsuccess(request):
    try:
        registeremail = UserEvents.objects.get(email = request.user.email)
    except UserEvents.DoesNotExist:
        temp_data = 'You are not allowed here'
        redirect_page = 'home'
        return errornotification(request,temp_data,redirect_page)

    return render(request,'registrationsuccess.html')


def paperpresentation(request):
    return render(request,'paperpresentation.html')


def guesstronics(request):
    return render(request,'guesstronics.html')


def electroswaggers(request):
    return render(request,'electroswaggers.html')


def electroquest(request):
    return render(request,'electroquest.html')


def cs2(request):
    return render(request,'cs2.html')


def bidwars(request):
    return render(request,'bidwars.html')


def funopedia(request):
    return render(request,'funopedia.html')


def guesswork(request):
    return render(request,'guesswork.html')


def debate(request):
    return render(request,'debate.html')


def rhymeredux(request):
    return render(request,'rhymeredux.html')



