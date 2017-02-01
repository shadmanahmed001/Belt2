from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$',views.register),
    url(r'^friends$',views.friends),
    url(r'^login$',views.login),
    url(r'^logout$', views.logout),
    url(r'^user/(?P<id>\d+)$', views.showuser),
    url(r'^addusertofriend/(?P<id>\d+)$', views.addusertofriend),
    url(r'^deletefriend/(?P<id>\d+)$', views.deletefriend)


]
