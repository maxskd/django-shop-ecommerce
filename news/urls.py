from django.urls import path

from .views import *

urlpatterns = [
    path('', news, name='news'),
    path('<slug:post_slug>/', show_post, name='post'),
]
