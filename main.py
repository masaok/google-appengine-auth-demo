
import webapp2
import os
import jinja2
import json
import datetime
import time
from google.appengine.api import users
from google.appengine.ext import ndb

from data import Course, Teacher, User, Post, Enrollment

from content_manager import populate_feed, logout_url, login_url

from pprint import pprint, pformat

jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

def get_auth():

  # Get the Google user
  user = users.get_current_user()
  nickname = None
  if user:
    nickname = user.nickname()
    auth_url = users.create_logout_url('/')
  else:
    auth_url = users.create_login_url('/login')
  return {
    "nickname": nickname,
    "auth_url": auth_url,
    "auth_text": "Sign out" if user else "Sign in"
  }

# the handler section
class MainPage(webapp2.RequestHandler):
  def get(self): #for a get request
    # self.response.headers['Content-Type'] = 'text/plain'
    # self.response.write('Hello, World!') #the response

    template= jinja_env.get_template("/templates/home.html")
    self.response.write(template.render(get_auth()))
    # self.response.write(template.render())

class LogInHandler(webapp2.RequestHandler):
  def get(self):
      google_login_template = jinja_env.get_template("/templates/google_login.html")
      new_user_template = jinja_env.get_template("/templates/new_user.html")

      user = users.get_current_user()

      if user:
          print("ACCOUNT EXISTS:")
          print(user.email())
          print(user.nickname())


          existing_user = User.query().filter(User.email == user.email()).get()
          nickname = user.nickname()
          if existing_user:
              self.redirect('/addcourses')

          if not existing_user:
              fields = {
                "nickname": nickname,
                "logout_url": logout_url,
              }
              self.response.write(new_user_template.render(fields))
          # else:
          #     self.redirect('/layout.html')
      else:
          self.response.write(google_login_template.render({ "login_url": login_url  }))

# the app configuration section
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/login', LogInHandler),
], debug=True)
