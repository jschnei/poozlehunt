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
                        maxmp = unit_stats[s]['maxmp'],
			level = unit_stats[s]['level'])

    n.put()
    return n.key().id()

def get_unit_by_id(uid):
    return PoozleQuestUnit.get_by_id(uid)

def get_units_of_type(bid, player_units = True):
    query = db.Query(PoozleQuestUnitBattle)
    query.filter('bid =', bid)
    query.order('uid')

    return [u.uid for u in query if get_unit_by_id(u.uid).is_player == player_units]

def get_player_units(qid):
    return [q.uid for q in db.Query(PoozleQuestPCData).filter('qid =', qid).order('uid')]

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

# battle-specific functions ... should probably move later

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
    msg = ''
    dmg = 0
    source_name = source.name if source.is_player else 'the ' + source.name
    target_name = target.name if target.is_player else 'the ' + target.name

    if spell == 'attack':
	dmg = source.atk
	msg = source_name + ' slashes ' + target_name + ' for <b>%d</b> damage!<br>'

    elif spell == 'rend':
	dmg = source.atk
	apply_buff(source.key().id(), target.key().id(), spell, 'rend', 3)
	msg = source_name + ' rends ' + target_name + ' for <b>%d</b> damage!<br>'

    elif spell == 'charge':
	msg = source_name + ' charges, readying for a powerful attack!'
	apply_buff(source.key().id(), source.key().id(), spell, 'charge', 2)
    
    source_dmg = dmg
    
    for b in get_buffs(source.key().id()):
	buff = get_buff_by_id(b)
	if dmg > 0 and 'attack' in buff_stats[buff.buffid]:
	    msg += buff_effect(b, 'attack', [source, target, dmg])

    dmg += target.dmg_buffer
    target.dmg_buffer = 0.
    target.hp -= int(dmg)

    if dmg > 0:
	msg = msg % dmg
    if target.hp < 0:
	target.hp = 0

    target.put()

    return msg

def delete_battle(bid):
    PoozleQuestBattle.get_by_id(bid).delete()

    q = db.Query(PoozleQuestUnitBattle)
    q.filter('bid =', bid)

    for u in q:
	uid = u.uid
	if not get_unit_by_id(uid).is_player:
	    get_unit_by_id(uid).delete()

	u.delete()

# buff utility functions

def get_buff_by_id(buffid):
    return PoozleQuestBuffData.get_by_id(buffid)

def buff_information(uid, sid, buffid):
    u = get_unit_by_id(uid)

    query = db.Query(PoozleQuestSpellData)
    query.filter('uid =', uid)
    query.filter('sid =', sid)
    spell = query.get()

    if buffid == 'rend':
	return [int(u.level / (5 - spell.level) / 3 + 1)]
    if buffid == 'charge':
	return [30 * spell.level]

def apply_buff(uid, tid, sid, buffid, duration):
    # applying buffid from uid -> tid with spell sid

    buff = PoozleQuestBuffData(uid = tid, buffid = buffid, duration = duration)
    buff_info = buff_information(uid, sid, buffid)
    
    # hack
    if len(buff_info) > 0:
	buff.info0 = buff_info[0]
    if len(buff_info) > 1:
	buff.info1 = buff_info[1]
    if len(buff_info) > 2:
	buff.info2 = buff_info[2]
    if len(buff_info) > 3:
	buff.info3 = buff_info[3]

    buff.put()

def buff_effect(buffid, type, params):
    msg = ''
    unit, target, tdamage = params

    buff = get_buff_by_id(buffid)
    for key in buff_stats[buff.buffid][type]:
	if key == 'damage':
	    dmg = buff_stats[buff.buffid][type][key](buff)
	    unit.hp -= dmg
	    if unit.hp < 0:
		unit.hp = 0
	    msg += '%s causes %d damage!<br>' % (buff.buffid, dmg)
	    unit.put()

	if key == 'tdamage':
	    dmg = buff_stats[buff.buffid][type][key](buff, tdamage)
	    target.dmg_buffer += dmg
	    if target.hp < 0:
		target.hp = 0
	    target.put()

    return msg

