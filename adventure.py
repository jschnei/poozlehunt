from adventure_util import *
from items import *

import collections

def receive(text, player):
    p1 = Player([])

    if text == '':
        return ''
    if player != '':
        p1 = player_unpickle(player)
    
    command = parse(text.lower())

    res = process(command, p1)
    
    return res, player_pickle(p1)

def process(command, p1):
    if 'maria' in command and 'grod' in p1.milestones and p1.current_room == 'fe':
        return 'Well done, adventurer! Your answer is HEXAMETERS! I hope you had fun on your journey.'

    if command[0] == 'climb' and ((p1.current_room == 'c' and p1.current_season != 'summer') or (p1.current_room == 'snow' and 'grope' in p1.milestones)):
        command = ['move'] + command
        
    if command[0] == 'help' or command[0] == '?':
        return help_text
    
    elif command[0] == 'inventory' or command[0] == 'items':
        return p1.items_text()
    
    elif command[0] == 'examine':
        if len(command) == 1:
            return gen_room_desc(room_map[p1.current_room], p1)
        else:
            action = touch_object(room_map[p1.current_room], command[1])
            if action:
                if isinstance(action, TakeAction) and p1.current_season in action.seasons:
                    return action.item.d['examine']
                elif isinstance(action, BasicResponseAction):
                    return action.d['examine'](p1)
            else:
                for i in p1.items:
                    if command[1] in i.names:
                        return i.d['examine']

            return 'I can\'t say I know what that is.'
        
    elif command[0] == 'talk':
        if len(command) == 1:
            return 'Who do you want to talk to?'
        elif p1.current_room == 'fe':
            action = touch_object(room_map[p1.current_room], command[1])
            if action and isinstance(action, BasicResponseAction):
                return action.d['talk'](p1)

        return 'I don\'t know who you mean.'

    elif command[0] == 'take':
        if len(command) == 1:
            return 'What do you want to take?'
        
        action = touch_object(room_map[p1.current_room], command[1])
        for a in room_map[p1.current_room].actions + global_actions:
            if isinstance(a, TakeAction) and p1.current_season in a.seasons:
                if command[1] in a.names:
                    ok = True
                    for r in a.reqs:
                        if r not in p1.milestones and r not in p1.temp_milestones:
                            ok = False
                            break

                    if ok:
                        if a.item.names[0] in p1.milestones:
                            return 'You don\'t need another one of these!'
                        
                        p1.set_milestone(a.item.names[0])
                        p1.items += [a.item]
                        return a.item.d['take']

        for a in room_map[p1.current_room].actions + global_actions:
            if isinstance(a, BasicResponseAction) and p1.current_season in a.seasons:
                if command[1] in a.names and 'take' in a.d:
                    return a.d['take'](p1)
                    
        return 'I can\'t say I know what that is.'

    elif command[0] == 'move':
        if len(command) == 1:
            return 'Where do you want to go today?'
        
        for a in room_map[p1.current_room].actions + global_actions:
            if isinstance(a, MoveAction):
                if command[1] in a.names:
                    if p1.current_season in a.seasons:
                        ok = True
                        for r in a.reqs:
                            if r not in p1.milestones and r not in p1.temp_milestones:
                                ok = False
                                break
                        
                        if ok:
                            p1.current_room = a.room
                            p1.clear_tmp_milestones()

                            return gen_room_desc(room_map[p1.current_room], p1)
                    
                    if a.fdesc != '':
                        return a.fdesc
                
        return 'You can\'t move that way.'
                        
    elif command[0] == 'use':
        if len(command) == 1:
            return 'What do you want to use?'
        
        ok = False
        iname = ''
            
        for r in p1.items:
            if command[1] in r.names:
                ok = True
                if 'use' in r.d:
                    iname = r.d['use']

        if len(command) <= 2:
            if not ok:
                return 'You don\'t have such a thing!'
            
            for a in room_map[p1.current_room].actions + global_actions:
                if isinstance(a, UseAction):
                    ok = True
                    
                    for r in a.reqs:
                        if r not in p1.milestones and r not in p1.temp_milestones:
                            ok = False
                            break

                    if ok and command[1] in a.names:
                        r = a.response(p1)
                        a.fn(p1)
                        return r

            if iname != '':
                return iname
                
            return 'You can\'t use that here.'

        else:
            rr = True
            
            if command[-1] in ['woman', 'lady'] and p1.current_room == 'fe':
                command[0] = 'give'
                rr = False

            if rr and food in p1.items and (command[1] in food.names or command[2] in food.names):
                rr = False

            if rr:
                for a in room_map[p1.current_room].actions + global_actions:
                    if isinstance(a, UseWithAction):
                        if (command[1] in a.names and command[2] in a.tnames) or (command[1] in a.tnames and command[2] in a.names):
                            r = a.response(p1)
                            a.fn(p1)
                            return r
                        
                return 'You can\'t use that like that.'
        
    if command[0] == 'give':
        if p1.current_room != 'fe':
            return 'There\'s nobody to give anything to!'
        
        if len(command) == 1:
            return 'What do you want to give?'

        desired_items = [rainrose, whiskers, kettle, mittens,
                         package, pony, apple, doorbell, sleighbell,
                         food, goose, doll, snowflake, rod]

        i = None
        has_item = None

        for item in desired_items:
            if command[1] in item.names:
                i = item
                break

        for item in p1.items:
            if command[1] in item.names and (i == None or not i.equals(has_item)):
                has_item = item
                break

        if not has_item:
            return 'You don\'t have such a thing.'

        elif i == None or not i.equals(has_item):
            return 'The woman says:<br>"Thank you for the thought, but that\'s not one of my favorite things. You can keep it."'
                    
        if i.equals(rod) and p1.count_given < 13:
            return 'The woman says:<br>"Ahh...my most favorite item of all. I will accept this from you, but not now. I have a feeling you\'ll need it."'
        elif i.equals(rod):
            p1.count_given += 1
            p1.set_milestone('g' + command[1])
            p1.items.remove(has_item)
            return 'The woman says:<br>"Your journey is done, adventurer! I can be on my way...but first, for your final task: have you figured out my name?'

        p1.set_milestone('g' + i.names[0])
        p1.items.remove(has_item)
        p1.count_given += 1

        return 'The woman says:<br>"Thank you so much! You don\'t know how much this means to me."'
    
    elif len(command) >= 2:
        for a in room_map[p1.current_room].actions + global_actions:
            if isinstance(a, SimpleToggleAction) and command[1] in a.names:
                key = a.names[0]
                if key in p1.temp_milestones and command[0] in a.unprefixes:
                    del p1.temp_milestones[key]
                    return a.unresponse(p1)

                elif key not in p1.temp_milestones and command[0] in a.prefixes:
                    p1.temp_milestones[key] = 0
                    return a.response(p1)
                
        for a in room_map[p1.current_room].actions:
            if isinstance(a, BasicResponseAction) and command[1] in a.names and command[0] in a.d:
                return a.d[command[0]](p1)

    if p1.current_room == 'fe' and 'grod' in p1.milestones:
        return '"That\'s not my name," says the woman.'
    
    return 'I\'m sorry, I don\'t understand...'

