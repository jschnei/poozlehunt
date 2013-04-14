# util functions for users

from models import *

# these functions are bad, I'll replace them later.
# they result in making a lot of round trips to the database
# which will slow things down with millions of users

import puzzle_util
import hunt_util

def get_users():
  return list(db.Query(User))

def is_admin(uid):
  user = User.get_by_id(uid)
  if user and user.is_admin:
    return True
  return False

def user_can_view_puzzle(uid, pid):
  if is_admin(uid):
    return True

  puzzle = puzzle_util.get_puzzle_by_id(pid)
  if puzzle.approved or puzzle.author == uid:
    return True

  return False

def user_can_edit_puzzle(uid, pid):
  if is_admin(uid):
    return True

  puzzle = puzzle_util.get_puzzle_by_id(pid)
  if puzzle.author == uid:
    return True

  return False
  
def user_can_edit_hunt(uid, hid):
  if is_admin(uid):
    return True
    
  hunt = hunt_util.get_hunt_by_id(hid)
  if hunt.author == uid:
    return True
    
  return False
  