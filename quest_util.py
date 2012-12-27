# util functions for puzzles

from models import *

import user_util
import random
import collections
import sys

from pquest_tiles import *

def get_uqinfo(uid, create_if_none=True):
  query = db.Query(PoozleQuest)
  query.filter('uid =', uid)
  
  ret = query.get()
  if create_if_none and ret is None:
      ret = PoozleQuest(uid = uid,
                        mmap = "noodle",
                        xpos = 7,
                        ypos = 7,
                        in_battle=False)

      player_unit = PoozleQuestUnit(name = 'player_fight',
				    atk = 11, pdef = 3, mag = 7, mdef = 3, spd = 2.8, mspd = 4.0, hp = 35, mp = 7, maxhp = 35, maxmp = 7, is_player = True)
      
      ret.put() 
      player_unit.put()

      unit_data = PoozleQuestPCData(qid = ret.key().id(), uid = player_unit.key().id(), in_party = True)
      unit_data.put()

  return ret

def get_ubinfo(uid, create_if_none=True):
    query = db.Query(PoozleQuest)
    query.filter('uid =', uid)
    user = query.get()
    bid = user.battle_id

    ret = PoozleQuestBattle.get_by_id(bid)

    if create_if_none and ret is None:
        ret = PoozleQuestBattle()
        user.battle_id = ret.key().id()
        user.put()

    return ret

def create_unit(s):
    n = PoozleQuestUnit(name = s,
                        atk = unit_stats[s]['atk'],
                        pdef = unit_stats[s]['pdef'],
                        mag = unit_stats[s]['mag'],
                        mdef = unit_stats[s]['mdef'],
                        spd = unit_stats[s]['spd'],
			mspd = unit_stats[s]['mspd'],
                        hp = unit_stats[s]['maxhp'],
                        mp = unit_stats[s]['maxmp'],
                        maxhp = unit_stats[s]['maxhp'],
                        maxmp = unit_stats[s]['maxmp'])

    n.put()
    return n.key().id()

def get_unit_by_id(uid):
    return PoozleQuestUnit.get_by_id(uid)

def get_units_of_type(bid, player_units = True):
    query = db.Query(PoozleQuestUnitBattle)
    query.filter('bid =', bid)
    query.order('uid')

    return [u.uid for u in query if get_unit_by_id(u.uid).is_player == player_units]

def add_player_units_to_battle(qid, bid):
    query = db.Query(PoozleQuestPCData)
    query.filter('qid =', qid)

    for q in query:
	ub_link = PoozleQuestUnitBattle(uid = q.uid,
					bid = bid)
	ub_link.put()

def add_unit_to_battle(uid, bid):
    ub_link = PoozleQuestUnitBattle(uid = uid,
                                    bid = bid)
    ub_link.put()

def select_unit(area):
    den = 1.0
    for unit in enemy_map[area]:
        if random.random() <= (unit[0] / den):
            return unit[1]

        den -= unit[0]

    return ''

def create_units_for_battle(area, bid):
    unit = create_unit(select_unit(area))
    add_unit_to_battle(unit, bid)

    for add in prob_map[area]:
        if random.random() >= add:
            break

        unit = create_unit(select_unit(area))
        add_unit_to_battle(unit, bid)

# battle-specific spells ... should probably move later

def current_turn(bid):
    # return uid whose turn it is
    query = db.Query(PoozleQuestUnitBattle)
    query.filter('bid =', bid)

    min_unit = None
    for q in query:
        unit = get_unit_by_id(q.uid)
        if min_unit is None or unit.time_until_turn < min_unit.time_until_turn:
            min_unit = unit

    return min_unit.key().id()

def advance_turn(bid):
    query = db.Query(PoozleQuestUnitBattle)
    query.filter('bid =', bid)
    
    min_unit = None
    for q in query:
        unit = get_unit_by_id(q.uid)
        if (min_unit is None or unit.time_until_turn < min_unit.time_until_turn) and unit.hp > 0:
            min_unit = unit

    r = min_unit.time_until_turn

    PoozleQuestBattle.get_by_id(bid).turn_uid = min_unit.key().id()
    PoozleQuestBattle.get_by_id(bid).put()

    for q in query:
        unit = get_unit_by_id(q.uid)
	if unit.hp > 0:
	    unit.time_until_turn -= r
        unit.put()

def initialize_turns(bid):
    for u in get_units_of_type(bid, True) + get_units_of_type(bid, False):
	unit = get_unit_by_id(u)
	unit.time_until_turn = unit.spd

	unit.put()

    advance_turn(bid)

def apply_spell(source, target, spell):
    if spell == 'attack':
        target.hp -= source.atk
        if target.hp < 0:
            target.hp = 0

    target.put()

def delete_battle(bid):
    PoozleQuestBattle.get_by_id(bid).delete()

    q = db.Query(PoozleQuestUnitBattle)
    q.filter('bid =', bid)

    for u in q:
	uid = u.uid
	if not get_unit_by_id(uid).is_player:
	    get_unit_by_id(uid).delete()

	u.delete()

# loot-specific spells

def select_items(enemies):
    return collections.Counter([item for enemy in enemies for item in select_item(enemy)]).items()

def select_item(enemy):
    arr = []

    for u in defeat_stats[enemy]['spoils']:
        if random.random() <= u[0]:
            arr += [select_item_by_name(u[1])]

    return arr

def select_item_by_name(item):
    # shouldn't be called directly

    if item in spoil_groups:
	den = 1.0
	for n in spoil_groups[item]:
	    if random.random() <= (n[0] / den):
		return select_item_by_name(n[1])
	    den -= n[0]

    return item
