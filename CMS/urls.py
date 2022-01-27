from django.urls import path
from django.urls.conf import re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('CMS/', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('profile/', views.profile, name='profile'),
    path('aboutme', views.aboutme, name='aboutme'),
    path('aboutme/', views.aboutme, name='aboutme'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('past-consult/', views.pastconsult, name='pastconsult'),
    path('lab-reports/', views.report, name='report'),
    path('past-booking/', views.pastbooking, name='pastbooking'),
    path('active-booking/', views.activebooking, name='activebooking'),
    path('doctors', views.doctors, name='doctors'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/booking', views.booking, name='booking'),
    path('doctors/booking/', views.booking, name='booking'),
    path('change/<int:uid>', views.change, name='change'),
    path('forgot/', views.forgot, name='forgot'),
    path('otp/<int:uid>', views.otp, name='otp'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    # path('session-exp/', views.sessionExpired, name='session-exp'),
]

# this regex will match any url pattern and then render the 404 page.
urlpatterns += [
    re_path(r'(?P<path>.*)', views.error, name="error")
]
