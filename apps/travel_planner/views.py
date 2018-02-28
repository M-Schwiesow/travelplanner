# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from ..login_registration.models import User
from .models import Trip
# Create your views here.

#render trip list #triplist
def triplist(request):
  try:
    request.session['user_id']
  except KeyError:
    return redirect('loginReg:register')
  else:
    
    context = {
      'user' : User.objects.get_user(request.session['user_id']),
      'trip_list' : Trip.objects.user_trips(request.session['user_id']),
      'user_id' : int(request.session['user_id']),
      'other_trips' : Trip.objects.other_trips(request.session['user_id'])
    }

    return render(request, 'travel_planner/displaytrips.html', context)



  # context = {
  #   'trip' : Trip.objects.get_destination(trip_id),
  #   #check this query, then move it to the model!!!
  #   'travellers' : User.objects.filter(trips__id=trip_id)
  # }
#render destination display #destination
def destination(request, trip_id):
  try:
    request.session['user_id']
  except KeyError:
    return redirect('loginReg:register')
  else:
    context = {
      'trip' : Trip.objects.get_destination(trip_id),
      #check this query, then move it to the model!!!
      'travellers' : User.objects.list_travellers(trip_id, request.session['user_id'])
    }

    return render(request, 'travel_planner/destinationdetails.html', context)

#render new trip form #addtrip
def addtrip(request):
  try:
    request.session['user_id']
  except KeyError:
    return redirect('loginReg:register')
  else:
    return render(request, 'travel_planner/addtrip.html')

#create a new trip #create
def createtrip(request):
  if request.method == 'POST':
    data = {
      'destination' : request.POST['destination'],
      'description' : request.POST['description'],
      'start' : request.POST['start'],
      'end' : request.POST['end'],
      'planner' : int(request.session['user_id'])
    }
    error = Trip.objects.validate_trip(data)

    if type(error) is list:
      for x in error:
        messages.add_message(request, messages.ERROR, x)
      return redirect('travels:addtrip')
    else:
      return redirect('travels:triplist')
  return redirect('travels:triplist')

#add a user to a trip/trip to a user #join
def jointrip(request, trip_id):
  data={
    'trip_id' : int(trip_id),
    'user_id' : int(request.session['user_id'])
  }
  Trip.objects.join_trip(data)


  return redirect('travels:triplist')