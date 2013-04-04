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

def get_puzzles_of_hunt(hid):
  query = db.Query(Puzzle)
  query.filter('hid =', hid)

  return list(query)

def puzzle_in_hunt(puzzle, hunt):
  if hunt and puzzle:
    return puzzle.hid == hunt.key().id()
  else:
    return False
    
def puzzle_in_hunt_by_code(puzzle_code, hunt_code):
  hunt = get_hunt_by_code(hunt_code)
  puzzle = puzzle_util.get_puzzle_by_code(puzzle_code)
  return puzzle_in_hunt(puzzle, hunt)