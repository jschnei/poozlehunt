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
import string

import auth_util
import hunt_util
import puzzle_util
import render_util
import user_util

import pquest

import adventure
import adventure_util
import interactions
import items

from models import *

jinja_loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
jinja_env = jinja2.Environment(autoescape=True,
                               loader = jinja_loader)

class AuthHandler(webapp2.RequestHandler):
  def get(self, *args):
    self.uid = auth_util.auth_into_site(self)
    if self.uid:
      self.aget(*args)
    else:
      self.redirect('/')
  
  def post(self, *args):
    self.uid = auth_util.auth_into_site(self)
    if self.uid:
      self.apost(*args)
    else:
      self.redirect('/')
    

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

class PuzzlesHandler(AuthHandler):
  def render(self, puzzles, completion):
    template = jinja_env.get_template('puzzles.html')

    puzzle_info = zip(puzzles, completion)
    self.response.out.write(template.render(puzzle_info = puzzle_info,
                                            logged_in = True))

  def aget(self):
    puzzles = puzzle_util.get_puzzles()

    puzzle_filter = lambda k: (user_util.user_can_view_puzzle(self.uid, k.key().id()) and 
				not puzzle_util.puzzle_in_hunt(k) and 
				not k.author == self.uid)
    puzzles = filter(puzzle_filter, puzzles)

    completion = [puzzle_util.has_user_solved(uid, p.key().id()) for p in puzzles]

    self.render(puzzles, completion)

class OwnPuzzlesHandler(AuthHandler):
  def render(self, puzzles, completion):
    template = jinja_env.get_template('ownpuzzles.html')

    puzzle_info = zip(puzzles, completion)
    self.response.out.write(template.render(puzzle_info = puzzle_info,
                                            logged_in = True))

  def aget(self):  
    puzzles = puzzle_util.get_puzzles()

    puzzle_filter = lambda k: (k.author == self.uid)
    puzzles = filter(puzzle_filter, puzzles)

    completion = [puzzle_util.has_user_solved(self.uid, p.key().id()) for p in puzzles]
    self.render(puzzles, completion)


class PuzzleHandler(AuthHandler):
  def render(self, user, puzzle, up_info, rend_text):
    template = jinja_env.get_template('puzzle.html')
    self.response.out.write(template.render(user = user, 
                                            puzzle = puzzle, 
                                            up_info = up_info,
                                            rend_text = rend_text,
                                            logged_in = True))

  def aget(self, short_code):
    puzzle = puzzle_util.get_puzzle_by_code(short_code)
    pid = puzzle.key().id()
    user = User.get_by_id(self.uid)

    up_info = puzzle_util.get_upinfo(self.uid, pid)
    rend_text = render_util.render_page(self.uid, puzzle.text)
    
    self.render(user, puzzle, up_info, rend_text)
      
class PuzzleSubmitAnswerHandler(AuthHandler):
  def render(self, user, puzzle, up_info, rend_text, errors = None):
    template = jinja_env.get_template('puzzle.html')
    self.response.out.write(template.render(user = user, 
                                            puzzle = puzzle, 
                                            up_info = up_info,
                                            rend_text = rend_text,
                                            errors = errors,
                                            logged_in = True))
  
  # handler for submitted answers to puzzles
  def aget(self, short_code):
    self.redirect('/puzzles/' + short_code)

  def apost(self, short_code):
    answer = self.request.get('answer')
    puzzle = puzzle_util.get_puzzle_by_code(short_code)
    pid = puzzle.key().id()

    up_info = puzzle_util.get_upinfo(self.uid, pid)
    up_info.tries += 1
    
    if puzzle_util.check_answer(puzzle.answer, answer):
      up_info.solved = True
      up_info.put()
      
      user = User.get_by_id(self.uid)
      rend_text = render_util.render_page(self.uid, puzzle.text, fcodes = [short_code])
      
      self.render(user, puzzle, up_info, rend_text)
      
    else:
      up_info.put()
      
      user = User.get_by_id(self.uid)
      rend_text = render_util.render_page(self.uid, puzzle.text)
      
      errors = ['That answer is incorrect']
      
      self.render(user, puzzle, up_info, rend_text, errors)
      

class PuzzleSubmitPageHandler(AuthHandler):
  # handler for puzzle submission page
  def render(self, hunts):
    template = jinja_env.get_template('puzzle_submit.html')
    self.response.out.write(template.render(logged_in = 'True', 
					     hunts = hunts))

  def aget(self):
    hunts = hunt_util.get_hunts_by_user(self.uid)
    self.render(hunts)

