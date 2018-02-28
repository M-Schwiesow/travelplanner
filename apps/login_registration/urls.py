from django.conf.urls import url
from . import views

urlpatterns=[
  url(r'^$', views.register, name="register"),
  url(r'^register$', views.register, name="register"),
  url(r'^process$', views.process, name="process"),
  url(r'^login$', views.login, name = "login"),
  url(r'^logout$', views.logout, name="logout")
]