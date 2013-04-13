import collections
import re
import pickle

class Item:
    def __init__(self, names, d):
        self.names = names
        self.d = d

    def equals(self, i):
        if i == None:
            return False
        return self.names[0] == i.names[0]
        
class Player:
    def __init__(self, items = []):
        self.items = items
        self.milestones = { }
        self.temp_milestones = { }
        self.current_room = 'start'
        self.current_season = 'winter'
        self.count_given = 0

    def items_text(self):
        if len(self.items) == 0:
            return 'Inventory:<br>(nothing right now!)'
        
        return 'Inventory:<br>' + '<br>'.join(['  -' + k.names[0] for k in self.items])

    def change_season(self):
        self.current_season = seasonal(['summer', 'autumn', 'winter', 'spring'])(self.current_season)

    def set_milestone(self, m):
        self.milestones[m] = 0
        
    def set_tmp_milestone(self, m):
        self.temp_milestones[m] = 0
        
    def clear_tmp_milestones(self):
        self.temp_milestones = { }

    def generate_given(self):
        given_items = [k for k in ['drenched rose', 'whiskers', 'kettle', 'mittens',
                         'suspicious package', 'pony', 'apple strudel', 'doorbell', 'sleigh bell',
                         'schnitzel with noodles', 'goose', 'girl doll', 'snowflake', 'rod'] if 'g' + k in self.milestones]

        s = '<br>'.join(['-' + k for k in given_items])
        return '<br><b>Items returned so far:</b><br>' + s if s != '' else ''
        
        
class Room:
    def __init__(self, desc, actions):
        self.desc = desc
        self.actions = actions
    
class Action:
    def __init__(self, desc, names, seasons):
        self.desc = desc
        self.names = names
        self.seasons = seasons

class BasicResponseAction(Action):
    def __init__(self, names, d):
        self.d = d
        Action.__init__(self, '', names, ['spring', 'summer', 'autumn', 'winter'])
    
class TakeAction(Action):
    def __init__(self, item, desc, seasons = ['spring', 'summer', 'autumn', 'winter'], reqs = [], fdesc = ''):
        self.item = item
        self.reqs = reqs
        Action.__init__(self, desc, item.names, seasons)
        
class MoveAction(Action):
    def __init__(self, names, room, seasons = ['spring', 'summer', 'autumn', 'winter'], reqs = [], fdesc = ''):
        self.room = room
        self.fdesc = fdesc
        self.reqs = reqs
        Action.__init__(self, '', names, seasons)
        
class UseAction(Action):
    def __init__(self, names, fn, response, reqs = []):
        self.fn = fn
        self.response = response
        self.reqs = reqs
        Action.__init__(self, '', names, ['spring', 'summer', 'autumn', 'winter'])

class UseWithAction(Action):
    def __init__(self, names, tnames, fn, response, seasons = ['spring', 'summer', 'autumn', 'winter']):
        self.fn = fn
        self.tnames = tnames
        self.response = response
        Action.__init__(self, '', names, seasons)

class SimpleToggleAction(Action):
    def __init__(self, prefixes, unprefixes, names, r1, r2, seasons = ['spring', 'summer', 'autumn', 'winter']):
        self.prefixes = prefixes
        self.unprefixes = unprefixes # to undo the toggle
        self.response = r1
        self.unresponse = r2
        Action.__init__(self, '', names, seasons)

def parse(s):
    arr = [k for k in s.split(' ') if k != '']
    simple_remap = {'get': 'take', 'look': 'examine', 'north': 'up', 'east': 'right',
                    'west': 'left', 'south': 'down', 'go': 'move'}

    for k in range(len(arr)):
        if arr[k] in simple_remap:
            arr[k] = simple_remap[arr[k]]

    if len(arr) == 3 and arr[1] == 'on' and (arr[2] == 'stump' or arr[2] == 'roof'):
        arr = [arr[0], arr[2]]
        
    if arr[0] == 'play' and arr[1] == 'ocarina':
        arr[0] = 'use'
    if arr[0] == 'swing' and arr[1] == 'rod':
        arr[0] = 'use'
    if arr[0] == 'read' and (arr[1] == 'sign' or arr[1] == 'paper' or arr[1] == 'note'):
        arr[0] = 'examine'
    if arr[0] == 'move' and arr[1] == 'roof':
        arr[0] = 'climb'
            
    if arr[0] == 'up' or arr[0] == 'down' or arr[0] == 'left' or arr[0] == 'right' or arr[0] == 'out' or arr[0] == 'in':
        arr = ['move'] + arr
    if (arr[0] == 'use' or arr[0] == 'combine') and len(arr) > 2 and 'with' in arr:
        if arr[0] == 'combine':
            arr[0] = 'use'
        ind = 0
        for i in range(len(arr)):
            if arr[i] == 'with':
                ind = i
        arr = [arr[0], ' '.join(arr[1:ind]), ' '.join(arr[ind+1:])]
    elif arr[0] == 'use':
        arr = [arr[0], ' '.join(arr[1:])]

    if (arr[0] == 'examine' or arr[0] == 'take' or arr[0] == 'give') and len(arr) >= 2:
        arr = [arr[0], ' '.join(arr[1:])]

    return arr

def gen_room_desc(r, p):
    s = r.desc(p)
    has_actions = False
    for a in r.actions:
        if a.desc != '':
            if a.names[0] not in p.milestones:
                if not has_actions:
                    s += '<br>'
                    has_actions = True
                s += '<br>' + a.desc
            
    return s

def touch_object(room, key):
    for a in room.actions:
        if isinstance(a, Action):
            if key in a.names:
                return a
            
    return None

def seasonal(a):
    def f(s):
        if s == 'spring':
            return a[0]
        if s == 'summer':
            return a[1]
        if s == 'autumn':
            return a[2]
        return a[3]
    return f

def player_pickle(p):
    return pickle.dumps(p)

def player_unpickle(s):
    return pickle.loads(s)
