#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.ext import db

import jinja2
import os
import sys
import webapp2
import random

import auth_util
import puzzle_util
import user_util
import hunt_util

import pquest

from models import *

jinja_loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
jinja_env = jinja2.Environment(autoescape=True,
                               loader = jinja_loader)

class MainHandler(webapp2.RequestHandler):
  def render(self):
    template = jinja_env.get_template('main.html')
    self.response.out.write(template.render(logged_in = False))

  def get(self):
    if auth_util.auth_into_site(self) :
      self.redirect('/puzzles')
    else:
      self.render()

# deal with trailing /s
class TrailingHandler(webapp2.RequestHandler):
  def get(self, path):
    self.redirect(path)

class LoginHandler(webapp2.RequestHandler):
  def render(self, errors = None):
    template = jinja_env.get_template('login.html')
    html = template.render(errors = errors,
                           logged_in = False)
    self.response.out.write(html)

  def get(self):
    if auth_util.auth_into_site(self) :
      self.redirect('/puzzles')
    else:
      self.render()

  def post(self):
    if auth_util.auth_into_site(self) :
      self.redirect('/puzzles')
    else:
      username = self.request.get('username')
      password = self.request.get('password')

      errors = []

      vUser = auth_util.valid_username(username)
      vPass = auth_util.valid_password(password)


      if vUser and vPass:
          query = db.Query(User)
          query.filter('name =', username)
          query.filter('password =', password)
          rdusers = list(query.run())
          if rdusers:
              u = rdusers[0]
              uid = u.key().id()
              auth = auth_util.gen_cookie(uid)
              self.response.headers.add_header('Set-Cookie', 'auth = %s; Path = /' % auth)
              self.redirect('/')
          else:
              errors.append('Invalid Username/Password Combination')
      else:
          errors.append('Invalid Username/Password Combination')

      self.render(errors)


class RegisterHandler(webapp2.RequestHandler):
  def render(self, errors = None):
    template = jinja_env.get_template('register.html')
    html = template.render(errors = errors, 
                           logged_in = False)
    self.response.out.write(html)

  def get(self):
    if auth_util.auth_into_site(self):
      self.redirect('/puzzles')
    else:
      self.render()

  def post(self):
    if auth_util.auth_into_site(self):
      self.redirect('/puzzles')
    else:      
      username = self.request.get('username')
      password = self.request.get('password')
      verify = self.request.get('verify')
      email = self.request.get('email')

      errors = []
      if not auth_util.valid_username(username):
        errors.append("That's not a valid username")
      if not auth_util.valid_password(password):
        errors.append("That's not a valid password")
      if not auth_util.valid_verify(verify, password):
        errors.append("Your passwords do not match")
      if not auth_util.valid_email(email):
        errors.append("That's not a valid e-mail")

      
      # check if username is already taken
      query = db.Query(User)
      query.filter('name =', username)
      if query.get():
        errors.append("That user name is already taken")


      if not errors:
        u = User(name = username, password = password, email = email)
        u.put()
        uid = u.key().id()
        auth = auth_util.gen_cookie(uid)
        self.response.headers.add_header('Set-Cookie', 'auth = %s; Path = /' % auth)
        self.redirect('/')
      else:
        self.render(errors)

class LogoutHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers.add_header('Set-Cookie', 'auth=; Path=/')
    self.redirect('/')

class PuzzlesHandler(webapp2.RequestHandler):
  def render(self, puzzles, completion):
    template = jinja_env.get_template('puzzles.html')

    puzzle_info = zip(puzzles, completion)
    self.response.out.write(template.render(puzzle_info = puzzle_info,
                                            logged_in = True))

  def get(self):
    uid = auth_util.auth_into_site(self)
    if uid:
      puzzles = puzzle_util.get_puzzles()

      puzzle_filter = lambda k: (user_util.user_can_view_puzzle(uid, k.key().id()) and not k.author == uid)
      puzzles = filter(puzzle_filter, puzzles)

      completion = [puzzle_util.has_user_solved(uid, p.key().id()) for p in puzzles]

      self.render(puzzles, completion)
    else:
      self.redirect('/')

