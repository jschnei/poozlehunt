# models
from google.appengine.ext import db

class User(db.Model):
  name = db.StringProperty(required = True)
  password = db.StringProperty(required = True)
  email = db.StringProperty(required = True)
  is_admin = db.IntegerProperty(required=True, default=0)

  created = db.DateTimeProperty(auto_now_add = True)

class Puzzle(db.Model):
  title = db.StringProperty(required=True)
  short_code = db.StringProperty(required=True)
  answer = db.StringProperty(required=True)
  text = db.TextProperty(required=True)
  author = db.IntegerProperty(required=True)
  approved = db.BooleanProperty(required=True, default=False)

  is_puzzle = db.BooleanProperty(required=True, default=True)
  created = db.DateTimeProperty(auto_now_add = True)

class PuzzleHunt(db.Model):
  title = db.StringProperty(required=True)

  short_code = db.StringProperty(required=True)
  num_puzzles = db.IntegerProperty(required=True, default=0)

class PuzzleHuntPuzzleInfo(db.Model):
  # maps hunts to their individual puzzles
  hid = db.IntegerProperty(required=True)
  pid = db.IntegerProperty(required=True)

class UserPuzzleInfo(db.Model):
  uid = db.IntegerProperty(required=True)
  pid = db.IntegerProperty(required=True)

  author = db.BooleanProperty(required=True, default=False)
  locked = db.BooleanProperty(required=True, default=False)
  solved = db.BooleanProperty(required=True, default=False)
  tries = db.IntegerProperty(required=True, default=0)

class UserHuntInfo(db.Model):
  uid = db.IntegerProperty(required=True)
  hid = db.IntegerProperty(required=True)

  author = db.BooleanProperty(required=True, default=False)
  locked = db.BooleanProperty(required=True, default=False)
  solved = db.BooleanProperty(required=True, default=False)
  num_solved = db.IntegerProperty(required=True, default=0)

class PuzzleLockInfo(db.Model):
  # represents that you must solve puzzle <ppid> before puzzle <pid>

  pid = db.IntegerProperty(required=True)
  ppid = db.IntegerProperty(required=True)

class PuzzleFile(db.Model):
  uid = db.IntegerProperty(required=True)
  fname = db.StringProperty(required=True)
  pfile = db.BlobProperty()
  mime_type = db.StringProperty()
