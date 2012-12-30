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

class PoozleQuest(db.Model):
  uid = db.IntegerProperty(required=True)
  mmap = db.StringProperty(required=True)
  xpos = db.IntegerProperty(required=True)
  ypos = db.IntegerProperty(required=True)

  in_battle = db.BooleanProperty(required=True, default=False)
  battle_id = db.IntegerProperty()

  in_transition = db.BooleanProperty(required=True, default=False)
  transition_text = db.StringProperty()

class PoozleQuestUnit(db.Model):
  # represents a generic unit
  name = db.StringProperty(required=True)
  atk = db.IntegerProperty(required=True)
  pdef = db.IntegerProperty(required=True)
  mag = db.IntegerProperty(required=True)
  mdef = db.IntegerProperty(required=True)
  spd = db.FloatProperty(required=True)
  mspd = db.FloatProperty(required=True)

  hp = db.IntegerProperty(required=True)
  mp = db.IntegerProperty(required=True)
  maxhp = db.IntegerProperty(required=True)
  maxmp = db.IntegerProperty(required=True)

  is_player = db.BooleanProperty(required=True, default=False)
  level = db.IntegerProperty(required=True, default=1)

  time_until_turn = db.FloatProperty()
  dmg_buffer = db.FloatProperty(default=0.) # for adding diff. sources of damage together

class PoozleQuestBattle(db.Model):
  turn_uid = db.IntegerProperty()

  message = db.StringProperty(default='The fight begins!')

class PoozleQuestUnitBattle(db.Model):
  uid = db.IntegerProperty(required=True)
  bid = db.IntegerProperty(required=True)

class PoozleQuestPCData(db.Model):
  # information about player controlled characters
  qid = db.IntegerProperty(required=True)
  uid = db.IntegerProperty(required=True)

  in_party = db.BooleanProperty(required=True, default=False)

class PoozleQuestSpellData(db.Model):
  uid = db.IntegerProperty(required=True)
  sid = db.StringProperty(required=True)

  level = db.IntegerProperty(required=True, default=1)

class PoozleQuestBuffData(db.Model):
  uid = db.IntegerProperty(required=True)
  buffid = db.StringProperty(required=True)

  info0 = db.IntegerProperty(default=0)
  info1 = db.IntegerProperty(default=0)
  info2 = db.IntegerProperty(default=0)
  info3 = db.IntegerProperty(default=0)

  stacks = db.IntegerProperty(required=True, default=1)
  duration = db.IntegerProperty(required=True)