class OwnPuzzlesHandler(webapp2.RequestHandler):
  def render(self, puzzles, completion):
    template = jinja_env.get_template('ownpuzzles.html')

    puzzle_info = zip(puzzles, completion)
    self.response.out.write(template.render(puzzle_info = puzzle_info,
                                            logged_in = True))

  def get(self):
    uid = auth_util.auth_into_site(self)
    
    if uid:
      puzzles = puzzle_util.get_puzzles()

      puzzle_filter = lambda k: (k.author == uid)
      puzzles = filter(puzzle_filter, puzzles)

      completion = [puzzle_util.has_user_solved(uid, p.key().id()) for p in puzzles]
      self.render(puzzles, completion)
    else:
      self.redirect('/')

class PuzzleHandler(webapp2.RequestHandler):
  def render(self, user, puzzle, up_info):
    template = jinja_env.get_template('puzzle.html')
    self.response.out.write(template.render(user = user, 
                                            puzzle = puzzle, 
                                            up_info = up_info,
                                            logged_in = True))

  def get(self, short_code):
    uid = auth_util.auth_into_site(self)
    if uid:
      puzzle = puzzle_util.get_puzzle_by_code(short_code)
      pid = puzzle.key().id()
      user = User.get_by_id(uid)

      up_info = puzzle_util.get_upinfo(uid, pid)

      self.render(user, puzzle, up_info)
    else:
      self.redirect('/')

class PuzzleSubmitAnswerHandler(webapp2.RequestHandler):
  # handler for submitted answers to puzzles
  def get(self, short_code):
    self.redirect('/puzzles/' + short_code)

  def post(self, short_code):
    answer = self.request.get('answer')
    uid = auth_util.auth_into_site(self)
    puzzle = puzzle_util.get_puzzle_by_code(short_code)
    pid = puzzle.key().id()

    up_info = puzzle_util.get_upinfo(uid, pid)
    up_info.tries += 1
    
    if puzzle.answer == answer:
      up_info.solved = True

    up_info.put()

    self.redirect('/puzzles/' + short_code) #temporary!

class PuzzleSubmitPageHandler(webapp2.RequestHandler):
  # handler for puzzle submission page
  def render(self, hunts):
    template = jinja_env.get_template('puzzle_submit.html')
    self.response.out.write(template.render(logged_in = 'True', 
					     hunts = hunts))

  def get(self):
    uid = auth_util.auth_into_site(self)
    if uid:
      hunts = hunt_util.get_hunts_by_user(uid)
      self.render(hunts)

class PuzzleSubmitHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect('/puzzle_submit')

  def post(self):
    uid = auth_util.auth_into_site(self)
    create_success = False

    if uid:
      title = self.request.get('title')
      scode = self.request.get('scode')
      answer = self.request.get('answer')
      hunt = int(self.request.get('hunt'))

      if title != '' and answer != '' and scode != '':
        if hunt_util.is_user_author(uid, hunt) and not puzzle_util.code_used(scode):
          puzzle = Puzzle(title = title,
          short_code = scode,
          answer = answer,
          text = 'Insert puzzle text here',
          author = uid,
          hid = hunt,
          approved = user_util.is_admin(uid))

          puzzle.put()

          up_info = UserPuzzleInfo(uid = uid,
                                   pid = puzzle.key().id(),
                                   author = True,
                                   solved = True)
          up_info.put()

          create_success = True
          


    if create_success: 
      self.redirect('/puzzles/' + scode + '/edit')
    else:
      self.redirect('/puzzles')
 
class PuzzleApproveHandler(webapp2.RequestHandler):
  def get(self, short_code):
    self.redirect('/puzzles/' + short_code)

  def post(self, short_code):
    uid = auth_util.auth_into_site(self)
    pid = puzzle_util.get_puzzle_by_code(short_code).key().id()

    puzzle_util.approve_puzzle(uid, pid)

    self.redirect('/puzzles/' + short_code)

