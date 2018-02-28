# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_registration.models import User
from datetime import date, datetime
# Create your models here.

class TripManager(models.Manager):
  #validate trip creation
  def validate_trip(self, post_data):
    data={
      'destination' : post_data['destination'],
      'description' : post_data['description'],
      'start' : post_data['start'],
      'end' : post_data['end'],
      'planner' : post_data['planner']
    }
    error = []
    #No Blank Fields.
    #Verify dates as future
    #Verify start before end
    if not data['destination']:
      error.append("You must enter a destination.")
    if not data['description']:
      error.append("Your trip must include a description.")
    if not data['start']:
      error.append("Your trip must have a start date.")
    elif data['start'] <= date.today().strftime("%Y-%m-%d"):
      error.append("Your start date must be after today.")
    if not data['end']:
      error.append("You can't stay there forever, you know.  Your trip must have an end date.")
    elif data['end'] < data['start']:
      error.append("Your trip cannot end before it begins!")

    if error:
      return error
    else:
      self.add_trip(data)
      return post_data['planner']

  def add_trip(self, data):
    self.create(destination = data['destination'], description = data['description'], start = data['start'], end = data['end'], planned_by = User.objects.get(id=data['planner']))
    User.objects.get(id=data['planner']).trips.add(Trip.objects.last())

  
  def join_trip(self, data):
    User.objects.get(id=data['user_id']).trips.add(self.get(id=data['trip_id']))

  def user_trips(self, data):
    return self.filter(traveler__id=int(data))

  def other_trips(self, data):
    return self.exclude(traveler__id=int(data))

  def get_destination(self, data):
    return self.get(id=int(data))



class Trip(models.Model):
  destination = models.CharField(max_length = 50)
  description = models.CharField(max_length = 255)
  start = models.DateField()
  end = models.DateField()
  planned_by = models.ForeignKey(User, related_name = "plans")
  traveler = models.ManyToManyField(User, related_name="trips")
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  
  objects = TripManager()