from django.conf.urls import url
from . import views

urlpatterns=[
  url(r'^$', views.triplist, name="triplist"),
  url(r'^(?P<trip_id>\d+)/destination$', views.destination, name="destination"),
  url(r'^addtrip$', views.addtrip, name="addtrip"),
  url(r'^createtrip$', views.createtrip, name = "create"),
  url(r'^(?P<trip_id>\d+)/jointrip$', views.jointrip, name="join")
]