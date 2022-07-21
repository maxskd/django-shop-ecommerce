from django.urls import path

from .views import *

urlpatterns = [
    path('about/', about, name='about'),
    path('', welcome_page, name='welcome'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('profile/', user_profile, name='profile'),
    path('logout/', user_logout, name='logout'),
    path('contact_us/', contact_us, name='contact_us')
]
