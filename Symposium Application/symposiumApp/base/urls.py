from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('accounts/profile/',views.profile,name="profile"),
    path('logout/',views.logout_view,name='logout'),
    path('home/',views.home,name='home'),
    path('events/',views.events,name='event'),
]