class PuzzleEditHandler(webapp2.RequestHandler):
  def render(self, user, puzzle, puzzle_files, up_info):
    template = jinja_env.get_template('puzzle_edit.html')
    self.response.out.write(template.render(user = user, 
                                            puzzle = puzzle, 
                                            puzzle_files = puzzle_files,
                                            up_info = up_info,
                                            logged_in = True))

  def get(self, short_code):
    uid = auth_util.auth_into_site(self)
    
    puzzle = None
    while not puzzle:
      puzzle = puzzle_util.get_puzzle_by_code(short_code)
    
    pid = puzzle.key().id()
    user = User.get_by_id(uid)

    if user_util.user_can_edit_puzzle(uid, pid):
      up_info = puzzle_util.get_upinfo(uid, pid)
      puzzle_files = puzzle_util.get_puzzle_files(pid)
      self.render(user, puzzle, puzzle_files, up_info)
    else:
      self.redirect('/ownpuzzles')

class PuzzleFileHandler(webapp2.RequestHandler):
  def get(self, short_code, fname):
    pfile = puzzle_util.get_puzzle_file_by_code(short_code, fname)
    if pfile:
      self.response.headers['Content-Type'] = pfile.mime_type.encode('ascii', 'ignore')
      self.response.out.write(pfile.pfile)
    else:
      self.response.out.write('error: could not load file')

class PuzzleEditSubmitHandler(webapp2.RequestHandler):
  def get(self, short_code):
    self.redirect('/ownpuzzles')

  def post(self, short_code):
    uid = auth_util.auth_into_site(self)

    if uid:
      puzzle = puzzle_util.get_puzzle_by_code(short_code)

      if user_util.user_can_edit_puzzle(uid, puzzle.key().id()):
        puzzle.title = self.request.get('title')
        if self.request.get('uploadhtml'):
	  puzzle.text = self.request.get('uploadhtml')
        else:
	  puzzle.text = self.request.get('input')
        puzzle.answer = self.request.get('answer')

        puzzle.put()


    self.redirect('/ownpuzzles')

class PuzzleEditUploadHandler(webapp2.RequestHandler):
  # handler for file submission
  def get(self, short_code):
    self.redirect('/ownpuzzles')

  def post(self, short_code):
    uid = auth_util.auth_into_site(self)
    if uid:
      puzzle = puzzle_util.get_puzzle_by_code(short_code)
      if user_util.user_can_edit_puzzle(uid, puzzle.key().id()):
	
	pfile = self.request.get('uploadfile')
	fname = self.request.POST['uploadfile'].filename
	mime_type = puzzle_util.get_mime_type(fname.split('.')[-1])

	db_file = PuzzleFile(pid = puzzle.key().id(),
			    fname = fname,
			    mime_type = mime_type, 
			    pfile = db.Blob(pfile))
	db_file.put()

    self.redirect('/ownpuzzles')

class HuntsHandler(webapp2.RequestHandler):
  def render(self, hunts):
    template = jinja_env.get_template('hunts.html')

    self.response.out.write(template.render(hunts = hunts, logged_in = True))

  def get(self):
    uid = auth_util.auth_into_site(self)
    hunts = hunt_util.get_hunts()
    # no filters for hunts here yet

    self.render(hunts)

class HuntHandler(webapp2.RequestHandler):
  def render(self, hunt, puzzles, completion):
    template = jinja_env.get_template('hunt.html')

    puzzle_info = zip(puzzles, completion)
    self.response.out.write(template.render(hunt = hunt, puzzle_info = puzzle_info))

  def get(self, short_code):
    uid = auth_util.auth_into_site(self)
    
    if uid:
      hunt = hunt_util.get_hunt_by_code(short_code)
      puzzles = hunt_util.get_puzzles_of_hunt(hunt.key().id())

      completion = [puzzle_util.has_user_solved(uid, p.key().id()) for p in puzzles]

      self.render(hunt, puzzles, completion)

class HuntCreateHandler(webapp2.RequestHandler):
  def render(self):
    template = jinja_env.get_template('create_hunt.html')

    self.response.out.write(template.render())

  def get(self):
    uid = auth_util.auth_into_site(self)
    
    if uid:
      self.render()

