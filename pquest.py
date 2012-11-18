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
import quest_util

from models import *

jinja_loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
jinja_env = jinja2.Environment(autoescape=True,
                               loader = jinja_loader)

tile_map = { }
tile_map["noodle"] = [["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Dirt"],["Grass"],["Dirt"],["Dirt"],["Dirt"]]

length_map = { }
length_map["noodle"] = (15, 15)

def get_cells(src, x, y):
    cells = []
    for row in range(y - 5, y + 6):
        for col in range(x - 5, x + 6):
            cells.append(tile_map[src][row * length_map[src][1] + col])

    return cells

def gen_table_html(cells):
    s = '<table width="440" border="0" cellpadding="0" cellspacing="0">'
    for r in range(121):
        cell = cells[r]

        x = r % 11
        y  = int(r / 11)
        if x == 0:
            s += '<tr>'

        s += '<td><div class="pr">'
        s += '<img src="resource/quest/' + cell[0] + '.png" class="z0" />'
        if x == 5 and y == 5:
            s += '<img src="resource/quest/player.png" class="pa" style="z-index: 100" />'
        s += '</div></td>'
        s += '\n'

    s += '</tr>'
    s += '</table>'

    return s
       
class PoozleQuestHandler(webapp2.RequestHandler):
  # this is distinct from puzzle quest which is an actual game

    def render(self, cells):
      template = jinja_env.get_template('quest.html')
      self.response.out.write(template.render(cells = gen_table_html(cells), logged_in = 'True'))

    
        
    def get(self):
        uid = auth_util.auth_into_site(self)

        if uid is None:
            self.redirect('/')
        
        quest = quest_util.get_uqinfo(uid)

        cells = get_cells(quest.mmap, quest.xpos, quest.ypos)

        self.render(cells)

class PoozleQuestMoveHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/pquest')

    def render(self, cells):
        template = jinja_env.get_template('quest.html')
        self.response.out.write(gen_table_html(cells))

    def post(self):
        uid = auth_util.auth_into_site(self)

        dir_array = [ (0, 0), (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1) ]

        if uid:
            quest = quest_util.get_uqinfo(uid)
            move_dir = int(self.request.get('direction'))

            quest.xpos += dir_array[move_dir][0]
            quest.ypos += dir_array[move_dir][1]

            quest.put()
            
            cells = get_cells(quest.mmap, quest.xpos, quest.ypos)
            self.render(cells)
