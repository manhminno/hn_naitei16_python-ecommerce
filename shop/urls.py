from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('detail-profile', views.detail_profile, name='detail-profile'),
    path('logout', views.user_logout, name='logout'),
    url('signup', views.signup, name='signup'),
]
