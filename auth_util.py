# authutil.py
# This is a module that contains useful functions for authorization (login/signup)
# that are independent of the main webpage flow.

import hashlib
import re
import webapp2

from models import *

# cookie hash secret
SECRET = 'mesakoisnotrude'

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^^[\S]+@[\S]+\.[\S]+$$")

# checks whether the user has a valid cookie
# and is allowed to auth into the site
# if the user is, it returns the UID
# otherwise it returns None 
# (as opposed to auth_into_game doesn't
# do any redirects since for some pages
# we want the user to be logged in and for
# others we don't)
def auth_into_site(handler):
  auth = handler.request.cookies.get('auth', '')
  if check_cookie(auth):
    uid = get_uid(auth)  

    if not User.get_by_id(uid):
      # their cookie is valid, but this user doesn't
      # actually exist (it was maybe deleted, or the user
      # is hacking and knows our hash secret?)
      return None

    return uid
  
  return None

# methods for dealing with cookies

def hash_str(s):
  return hashlib.md5(s+SECRET).hexdigest()

def gen_cookie(uid):
  return str(uid) + "|" + hash_str(str(uid))

def check_cookie(cookie):
  parts = cookie.split('|')
  if len(parts) != 2: 
    return False
  if hash_str(parts[0]) == parts[1]:
    return True
  return False

def get_uid(cookie):
  parts = cookie.split('|')
  if len(parts) != 2: 
    return None
  return int(parts[0])

# login/signup form validations

def valid_teamname(teamname):
  return len(teamname) > 0 and len(teamname) < 120

def valid_username(username):
  return USER_RE.match(username)

def valid_password(password):
  return PASSWORD_RE.match(password)

def valid_verify(verify, password):
  return verify == password

def valid_email(email):
  return email == '' or EMAIL_RE.match(email)