class PuzzleSubmitHandler(AuthHandler):
  def aget(self):
    self.redirect('/puzzle_submit')

  def apost(self):
    create_success = False

    
    title = self.request.get('title')
    scode = self.request.get('scode')
    answer = self.request.get('answer')
    hunt = int(self.request.get('hunt'))

    if title != '' and answer != '' and scode != '':
      if hunt_util.is_user_author(self.uid, hunt) and not puzzle_util.code_used(scode):
	puzzle = Puzzle(title = title,
	short_code = scode,
	answer = answer,
	text = 'Insert puzzle text here',
	author = self.uid,
	hid = hunt,
	approved = user_util.is_admin(self.uid))

	puzzle.put()

	up_info = UserPuzzleInfo(uid = self.uid,
				  pid = puzzle.key().id(),
				  author = True,
				  solved = True)
	up_info.put()

	create_success = True
          
    if create_success: 
      self.redirect('/puzzles/' + scode + '/edit')
    else:
      self.redirect('/puzzles')
 
class PuzzleApproveHandler(AuthHandler):
  def aget(self, short_code):
    self.redirect('/puzzles/' + short_code)

  def apost(self, short_code):
    pid = puzzle_util.get_puzzle_by_code(short_code).key().id()

    puzzle_util.approve_puzzle(self.uid, pid)

    self.redirect('/puzzles/' + short_code)

class PuzzleEditHandler(AuthHandler):
  def render(self, user, puzzle, puzzle_files, up_info):
    template = jinja_env.get_template('puzzle_edit.html')
    self.response.out.write(template.render(user = user, 
                                            puzzle = puzzle, 
                                            puzzle_files = puzzle_files,
                                            up_info = up_info,
                                            logged_in = True))

  def aget(self, short_code):
    puzzle = None
    while not puzzle:
      puzzle = puzzle_util.get_puzzle_by_code(short_code)
    
    pid = puzzle.key().id()
    user = User.get_by_id(self.uid)

    if user_util.user_can_edit_puzzle(self.uid, pid):
      up_info = puzzle_util.get_upinfo(self.uid, pid)
      puzzle_files = puzzle_util.get_puzzle_files(pid)
      self.render(user, puzzle, puzzle_files, up_info)
    else:
      self.redirect('/ownpuzzles')

class PuzzleFileHandler(AuthHandler):
  def aget(self, short_code, fname):
    pfile = puzzle_util.get_puzzle_file_by_code(short_code, fname)
    if pfile:
      self.response.headers['Content-Type'] = pfile.mime_type.encode('ascii', 'ignore')
      self.response.out.write(pfile.pfile)
    else:
      self.response.out.write('error: could not load file')

class PuzzleEditSubmitHandler(AuthHandler):
  def aget(self, short_code):
    self.redirect('/ownpuzzles')

  def apost(self, short_code):
    puzzle = puzzle_util.get_puzzle_by_code(short_code)

    if user_util.user_can_edit_puzzle(self.uid, puzzle.key().id()):
      puzzle.title = self.request.get('title')
      if self.request.get('uploadhtml'):
	puzzle.text = self.request.get('uploadhtml')
      else:
	puzzle.text = self.request.get('input')
      
      if self.request.get('ptype') == 'puzzle':
	puzzle.is_puzzle = True
	puzzle.answer = self.request.get('answer')
      else:
	puzzle.is_puzzle = False
	puzzle.answer = 'notapuzzle'

      puzzle.put()


    self.redirect('/ownpuzzles')

class PuzzleEditUploadHandler(AuthHandler):
  # handler for file submission
  def aget(self, short_code):
    self.redirect('/puzzles/' + short_code)

  def apost(self, short_code):
    puzzle = puzzle_util.get_puzzle_by_code(short_code)
    if user_util.user_can_edit_puzzle(self.uid, puzzle.key().id()):
      
      pfile = self.request.get('uploadfile')
      fname = self.request.POST['uploadfile'].filename
      mime_type = puzzle_util.get_mime_type(fname.split('.')[-1])

      db_file = PuzzleFile(pid = puzzle.key().id(),
			  fname = fname,
			  mime_type = mime_type, 
			  pfile = db.Blob(pfile))
      db_file.put()

    self.redirect('/puzzles/' + short_code + '/edit')

class HuntsHandler(AuthHandler):
  def render(self, hunts):
    template = jinja_env.get_template('hunts.html')

    self.response.out.write(template.render(hunts = hunts, logged_in = True))

  def aget(self):
    hunts = [hunt for hunt in hunt_util.get_hunts() if hunt.author != self.uid]
    self.render(hunts)

class OwnHuntsHandler(AuthHandler):
  def render(self, hunts):
    template = jinja_env.get_template('ownhunts.html')

    self.response.out.write(template.render(hunts = hunts, logged_in = True))

  def aget(self):
    hunts = hunt_util.get_hunts_by_user(self.uid)

    self.render(hunts)


