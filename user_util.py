# util functions for users

from models import *

# these functions are bad, I'll replace them later.
# they result in making a lot of round trips to the database
# which will slow things down with millions of users

import sys
import puzzle_util

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