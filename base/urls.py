from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('accounts/profile/',views.profile,name="profile"),
    path('logout/',views.logout_view,name='logout'),
    path('',views.home,name='home'),
    path('registration/',views.registration,name='registration'),
    path('payment/',views.payment,name='payment'),
    path('paymentsuccess/',views.paymentsuccess,name='paymentsuccess'),
    path('alreadypaid/',views.alreadypaid,name='alreadypaid'),
    path('errornotification/', views.errornotification, name='errornotification'),
    path('registrationsuccess/',views.registrationsuccess,name='registrationsuccess'),
    path('paperpresentation/',views.paperpresentation,name='paperpresentation'),
    path('guesstronics/',views.guesstronics,name='guesstronics'),
    path('electroswaggers/',views.electroswaggers,name='electroswaggers'),
    path('electroquest/',views.electroquest,name='electroquest'),
    path('cs2/',views.cs2,name='cs2'),
    path('bidwars/',views.bidwars,name='bidwars'),
    path('funopedia/',views.funopedia,name='funopedia'),
    path('guesswork/',views.guesswork,name='guesswork'),
    path('debate/',views.debate,name='debate'),
    path('rhymeredux/',views.rhymeredux,name='rhymeredux'),
]