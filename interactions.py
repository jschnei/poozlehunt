from adventure_util import *
from items import *

def knock_cat(p):
    p.set_milestone('catknock')
    room_map[p.current_room].actions.insert(TakeAction(whiskers, ''))
    
def knock_goose(p):
    p.set_milestone('gooseknock')
    room_map[p.current_room].actions.insert(TakeAction(goose, ''))
    
def drench_rose(p):
    p.set_milestone('rainrose')
    p.items += [rainrose]
    p.items.remove(rose)
