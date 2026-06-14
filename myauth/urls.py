from django.urls import path
app_name = 'myauth'
from . import views

urlpatterns = [
    path('login', views.xxlogin, name='login'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='captcha'),
    path('logout', views.xxlogout, name='logout'),
]