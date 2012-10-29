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

from models import *

jinja_loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
jinja_env = jinja2.Environment(autoescape=True,
                               loader = jinja_loader)

class ImageHandler(webapp2.RequestHandler):
  def get(self):
    img_class = Image.get_by_id(int(self.request.get('id')))
    if img_class.img:
      self.response.headers['Content-Type'] = 'image/png'
      self.response.out.write(img_class.img)
    else:
      self.response.out.write('could not load image')

class PdfHandler(webapp2.RequestHandler):
  def get(self):
    if self.request.get('puzzle'):
	puzzle_class = puzzle_util.get_puzzle_by_code(self.request.get('puzzle'))
	pdf = puzzle_util.get_puzzle_pdf(puzzle_class.key().id())

	if pdf and pdf.pdf:
	    self.response.headers['Content-Type'] = 'application/pdf'
	    self.response.out.write(pdf.pdf)
	else:
	    self.response.out.write('no pdf')
    else:
	self.response.out.write('no pdf')
	
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
    puzzles = puzzle_util.get_puzzles()

    puzzles = filter(lambda k: user_util.user_can_view_puzzle(uid, k.key().id()), puzzles)

    completion = [puzzle_util.has_user_solved(uid, p.key().id()) for p in puzzles]
    self.render(puzzles, completion)

class PuzzleHandler(webapp2.RequestHandler):
  def render(self, user, puzzle, up_info, pdf):
    template = jinja_env.get_template('puzzle.html')
    self.response.out.write(template.render(user = user, 
                                            puzzle = puzzle, 
                                            up_info = up_info,
					    pdf = pdf,
                                            logged_in = True))

  def get(self, short_code):
    puzzle = puzzle_util.get_puzzle_by_code(short_code)
    uid = auth_util.auth_into_site(self)
    pid = puzzle.key().id()
    user = User.get_by_id(uid)

    up_info = puzzle_util.get_upinfo(uid, pid)
    pdf = puzzle_util.get_puzzle_pdf(pid)

    self.render(user, puzzle, up_info, pdf)

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
  def render(self, images):
    template = jinja_env.get_template('puzzle_submit.html')
    self.response.out.write(template.render(logged_in = 'True', images = images))

  def get(self):
    uid = auth_util.auth_into_site(self)
    images = list(db.Query(Image))
    self.render(images)

class PuzzleSubmitImageHandler(webapp2.RequestHandler):
  # handler for image submission
  def get(self):
    self.redirect('/puzzle_submit')

  def post(self):
    uid = auth_util.auth_into_site(self)
    if uid:
	image = self.request.get('img')
	db_image = Image(uid = uid,
			 img = db.Blob(image))

	db_image.put()
    
    self.redirect('/puzzle_submit')

class PuzzleSubmitHandler(webapp2.RequestHandler):
  def get(self):
    self.redirect('/puzzle_submit')

  def post(self):
    uid = auth_util.auth_into_site(self)
    if uid:
      title = self.request.get('title')
      text = self.request.get('text')
      answer = self.request.get('answer')
      ptype = self.request.get('ptype')


    if title != '' and text != '' and answer != '':
        puzzle = Puzzle(title = title,
        short_code = 'tmp' + str(int(random.random() * 100000000)), #change later
        answer = answer,
        text = text,
        author = uid,
        ptype = ptype,
        approved = user_util.is_admin(uid))

        puzzle.put()

        pdf = self.request.get('pdf')
        if pdf:
          db_pdf = Pdf(pid = puzzle.key().id(),
            pdf = db.Blob(pdf))

          db_pdf.put()

    self.redirect('/puzzles')
 
class PuzzleApproveHandler(webapp2.RequestHandler):
  def get(self, short_code):
    self.redirect('/puzzles/' + short_code)

  def post(self, short_code):
    uid = auth_util.auth_into_site(self)
    pid = puzzle_util.get_puzzle_by_code(short_code).key().id()

    puzzle_util.approve_puzzle(uid, pid)

    self.redirect('/puzzles/' + short_code)

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('(.*)/', TrailingHandler),
			       ('/img_uploads', ImageHandler),
			       ('/pdfs', PdfHandler),
                               ('/login', LoginHandler),
                               ('/register', RegisterHandler),
                               ('/logout', LogoutHandler),
                               ('/puzzles', PuzzlesHandler),
                               ('/puzzles/([a-zA-Z0-9]+)', PuzzleHandler),
			       ('/puzzles/([a-zA-Z0-9]+)/submit', PuzzleSubmitAnswerHandler),
			       ('/puzzles/([a-zA-Z0-9]+)/approve', PuzzleApproveHandler),
			       ('/puzzle_submit', PuzzleSubmitPageHandler),
			       ('/puzzle_submit/submit', PuzzleSubmitHandler),
			       ('/puzzle_submit/img_submit', PuzzleSubmitImageHandler),
				],

                              debug=True)
