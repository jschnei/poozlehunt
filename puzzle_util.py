# util functions for puzzles

from models import *

def get_puzzles():
  return list(db.Query(Puzzle))

def get_puzzle_by_id(pid):
  return Puzzle.get_by_id(pid)

def get_puzzle_by_code(short_code):
  query = db.Query(Puzzle)
  query.filter('short_code =', short_code)
  return query.get()