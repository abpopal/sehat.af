
from django.urls import path, include
from django.conf.urls import url

from mysite import views

urlpatterns = [

    path('search/', views.search_view, name='search'),
    url(r'^request/(?P<record_id>[-\w]+)/$', views.send_req_view, name='request'),
    path('requests/', views.req_view, name='requests'),
    path('profile/', views.profile_view, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    url(r'^requests/delete/(?P<req_id>[-\w]+)/$', views.delete_req_view, name='d_request'),
    url(r'^requests/accept/(?P<req_id>[-\w]+)/$', views.accept_req_view, name='accept_request'),
    url(r'^requests/reject/(?P<req_id>[-\w]+)/$', views.reject_req_view, name='reject_request'),
    path('notifications/', views.notification_view, name='notifications'),
    path('profile/become_donor', views.become_donor_view, name='become_donor'),
    path('add_record', views.add_record_view, name='add_record'),

]