class HuntHandler(AuthHandler):
  def render(self, hunt, puzzles, completion):
    template = jinja_env.get_template('hunt.html')

    puzzle_info = zip(puzzles, completion)
    self.response.out.write(template.render(hunt = hunt, 
					     puzzle_info = puzzle_info,
					     logged_in = True))

  def aget(self, short_code):
    hunt = hunt_util.get_hunt_by_code(short_code)
    main_page = hunt_util.get_main_page(hunt)
    
    if main_page:
      self.redirect('/hunts/' + hunt.short_code + '/puzzles/' + main_page.short_code)
    else:
      puzzles = hunt_util.get_puzzles_of_hunt(hunt.key().id())

      completion = [puzzle_util.has_user_solved(self.uid, p.key().id()) for p in puzzles]

      self.render(hunt, puzzles, completion)

class HuntCreateHandler(AuthHandler):
  def render(self):
    template = jinja_env.get_template('create_hunt.html')

    self.response.out.write(template.render(logged_in = True))

  def aget(self):
    self.render()
    

class HuntCreateSubmitHandler(AuthHandler):
  def aget(self):
    self.redirect('/create_hunt')

  def apost(self):
    title = self.request.get('title')
    short_code = self.request.get('short_code')

    if (self.uid and title and short_code and 
	not puzzle_util.code_used(short_code)):
      hunt = PuzzleHunt(title = title,
                        short_code = short_code,
                        author = self.uid)

      hunt.put()

      self.redirect('/hunts/%s/edit' % short_code)
    else:
      self.redirect('/create_hunt')

class HuntEditHandler(AuthHandler):
  def render(self, user, hunt, puzzles, main_page):
    template = jinja_env.get_template('edit_hunt.html')

    self.response.out.write(template.render(user = user,
                                            hunt = hunt,
					     puzzles = puzzles,
					     main_page = main_page,
                                            logged_in = True))

  def aget(self, short_code):
    hunt = None
    while not hunt:
      hunt = hunt_util.get_hunt_by_code(short_code)
      
    hid = hunt.key().id()
    user = User.get_by_id(self.uid)

    if user_util.user_can_edit_hunt(self.uid, hid): 
      puzzles = hunt_util.get_puzzles_of_hunt(hid)
      main_page = hunt_util.get_main_page(hunt)
      self.render(user, hunt, puzzles, main_page)
    else:
      self.redirect('/ownhunts')

class HuntSetMainPageHandler(AuthHandler):
  def aget(self, hunt_code, pid):
    self.redirect('/hunts')

  def apost(self, hunt_code, pid):
    hunt = hunt_util.get_hunt_by_code(hunt_code)
    puzzle = puzzle_util.get_puzzle_by_id(int(pid))

    if (user_util.user_can_edit_hunt(self.uid, hunt.key().id()) and
	hunt_util.puzzle_in_hunt(puzzle, hunt)):
      hunt.main_page = int(pid)
      hunt.put()

    self.redirect('/hunts/' + hunt_code + '/edit')

class HuntEditSubmitHandler(AuthHandler):
  def aget(self, short_code):
    self.redirect('/hunts')

  def apost(self, short_code):
    hunt = hunt_util.get_hunt_by_code(short_code)

    if user_util.user_can_edit_hunt(self.uid, hunt.key().id()):
      hunt.title = self.request.get('title')

      hunt.put()

    self.redirect('/ownhunts')

class HuntPuzzleHandler(AuthHandler):
  def render(self, user, puzzle, hunt, up_info, rend_text):
    template = jinja_env.get_template('puzzle.html')
    self.response.out.write(template.render(user = user, 
                                            puzzle = puzzle, 
                                            hunt = hunt,
                                            up_info = up_info,
                                            rend_text = rend_text,
                                            logged_in = True))

  def aget(self, hunt_code, puzzle_code):
    hunt = hunt_util.get_hunt_by_code(hunt_code)
    puzzle = puzzle_util.get_puzzle_by_code(puzzle_code)
    
    if hunt_util.puzzle_in_hunt(puzzle, hunt):
      hid = hunt.key().id()
      pid = puzzle.key().id()
      
      user = User.get_by_id(self.uid)

      up_info = puzzle_util.get_upinfo(self.uid, pid)
      rend_text = render_util.render_page(self.uid, puzzle.text)

      self.render(user, puzzle, hunt, up_info, rend_text)
    else:
      self.redirect('/hunts')

