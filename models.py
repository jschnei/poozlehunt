# models
from google.appengine.ext import db

class User(db.Model):
  name = db.StringProperty(required = True)
  password = db.StringProperty(required = True)
  email = db.StringProperty(required = True)

  created = db.DateTimeProperty(auto_now_add = True)

class Puzzle(db.Model):
  title = db.StringProperty(required=True)
  short_code = db.StringProperty(required=True)
  answer = db.StringProperty(required=True)
  text = db.TextProperty(required=True)

  created = db.DateTimeProperty(auto_now_add = True)

class UserPuzzleInfo(db.Model):
  uid = db.IntegerProperty(required=True)
  pid = db.IntegerProperty(required=True)

  solved = db.BooleanProperty(required=True, default=False)
  tries = db.IntegerProperty(required=True, default=0)