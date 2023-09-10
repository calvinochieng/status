
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index , name='index'),
    path('home/', status , name='status'),
    path('about/', about , name='about'), 
    path('howto/', howto , name='howto'), 
    path('help/', help , name='help'), 
    path('register/', signup , name='register'),
    path('verify-account/', verifyaccount , name='verifyaccount'), 
    path('edit/', edit , name='editprofile'), 
    path('update/', updateprofile , name='updateprofile'), 
    path('login/', auth_views.LoginView.as_view(template_name ='status/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name ='status/logout.html', ), name='logout'),
    path('job/id-<uuid:uuid>/', job , name='job'),  
    path('job/id-<uuid:uuid>/download/', download , name='download'),  
    path('withdraw/', withdraw , name='withdraw'),  
    path('dashboard/', dashboard , name='dashboard'),  


]