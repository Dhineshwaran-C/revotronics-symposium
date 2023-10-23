from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('accounts/profile/',views.profile,name="profile"),
    path('logout/',views.logout_view,name='logout'),
    path('',views.home,name='home'),
    path('events/',views.events,name='event'),
    path('registration/',views.registration,name='registration'),
    path('payment/',views.payment,name='payment'),
    path('paymentsuccess/',views.paymentsuccess,name='paymentsuccess'),
    path('alreadypaid/',views.alreadypaid,name='alreadypaid'),
    path('errornotification/', views.errornotification, name='errornotification'),
]