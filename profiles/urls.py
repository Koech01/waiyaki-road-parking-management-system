from . import views
from django.urls import path

app_name = 'profiles'

urlpatterns = [
    path('', views.profileView, name='profile'),
    path('edit/', views.editProfile, name='editProfile'),
]