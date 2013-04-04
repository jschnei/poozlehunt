# util functions for puzzles

from models import *

import user_util
import puzzle_util

def get_hunts():
  return list(db.Query(PuzzleHunt))

def get_hunt_by_id(hid):
  return PuzzleHunt.get_by_id(hid)

def get_hunt_by_code(short_code):
  query = db.Query(PuzzleHunt)
  query.filter('short_code =', short_code)
  return query.get()

def get_hunts_by_user(uid):
  query = db.Query(PuzzleHunt)
  query.filter('author =', int(uid))
  
  return list(query)

def code_used(short_code):
  query = db.Query(PuzzleHunt)
  query.filter('short_code =', short_code)
  
  return True if query.get() else False

def is_user_author(uid, hid):
  if hid==-1: # general non-hunt puzzles
    return True
  
  hunt = get_hunt_by_id(hid)
  return (hunt.author == uid)

def get_uhinfo(uid, hid, create_if_none=True):
  query = db.Query(UserHuntInfo)
  query.filter('uid =', uid)
  query.filter('hid =', hid)

  ret = query.get()
  if create_if_none and not ret:
    ret = UserHuntInfo(uid = uid,
		       hid = hid,
		       solved = False)

  return ret

def get_puzzles_of_hunt(hid):
  query = db.Query(PuzzleHuntPuzzleInfo)
  query.filter('hid =', hid)    

  return [puzzle_util.get_puzzle_by_id(q.pid) for q in list(query)]

def add_puzzle_to_hunt(pid, hid):
  p = PuzzleHuntPuzzleInfo(hid, pid)
  h = get_hunt_by_id(hid)
  
  p.put()
  h.put()
