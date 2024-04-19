from django.urls import path
from . import views

urlpatterns = [
    path('', views.start),
    path('home.html', views.home),
    path('offer.html', views.signForCourse, name='signForCourse'),
    path('login.html', views.login, name='login'),
    path('loggingResultResult.html', views.loggingResult, name='loggingResult'),
    path('register.html', views.register, name='register'),
    path('registrationResult.html', views.registrationResult, name='registrationResult')
]
