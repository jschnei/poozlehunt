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

def get_upinfo(uid, pid):
  query = db.Query(UserPuzzleInfo)
  query.filter('uid =', uid)
  query.filter('pid =', pid)
  
  return query.get()

def has_user_solved(uid, pid):
  upinfo = get_upinfo(uid, pid)
  return upinfo.solved if upinfo else False

def has_user_tried(uid, pid):
  upinfo = get_upinfo(uid, pid)
  return (upinfo.tries > 0) if upinfo else False

