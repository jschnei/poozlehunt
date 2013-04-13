# util functions for puzzles

from models import *

import re
import string

import puzzle_util
import hunt_util

def render_page(uid, page, fcodes = []):
  tokens = split_page(page)
  codes = [parse_tag(tag)[1] for tag in tokens if is_tag(tag)]
  
  codebook = get_codebook(uid, codes)  
  # update codebook with forced codes
  for fcode in fcodes:
    codebook[fcode] = True
  
  filtered_page = []
  tag_set = set()
  code_value = True
  for token in tokens:
    if is_tag(token):
      toggle_element(tag_set, parse_tag(token))
      code_value = all(truth_tag(tag, codebook) for tag in tag_set)
    else:
      if code_value:
	filtered_page.append(token)
  
  return string.join(filtered_page, '')
      
def toggle_element(code_set, code):
  if code in code_set:
    code_set.remove(code)
  else:
    code_set.add(code)

def split_page(page):
  exp = '(\[\[\[[YN]:\w+\]\]\])'
  return re.split(exp, page)

def is_tag(token):
  return token[:3] == '[[[' and token[-3:] == ']]]'

def parse_tag(tag):
  return tuple(tag[3:-3].split(':'))

def truth_tag(parsed_tag, codebook):
  if parsed_tag[0] == 'Y':
    return codebook[parsed_tag[1]] 
  else:
    return not codebook[parsed_tag[1]]

def get_codebook(uid, codes):
  return {code: puzzle_util.has_user_solved_by_code(uid, code) for code in codes}
  