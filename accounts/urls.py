from django.urls import path, include
from django.conf.urls import url
from accounts import views

urlpatterns = [


    #path('registration/login', views.log_in_view, name='login'),
    path('signup/', views.registration_view, name='register'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    url(r'^password/$', views.change_password, name='change_password'),



]