class HuntCreateSubmitHandler(webapp2.RequestHandler):
  # we should really refactor this stuff soon
  def get(self):
    self.redirect('/create_hunt')

  def post(self):
    uid = auth_util.auth_into_site(self)
    title = self.request.get('title')
    short_code = self.request.get('short_code')

    if uid and title != '' and short_code != '':
      #todo: add ajax check that short_code doesn't exist
      hunt = PuzzleHunt(title = title,
                        short_code = short_code,
                        author = uid)

      hunt.put()

      self.redirect('/hunts/%s/edit' % short_code)

    else:
      self.redirect('/create_hunt')

class HuntEditHandler(webapp2.RequestHandler):
  def render(self, user, hunt, puzzles):
    template = jinja_env.get_template('edit_hunt.html')

    self.response.out.write(template.render(user = user,
                                            hunt = hunt,
					     puzzles = puzzles,
                                            logged_in = True))

  def get(self, short_code):
    hunt = None
    while not hunt:
      hunt = hunt_util.get_hunt_by_code(short_code)
      
    
    uid = auth_util.auth_into_site(self)
    hid = hunt.key().id()
    user = User.get_by_id(uid)

    puzzles = hunt_util.get_puzzles_of_hunt(hid)

    if True: # todo: user_can_edit_hunt(uid, hid)
      self.render(user, hunt, puzzles)
    else:
      self.redirect('/hunts')

class HuntEditSubmitHandler(webapp2.RequestHandler):
  def get(self, short_code):
    self.redirect('/hunts')

  def post(self, short_code):
    uid = auth_util.auth_into_site(self)

    if uid:
      puzzle = puzzle_util.get_puzzle_by_code(short_code)

      if user_util.user_can_edit_puzzle(uid, puzzle.key().id()):
        puzzle.title = self.request.get('title')
        puzzle.text = self.request.get('input')
        puzzle.answer = self.request.get('answer')

        puzzle.put()

    self.redirect('/puzzles')

    

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('(.*)/', TrailingHandler),
                               ('/login', LoginHandler),
                               ('/register', RegisterHandler),
                               ('/logout', LogoutHandler),
                               ('/puzzles', PuzzlesHandler),
                               ('/ownpuzzles', OwnPuzzlesHandler),
                               ('/puzzles/([a-zA-Z0-9]+)', PuzzleHandler),
                               ('/puzzles/([a-zA-Z0-9]+)/files/(.*)', PuzzleFileHandler),
                               ('/puzzles/([a-zA-Z0-9]+)/submit', PuzzleSubmitAnswerHandler),
                               ('/puzzles/([a-zA-Z0-9]+)/approve', PuzzleApproveHandler),
                               ('/puzzles/([a-zA-Z0-9]+)/edit', PuzzleEditHandler),
                               ('/puzzles/([a-zA-Z0-9]+)/edit_submit', PuzzleEditSubmitHandler),
                               ('/puzzles/([a-zA-Z0-9]+)/edit_upload', PuzzleEditUploadHandler),
                               ('/puzzle_submit', PuzzleSubmitPageHandler),
                               ('/puzzle_submit/submit', PuzzleSubmitHandler),
                               ('/hunts', HuntsHandler),
                               ('/create_hunt', HuntCreateHandler),
                               ('/create_hunt/submit', HuntCreateSubmitHandler),
                               ('/hunts/([a-zA-Z0-9]+)', HuntHandler),
                               ('/hunts/([a-zA-Z0-9]+)/edit', HuntEditHandler),
                               ('/hunts/([a-zA-Z0-9]+)/edit_submit', HuntEditSubmitHandler),
			       ('/hunts/([a-zA-Z0-9]+)/edit_add', HuntEditAddPuzzleHandler),
			       ('/hunts/([a-zA-Z0-9]+)/edit_remove', HuntEditRemovePuzzleHandler),
                ('/pquest', pquest.PoozleQuestHandler),
                ('/pquest/move', pquest.PoozleQuestMoveHandler),
                ('/pquest/action', pquest.PoozleQuestActionHandler),
		('/pquest/inventory', pquest.PoozleQuestInvHandler),
		('/pquest/inventory/action', pquest.PoozleQuestInvActionHandler),
				],

                              debug=True)
