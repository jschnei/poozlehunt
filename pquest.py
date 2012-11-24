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

import collections

from models import *
from pquest_tiles import *

jinja_loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
jinja_env = jinja2.Environment(autoescape=True,
                               loader = jinja_loader)

area_map = {}
area_map["noodle"] = "Noodle Village"
area_map["noodle2"] = "Noodle Peninsula"

solid_list = ["Ocean", "Mountain", "Rock"]

length_map = { }
length_map["noodle"] = (15, 15)

person_map = { }
person_map["p1"] = ["misc_man1", "Charlem", "talk"]

talk_choice_map = collections.defaultdict(dict)
talk_choice_map["p1"]["village"] = 'say: "What can you tell me about the village?"'
talk_choice_map["p1"]["area"] = 'say: "What can you tell me about the area?"'

talk_dialog_map = collections.defaultdict(dict)
talk_dialog_map["p1"][""] = "Hello, $NAME!  How are you?"
talk_dialog_map["p1"]["village"] = "Noodle Village has been a small farming village for over a century.  Many of us grow fruits and take them to market in Lynbrook, a city to the south."
talk_dialog_map["p1"]["area"] = "Well, for starters, we're in Noodle Village!  It's on the northern tip of the continent!  Also, it's surrounded by mountains on all sides, and a tunnel to the south is the only way to get in or out."

tag_map = collections.defaultdict(str)
tag_map["noodle"] = [["town", "noodle2", 11, 11]]

warp_map = { }
warp_map["w1"] = ["noodle", 5, 5]

def img_wrap(s, depth):
    return '<img src="resource/quest/' + s + '.png" class="pa" style="z-index: %s" />' % str(depth)

def js_wrap(s):
    return '<script type="text/javascript">' + s + '</script>'

def get_cells(src, x, y):
    cells = []
    for row in range(y - 5, y + 6):
        cells.append(tile_map[src][row][x-5:x+6])
    
    return cells

def gen_result_html(target, action, subaction):
    s = ''

    if target[0] == 'p':
        if action == 'talk':
            s += talk_dialog_map["p1"][subaction] + '<br><br>'
            for typ_talk in talk_choice_map[target]:
                if typ_talk != subaction and typ_talk != "":
                    s += '<a id="btn_%s_%s" href="javascript:;">%s</a>' % (target, typ_talk, talk_choice_map[target][typ_talk])
                    s += js_wrap('document.getElementById("btn_%s_%s").addEventListener("click", function() { action("%s", "talk", "%s"); });' % (target, typ_talk, target, typ_talk)) + '<br>'

    return s

def gen_table_html(cells):
    s = '<table width="440" border="0" cellpadding="0" cellspacing="0">'
    for y in range(11):
        s += '<tr>'
        for x in range(11):
            cell = cells[y][x]

            s += '<td><div class="pr">'
            s += img_wrap(cell[0], 0)
            
            depth = 1
            for other in cell[1:]:
                if other[0] == 'p':
                    s += img_wrap(person_map[other][0], depth)
                elif other[0] != 'w':
                    s += img_wrap(other, depth)

            if x == 5 and y == 5:
                s += img_wrap('player', 100)

            s += '</div></td>'

    s += '</tr>'
    s += '</table>'

    return s

def gen_action_html(cells):
    s = ''

    for y in [4, 5, 6]:
        for x in [4, 5, 6]:
            cell = cells[y][x]

            for other in cell[1:]:
                if other[0] == 'p': #denotes a person
                    s += '<a id="btn_%s" href="javascript:;">Talk to %s</a>' % (other, person_map[other][1])
                    s += js_wrap('document.getElementById("btn_%s").addEventListener("click", function() { action("%s", "talk", ""); });' % (other, other))
                    s += '<br>'

    return s
       
class PoozleQuestHandler(webapp2.RequestHandler):
  # this is distinct from puzzle quest which is an actual game

    def render(self, cells):
      template = jinja_env.get_template('quest.html')
      self.response.out.write(template.render(result = "", cells = gen_table_html(cells), actions = gen_action_html(cells), logged_in = 'True'))

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
        self.response.out.write('{"table":"' + gen_table_html(cells).replace('"', '\\"') + '", "action":"' + gen_action_html(cells).replace('"', '\\"') + '", "result":""}')

    def post(self):
        uid = auth_util.auth_into_site(self)

        dir_array = [ (0, 0), (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1) ]

        if uid:
            quest = quest_util.get_uqinfo(uid)
            move_dir = int(self.request.get('direction'))

            quest.xpos += dir_array[move_dir][0]
            quest.ypos += dir_array[move_dir][1]
            cells = get_cells(quest.mmap, quest.xpos, quest.ypos)

            cell = tile_map[quest.mmap][quest.ypos][quest.xpos]
            block = False

            for other in cell:
                if other[0] == 'w':
                    quest.mmap, quest.ypos, quest.xpos = warp_map[other]
                    cells = get_cells(quest.mmap, quest.xpos, quest.ypos)
                elif other[0] == 'p' or other in solid_list:
                    block = True

            if not block and (quest.xpos <= 4 or quest.ypos <= 4 or quest.ypos >= len(tile_map[quest.mmap])-6 or quest.xpos >= len(tile_map[quest.mmap][quest.ypos])-6):
                block = True
                for tag in tag_map[quest.mmap]:
                    if tag[0] == 'town':
                        block = False
                        quest.mmap, quest.ypos, quest.xpos = tag[1], tag[2], tag[3]
                        quest.xpos += dir_array[move_dir][0]
                        quest.ypos += dir_array[move_dir][1]

                        cells = get_cells(quest.mmap, quest.xpos, quest.ypos)
                
            if block:
                quest.xpos -= dir_array[move_dir][0]
                quest.ypos -= dir_array[move_dir][1]
                cells = get_cells(quest.mmap, quest.xpos, quest.ypos)

            quest.put()
            
            self.render(cells)

class PoozleQuestActionHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/pquest')

    def render(self, cells, target, action, subaction):
        result_html = ''
        if action != 'talk':
            result_html = gen_table_html(cells)

        self.response.out.write('{"table":"' + result_html.replace('"', '\\"') + '", "action":"' + gen_action_html(cells).replace('"', '\\"') + '", "result":"' + gen_result_html(target, action, subaction).replace('"', '\\"') + '"}')

    def post(self):
        uid = auth_util.auth_into_site(self)

        if uid:
            quest = quest_util.get_uqinfo(uid)
            target = self.request.get('target')
            action_type = self.request.get('type')
            action_subtype = self.request.get('subtype')
            found_person = False

            cells = get_cells(quest.mmap, quest.xpos, quest.ypos)

            for y in [4, 5, 6]:
                for x in [4, 5, 6]:
                    cell = cells[y][x]

                    for other in cell[1:]:
                        if other[0] == 'p' and other == target:
                            # person handler
                            found_person = True
                            self.render(cells, target, action_type, action_subtype)
        
        if not found_person:
            self.response.out.write("")