def get_buffs(uid):
    query = db.Query(PoozleQuestBuffData)
    query.filter('uid =', uid)
    return [q.key().id() for q in query]

# spell utility functions

def get_spell_by_id(sid):
    return PoozleQuestSpellData.get_by_id(sid)

def get_spells(uid):
    query = db.Query(PoozleQuestSpellData)
    query.filter('uid =', uid)
    return [q.key().id() for q in query]

def wrap_spell_description(str, uid, sid):
    u = get_unit_by_id(uid)
    params = []

    if sid == 'rend':
	params = [int(u.level / (5 - sid.level) / 3 + 1)]
	

# loot-specific functions

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

# inventory-related item functions

def get_items(qid):
    query = db.Query(PoozleQuestItem)
    query.filter('qid =', qid)
    r = [q.key().id() for q in query]
    r.sort()
    return r

def get_attributes(itemid):
    query = db.Query(PoozleQuestItemAttribute)
    query.filter('itemid =', itemid)
    return [q.key().id() for q in query]

def create_item_rough(qid, name, tag, attributes = []):
    item = PoozleQuestItem(qid = qid, name = name, tag = tag)
    item.put()
    for a in attributes:
	att = PoozleQuestItemAttribute(	itemid = item.key().id(),
					type = a[0], subtype = a[1] if len(a) >= 2 else '',
					info0 = a[2] if len(a) >= 3 else 0,
					info1 = a[3] if len(a) >= 4 else 0,
					info2 = a[4] if len(a) >= 5 else 0,
					info3 = a[5] if len(a) >= 6 else 0 )
	att.put()

    return item.key().id()

def unequip_item(i):
    item = PoozleQuestItem.get_by_id(i)
    uid = item.equip_id

    for a in get_attributes(i):
	deapply_attribute(uid, a)

    item.equip_id = 0
    item.put()

def equip_item(uid, i):
    item = PoozleQuestItem.get_by_id(i)
    if item.equip_id != 0:
	unequip_item(i)

    item.equip_id = uid

    for a in get_attributes(i):
	apply_attribute(uid, a)

    item.put()

def get_equipped_items(uid):
    query = db.Query(PoozleQuestItem)
    query.filter('equip_id =', uid)
    return [q.key().id() for q in query]

def apply_attribute(uid, aid):
    unit = get_unit_by_id(uid)
    attr = PoozleQuestItemAttribute.get_by_id(aid)
    type = attr.type

    if type == 'atk':
	unit.atk += attr.info0
    elif type == 'pdef':
	unit.pdef += attr.info0
    elif type == 'mag':
	unit.mag += attr.info0
    elif type == 'mdef':
	unit.mdef += attr.info0
    elif type == 'spd':
	unit.spd += attr.info0
    elif type == 'mspd':
	unit.mspd += attr.info0
    elif type == 'hp':
	unit.maxhp += attr.info0
    elif type == 'mp':
	unit.maxmp += attr.info0

    unit.put()

def deapply_attribute(uid, aid):
    unit = get_unit_by_id(uid)
    attr = PoozleQuestItemAttribute.get_by_id(aid)
    type = attr.type

    if type == 'atk':
	unit.atk -= attr.info0
    elif type == 'pdef':
	unit.pdef -= attr.info0
    elif type == 'mag':
	unit.mag -= attr.info0
    elif type == 'mdef':
	unit.mdef -= attr.info0
    elif type == 'spd':
	unit.spd -= attr.info0
    elif type == 'mspd':
	unit.mspd -= attr.info0
    elif type == 'hp':
	unit.maxhp -= attr.info0
    elif type == 'mp':
	unit.maxmp -= attr.info0
    
    unit.put()

########## item generation code

def generate_item(qid, itemid, params = []):
    basic_buffs = ['atk', 'pdef', 'mag', 'mdef', 'hp', 'mp']

    item = PoozleQuestItem(qid = qid, name = itemid)
    item.put()

    if 'equip' not in item_info[id]:
	return item.key().id()

    att = PoozleQuestItemAttribute(itemid = item.key().id(),
