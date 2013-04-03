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

def img_wrap(s, depth=0):
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

def debug(s):
    print >> sys.stderr, str(s)

def gen_main_html(uid, cells, extra = { }):
    quest = quest_util.get_uqinfo(uid)

    if quest.in_battle:
        return gen_combat_html(uid, extra)

    return gen_table_html(cells, extra)

def gen_combat_html(uid, extra = { }):
    s = ''

    quest = quest_util.get_uqinfo(uid)
    bid = quest.battle_id

    p = [quest_util.get_unit_by_id(q) for q in quest_util.get_units_of_type(bid, True)]
    e = [quest_util.get_unit_by_id(q) for q in quest_util.get_units_of_type(bid, False)]
    target = int(extra['target']) if 'target' in extra else 0
    spells = []

    move = 'end'
    in_progress = (min(max([k.hp for k in p]), max([k.hp for k in e])) > 0)
    if in_progress:
        u = quest_util.get_unit_by_id(quest_util.current_turn(bid))
	move = 'player' if u.is_player else 'enemy'
	
	if u.is_player:
	    spells = [quest_util.get_spell_by_id(k) for k in quest_util.get_spells(u.key().id())]
	    spells = [(k, spell_stats[k.sid]) for k in spells]

    if quest.in_transition:
	return quest.transition_text

    p = [(k, [(quest_util.get_buff_by_id(r), buff_stats[quest_util.get_buff_by_id(r).buffid]['desc']) for r in quest_util.get_buffs(k.key().id())]) for k in p]
    e = [(k, [(quest_util.get_buff_by_id(r), buff_stats[quest_util.get_buff_by_id(r).buffid]['desc']) for r in quest_util.get_buffs(k.key().id())]) for k in e]

    template = jinja_env.get_template('battle.html')
    return template.render(player_units = p, enemy_units = e, move = move, spells = spells, target = target, message = PoozleQuestBattle.get_by_id(bid).message).replace('\t', '').replace('\n', '')

def gen_table_html(cells, extra = { }):
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

    def render(self, uid, cells):
      template = jinja_env.get_template('quest.html')
      self.response.out.write(template.render(result = "", cells = gen_main_html(uid, cells), actions = gen_action_html(cells), logged_in = 'True'))

    def get(self):
        uid = auth_util.auth_into_site(self)

        if uid is None:
            self.redirect('/')
        
        quest = quest_util.get_uqinfo(uid)

        cells = get_cells(quest.mmap, quest.xpos, quest.ypos)

        self.render(uid, cells)

class PoozleQuestMoveHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/pquest')

    def render(self, uid, cells, in_battle = False):
        template = jinja_env.get_template('quest.html')
        to_write = { }
        to_write['table'] = gen_main_html(uid, cells).replace('"', '\\"')
        to_write['action'] = gen_action_html(cells).replace('"', '\\"')
        to_write['result'] = ''
        to_write['nav'] = '' if in_battle == False else 'hide'

        out_str = '{' + ','.join(['"' + k + '":"' + to_write[k] + '"' for k in to_write]) + '}'
        self.response.out.write(out_str)

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

            else:
                # combat!
                if quest.mmap in prob_encounter and random.random() <= prob_encounter[quest.mmap]:
                    pqb = PoozleQuestBattle()
                    pqb.put()

                    quest_util.create_units_for_battle(quest.mmap, pqb.key().id())
		    quest_util.add_player_units_to_battle(quest.key().id(), pqb.key().id())

                    quest.in_battle = True
                    quest.battle_id = pqb.key().id()
		    
		    quest_util.initialize_turns(quest.battle_id)

            quest.put()
            
            self.render(uid, cells, quest.in_battle)

class PoozleQuestActionHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/pquest')

    def render(self, uid, cells, target, action, subaction, extra = { }):
        result_html = ''
        if action != 'talk':
            result_html = gen_main_html(uid, cells, extra)

        to_write = { }
	to_write['table'] = result_html.replace('"', '\\"')
	to_write['action'] = gen_action_html(cells).replace('"', '\\"')
	for item in extra:
	    to_write[item] = extra[item]

	if action != '' and subaction != '':
	    to_write['result'] = gen_result_html(target, action, subaction).replace('"', '\\"')

        out_str = '{' + ','.join(['"' + k + '":"' + to_write[k] + '"' for k in to_write]) + '}'
        self.response.out.write(out_str)
    
    def action(self, uid):
        target = self.request.get('target')
        action_type = self.request.get('type')
        action_subtype = self.request.get('subtype')
        found_person = False

	quest = quest_util.get_uqinfo(uid)

        cells = get_cells(quest.mmap, quest.xpos, quest.ypos)

        for y in [4, 5, 6]:
            for x in [4, 5, 6]:
                cell = cells[y][x]

                for other in cell[1:]:
                    if other[0] == 'p' and other == target:
                        # person handler
                        found_person = True
                        self.render(uid, cells, target, action_type, action_subtype)
        
        if not found_person:
            self.response.out.write("")

    def battle_action(self, uid):
	quest = quest_util.get_uqinfo(uid)

        cells = get_cells(quest.mmap, quest.xpos, quest.ypos)

        target = self.request.get('target')
        action = self.request.get('type')
        
        quest = quest_util.get_uqinfo(uid)
        bid = quest.battle_id

        u = quest_util.get_unit_by_id(quest_util.current_turn(bid))

        query = db.Query(PoozleQuestUnitBattle)
        query.filter('bid =', bid)
        query.order('uid')
	
        p = [quest_util.get_unit_by_id(q) for q in quest_util.get_units_of_type(bid, True)]
	e = [quest_util.get_unit_by_id(q) for q in quest_util.get_units_of_type(bid, False)]

	target = int(target)
	in_progress = (min(max([k.hp for k in p]), max([k.hp for k in e])) > 0)

	if in_progress:
	    msg = ''
	    if u.is_player and action != "next":
		if e[target].hp == 0:
		    target = filter(lambda k: k[1].hp > 0, enumerate(e))
		    target = target[0][0] if target else 0

		msg += quest_util.apply_spell(u, e[target], action)

	    elif not u.is_player and action == "next":
		action = 'attack'
		enemy_target = 0
		msg += quest_util.apply_spell(u, p[enemy_target], action)
	    
	    apply_id = u.key().id()
	    for b in quest_util.get_buffs(apply_id):
		buff = quest_util.get_buff_by_id(b)
		if 'turn' in buff_stats[buff.buffid]:
		    msg += quest_util.buff_effect(b, 'turn', [u, None, 0])

		buff.duration -= 1
		if buff.duration == 0:
		    buff.delete()
		else:
		    buff.put()

	    if action == 'attack':
		u.time_until_turn += u.spd
	    else:
		u.time_until_turn += u.mspd

	    u.put()
	    
	    pqb = PoozleQuestBattle.get_by_id(bid)
	    pqb.message = msg
	    pqb.put()

	    if u.is_player and e[target].hp == 0:
		target = filter(lambda k: k[1].hp > 0, enumerate(e))
		target = target[0][0] if target else 0

	    cells = get_cells(quest.mmap, quest.xpos, quest.ypos)
	    quest_util.advance_turn(bid)
	    self.render(uid, cells, '', '', '', extra = {'target' : str(target)})

	else:
	    to_write = { }
	    if not quest.in_transition and not in_progress and action == 'end':
		items = quest_util.select_items([n.name for n in e])
		for item in items:
		    for r in range(item[1]):
			quest_util.generate_item(quest.key().id(), item[0])
			print >> sys.stderr, str(item[0]) + '~~~'

		items = [(item_info[k[0]]['name'], k[1]) for k in items]
		template = jinja_env.get_template('battle_win.html')

		quest.transition_text = template.render(xp = 14, gold = 10, items = items).replace('\t', '').replace('\n', '')
		to_write['table'] = quest.transition_text.replace('"', '\\"')

		quest.in_transition = True

		quest.put()

	    elif quest.in_transition and action == 'map_return':
		quest.in_battle = False
		quest.in_transition = False
		quest.transition_text = ''

		quest_util.delete_battle(bid)
		
		quest.put()

		template = jinja_env.get_template('quest.html')

		to_write['table'] = gen_main_html(uid, cells).replace('"', '\\"')

	    out_str = '{' + ','.join(['"' + k + '":"' + to_write[k] + '"' for k in to_write]) + '}'
	    self.response.out.write(out_str)

    def post(self):
        uid = auth_util.auth_into_site(self)

        if uid:
            quest = quest_util.get_uqinfo(uid)
            if quest.in_battle:
                self.battle_action(uid)
            else:
                self.action(uid)

class PoozleQuestInvHandler(webapp2.RequestHandler):
    def render(self, units, items):
	template = jinja_env.get_template('inventory_disp.html')
	info_template = jinja_env.get_template('info.html')
	info = info_template.render(units = units, items = items)

	self.response.out.write(template.render(info = info))

    def get(self):
	uid = auth_util.auth_into_site(self)

	if uid is None:
	    self.redirect('/')

	quest = quest_util.get_uqinfo(uid)

	#if quest.in_battle:
	if False:
	    self.redirect('/pquest')
	else:
	    units = [i for i in quest_util.get_player_units(quest.key().id())]
	    units = [(quest_util.get_unit_by_id(u), [PoozleQuestItem.get_by_id(k) for k in quest_util.get_equipped_items(u)]) for u in units]
	    self.render(units = units,
			items = [PoozleQuestItem.get_by_id(i) for i in quest_util.get_items(quest.key().id())])

class PoozleQuestInvActionHandler(webapp2.RequestHandler):
    def render(self, units, items):
	template = jinja_env.get_template('inventory_disp.html')
	info_template = jinja_env.get_template('info.html')

	to_write = { }
	to_write['info'] = info_template.render(units = units, items = items).replace('\t', '').replace('\n', '').replace('"', '\\"')

	out_str = '{' + ','.join(['"' + k + '":"' + to_write[k] + '"' for k in to_write]) + '}'
	self.response.write(out_str)
	
    def get(self):
	self.redirect('/pquest/inventory')

    def post(self):
	uid = auth_util.auth_into_site(self)
	if uid:
	    qid = quest_util.get_uqinfo(uid).key().id()

	    type = self.request.get('type')
	    uid = int(self.request.get('uid'))
	    itemid = int(self.request.get('itemid'))
	    if type == 'equip':
		uid = quest_util.get_player_units(qid)[uid]
		itemid = quest_util.get_items(qid)[itemid]
		quest_util.equip_item(uid, itemid)
	    elif type == 'unequip':
		uid = quest_util.get_player_units(qid)[uid]
		itemid = quest_util.get_equipped_items(uid)[itemid]
		quest_util.unequip_item(itemid)
	    
	    units = [i for i in quest_util.get_player_units(qid)]
	    units = [(quest_util.get_unit_by_id(u), [PoozleQuestItem.get_by_id(k) for k in quest_util.get_equipped_items(u)]) for u in units]
	    self.render(units = units,
			items = [PoozleQuestItem.get_by_id(i) for i in quest_util.get_items(qid)])
