from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^main$', views.main),
    url(r'^edit$', views.edit),
    url(r'^like/(?P<qID>\d+)$', views.like),
    url(r'^delete/(?P<qID>\d+)$', views.delete),
    url(r'^users/(?P<uID>\d+)$', views.showuser),
]
