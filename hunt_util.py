# util functions for puzzles

from models import *

import user_util

def get_hunt_by_id(hid):
  return PuzzleHunt.get_by_id(hid)

def get_hunt_by_code(short_code):
  query = db.Query(PuzzleHunt)
  query.filter('short_code =', short_code)
  return query.get()

def get_puzzles_of_hunt(hid):
  query = db.Query(PuzzleHuntPuzzleInfo)
  query.filter('hid =', hid)    

  return [puzzle_util.get_puzzle_by_id(q.pid) for q in list(query)]

def add_puzzle_to_hunt(pid, hid):
  p = PuzzleHuntPuzzleInfo(hid, pid)
  h = get_hunt_by_id(hid)
  h.num_puzzles += 1

  p.put()
  h.put()
