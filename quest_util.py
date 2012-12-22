# util functions for puzzles

from models import *

import user_util
import random

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
                        hp = unit_stats[s]['maxhp'],
                        mp = unit_stats[s]['maxmp'],
                        maxhp = unit_stats[s]['maxhp'],
                        maxmp = unit_stats[s]['maxmp'])

    n.put()
    return n.key().id()

def get_unit_by_id(uid):
    return PoozleQuestUnit.get_by_id(uid)

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
        if min_unit is None or unit.time_until_turn < min_unit.time_until_turn:
            min_unit = unit

    r = min_unit.time_until_turn

    PoozleQuestBattle.get_by_id(bid).turn_uid = min_unit.key().id()
    PoozleQuestBattle.get_by_id(bid).put()

    for q in query:
        unit = get_unit_by_id(q.uid)
        unit.time_until_turn -= r
        unit.put()

def apply_spell(source, target, spell):
    if spell == 'attack':
        target.hp -= source.atk
        if target.hp < 0:
            target.hp = 0

    target.put()
