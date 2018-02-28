# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
#import bcrypt for password security
import bcrypt
#import Trip? from travel_planner.models

class UserManager(models.Manager):

  def get_user(self, user_id):
    return self.get(id=user_id)

  #validate registration info
  def validate_registration(self, post_data):
    data = {
      'name' : post_data['name'],
      'username' : post_data['username'],
      'password' : post_data['password'],
      'confirm' : post_data['confirm_password']
    }
    error = []

    if not data['name']:
      error.append("Please enter a name.")
    elif len(data['name']) <= 3 or not data['name'].isalpha():
      error.append("Name must be letters and longer than 3 characters.")
    if not data['username']:
      error.append("Please enter a Username.")
    elif len(data['username']) <= 3:
      error.append("Username must be longer than 3 characters.")
    if not data['password'] or not len(data['password']) > 7:
      error.append("Password much be at least 8 characters.")
    if not data['password'] == data['confirm']:
      error.append("Passwords must match.")

    #check against duplicate usernames
    if User.objects.filter(username = data['username']):
      error.append("Username already in use.")
    
    print error

    #return any errors in validation
    if error:
      return error
    #bcrypt the password, then add user.  return id# for session
    else:
      data['password'] = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
      self.add_user(data)
      return User.objects.filter(username = data['username'])[0].id

  #create a new user
  def add_user(self, post_data):
    self.create(name = post_data['name'], username = post_data['username'], password = post_data['password'])

  #login user by checking post data against database entries
  def login_user(self, post_data):
    data = {
      'username' : post_data['username'],
      'password' : post_data['password']
    }
    error = []
    #check for username in User database
    if User.objects.filter(username = data['username']):
      #for valid username, check password against User database
      check = User.objects.filter(username = data['username'])[0].password
      if bcrypt.checkpw(data['password'].encode(), check.encode()):
        print 'username and password match'
        return User.objects.filter(username = data['username'])[0].id
      else:
        error.append("Invalid password/username combination.")
        print "username passed, password failed"
        return error
    else:
      error.append("Invalid password/username combination.")
      print "invalid username"
      return error
  
  def list_travellers(self, trip_id, user_id):
    return self.filter(trips__id=int(trip_id)).exclude(id=int(user_id))

# Create your models here.
class User(models.Model):
  name = models.CharField(max_length = 45)
  username = models.CharField(max_length = 45)
  password = models.CharField(max_length = 45)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  objects = UserManager()