# util functions for puzzles

from models import *

import re

import puzzle_util
import hunt_util

def render_page(user, page):
  tokens = split_page(page)
  codes = [parse_tag(tag)[1] for tag in tokens if is_tag(tag)]
  

def split_page(page):
  exp = '(\[\[\[[SE]:\w+\]\]\])'
  return re.split(exp, page)

def is_tag(token):
  return token[:3] == '[[[' and token[-3:] = ']]]'

def parse_tag(tag):
  return token[3:-3].split(':')


