# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

from .models import User

from django.contrib import messages

# Create your views here.
#render login and registration page
def register(request):

  return render(request, 'login_registration/register.html')

#validate registration, add user
def process(request):
  if request.method == 'POST':
    error = User.objects.validate_registration(request.POST)
    if type(error) is list:
      #create messages if error detected
      for x in error:
        messages.add_message(request, messages.ERROR, x)
      return redirect('loginReg:register')
    else:
      print User.objects.last().name
      request.session['user_id'] = error
      return redirect('travels:triplist')

  return redirect('loginReg:register')

#validate login, set session for user
def login(request):
  if request.method == 'POST':
    error = User.objects.login_user(request.POST)
    if type(error) is list:
      #create messages if errors detected
      for x in error:
        messages.add_message(request, messages.ERROR, x)
      return redirect('loginReg:register')
    else:
      #set session for user_id
      request.session['user_id'] = error
      return redirect('travels:triplist')

  return redirect('loginReg:register')

#clear session on logout
def logout(request):
  del request.session['user_id']
  return redirect('loginReg:register')