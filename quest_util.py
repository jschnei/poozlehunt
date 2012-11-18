# util functions for puzzles

from models import *

import user_util

def get_uqinfo(uid, create_if_none=True):
  query = db.Query(PoozleQuest)
  query.filter('uid =', uid)
  
  ret = query.get()
  if create_if_none and ret is None:
      ret = PoozleQuest(uid = uid,
                        mmap = "noodle",
                        xpos = 7,
                        ypos = 7)

  return ret