class HuntPuzzleSubmitAnswerHandler(AuthHandler):
  def render(self, user, puzzle, hunt, up_info, rend_text, errors = None):
    template = jinja_env.get_template('puzzle.html')
    self.response.out.write(template.render(user = user, 
                                            puzzle = puzzle, 
                                            hunt = hunt,
                                            up_info = up_info,
                                            rend_text = rend_text,
                                            errors = errors,
                                            logged_in = True))
  
  # handler for submitted answers to puzzles
  def aget(self, hunt_code, puzzle_code):
    self.redirect('/hunts/' + hunt_code + '/puzzles/' + puzzle_code)

  def apost(self, hunt_code, puzzle_code):
    answer = self.request.get('answer')
    
    hunt = hunt_util.get_hunt_by_code(hunt_code)
    puzzle = puzzle_util.get_puzzle_by_code(puzzle_code)
    pid = puzzle.key().id()

    up_info = puzzle_util.get_upinfo(self.uid, pid)
    up_info.tries += 1
    if hunt_util.puzzle_in_hunt(puzzle, hunt):
      if puzzle_util.check_answer(puzzle.answer, answer):
	up_info.solved = True
	up_info.put()
	
	user = User.get_by_id(self.uid)
	rend_text = render_util.render_page(self.uid, puzzle.text, fcodes = [puzzle_code])
	
	self.render(user, puzzle, hunt, up_info, rend_text)
	
      else:
	up_info.put()
	
	user = User.get_by_id(self.uid)
	rend_text = render_util.render_page(self.uid, puzzle.text)
	
	errors = ['That answer is incorrect']
	
	self.render(user, puzzle, hunt, up_info, rend_text, errors)
    else:
      self.redirect('/hunts')

class HuntPuzzleFileHandler(AuthHandler):
  def aget(self, hunt_code, puzzle_code, fname):
    if hunt_util.puzzle_in_hunt_by_code(puzzle_code, hunt_code):
      pfile = puzzle_util.get_puzzle_file_by_code(puzzle_code, fname)
      if pfile:
	self.response.headers['Content-Type'] = pfile.mime_type.encode('ascii', 'ignore')
	self.response.out.write(pfile.pfile)
      else:
	self.response.out.write('error: could not load file')
    else:
      self.response.out.write('error: puzzle not in hunt')

class AdventureHandler(AuthHandler):
  def aget(self):
    template = jinja_env.get_template('adventure.html')
    self.response.out.write(template.render(logged_in = False))

class AdventureRealTimeHandler(AuthHandler):
  def apost(self):
    cookie = self.request.cookies.get('id', '')
    s = ''
    p = None

    if cookie == '':
        rgen = ''.join(random.choice(string.letters) for i in xrange(32))
        self.response.headers.add_header('Set-Cookie', 'id = %s; Path = /' % rgen)

        p = AdventurePlayer(hashid = rgen, player_info = '')
    else:
        query = db.Query(AdventurePlayer)
        query.filter('hashid =', cookie)
        p = query.get()
        if p:
            s = str(p.player_info)

    content = self.request.get('content')

    out_str, new_player = adventure.receive(content, s)

    p.player_info = new_player
    p.put()
    self.response.out.write(out_str)

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
                               ('/ownhunts', OwnHuntsHandler),
                               ('/create_hunt', HuntCreateHandler),
                               ('/create_hunt/submit', HuntCreateSubmitHandler),
                               ('/hunts/([a-zA-Z0-9]+)', HuntHandler),
                               ('/hunts/([a-zA-Z0-9]+)/edit', HuntEditHandler),
                               ('/hunts/([a-zA-Z0-9]+)/edit_submit', HuntEditSubmitHandler),
                               ('/hunts/([a-zA-Z0-9]+)/set_mainpage/([a-zA-Z0-9]+)', HuntSetMainPageHandler),
                               ('/hunts/([a-zA-Z0-9]+)/puzzles/([a-zA-Z0-9]+)', HuntPuzzleHandler),
                               ('/hunts/([a-zA-Z0-9]+)/puzzles/([a-zA-Z0-9]+)/submit', HuntPuzzleSubmitAnswerHandler),
                               ('/hunts/([a-zA-Z0-9]+)/puzzles/([a-zA-Z0-9]+)/files/(.*)', HuntPuzzleFileHandler),
                ('/pquest', pquest.PoozleQuestHandler),
                ('/pquest/move', pquest.PoozleQuestMoveHandler),
                ('/pquest/action', pquest.PoozleQuestActionHandler),
		('/pquest/inventory', pquest.PoozleQuestInvHandler),
		('/pquest/inventory/action', pquest.PoozleQuestInvActionHandler),

         ('/adventure', AdventureHandler),
         ('/adventure/send', AdventureRealTimeHandler),
				],

                              debug=True)
