from django.urls import path
from .views import *

urlpatterns = [
    path('fetch_videos/', fetch_videos, name='fetch_videos'),
    path('', home, name='home'),
]
