# util functions for puzzles

from models import *

import user_util

def get_puzzles():
  return list(db.Query(Puzzle))

def get_puzzle_by_id(pid):
  return Puzzle.get_by_id(pid)

def get_puzzle_by_code(short_code):
  query = db.Query(Puzzle)
  query.filter('short_code =', short_code)
  return query.get()

def code_used(short_code):
  query = db.Query(Puzzle)
  query.filter('short_code =', short_code)
  
  return True if query.get() else False

def puzzle_in_hunt(puzzle):
  return (puzzle.hid != -1)

def get_upinfo(uid, pid, create_if_none=True):
  query = db.Query(UserPuzzleInfo)
  query.filter('uid =', uid)
  query.filter('pid =', pid)
  
  ret = query.get()
  if create_if_none and ret is None:
    ret = UserPuzzleInfo(uid = uid,
			 pid = pid,
			 solved = False,
			 tries = 0)

  return ret

def has_user_solved(uid, pid):
  upinfo = get_upinfo(uid, pid)
  return upinfo.solved if upinfo else False

def has_user_tried(uid, pid):
  upinfo = get_upinfo(uid, pid)
  return (upinfo.tries > 0) if upinfo else False

def approve_puzzle(uid, pid):
  if uid and user_util.is_admin(uid):
    puzzle = get_puzzle_by_id(pid)
    puzzle.approved = True

    puzzle.put()


def get_puzzle_file(pid, fname):
  query = db.Query(PuzzleFile)
  query.filter('pid =', pid)
  query.filter('fname =', fname)

  return query.get()

def get_puzzle_file_by_code(short_code, fname):
  return get_puzzle_file(int(get_puzzle_by_code(short_code).key().id()), fname)

def get_puzzle_files(pid):
  query = db.Query(PuzzleFile)
  query.filter('pid =', pid)
  
  return list(query)

def get_puzzle_files_by_code(short_code):
  return get_puzzle_files(int(get_puzzle_by_code(short_code).key().id()))

mime_map = {'gif': 'image/gif', 
            'png': 'image/png', 
            'jpg': 'image/jpg', 
            'jpeg': 'image/jpeg', 
            'pdf': 'application/pdf'}

def get_mime_type(ext):
  return mime_map[ext] if ext in mime_map else 'text/plain'
