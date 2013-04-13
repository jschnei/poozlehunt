from adventure_util import *

import collections

# item data

rod = Item(['rod'], {'examine': 'A mysterious rod. You wonder what legendary powers lie within.',
                     'take': 'You take the rod. It is light and warm to the touch.',
                     'use': 'You swing your rod, but nothing happens.',})
sword = Item(['sword', 'blade'], {'examine': 'The blade of evil\'s bane.',
                              'take': 'You take the sword. Suddenly you feel like an adult.',})
doorbell = Item(['doorbell', 'door bell'], {'examine': 'A standard doorbell.',
                              'take': 'You pocket the doorbell. Somehow.',})
sleighbell = Item(['sleigh bell', 'sleigh bells', 'bell'], {'examine': 'A standard sleigh bell.',
                              'take': 'You pocket a sleigh bell. Festive!',})
snowflake = Item(['snowflake', 'snow'], {'examine': 'Unique, just like every other.',
                              'take': 'You catch a snowflake. Careful not to let it melt!',})
whiskers = Item(['whiskers'], {'examine': 'Whiskers from a cat.',
                              'take': 'You pull some of the cat\'s whiskers and pocket them. Weirdo.',})
kettle = Item(['kettle'], {'examine': 'A polished copper kettle.',
                              'take': 'Taken.',})
schnit = Item(['pork schnitzel', 'schnitzel', 'pork'], {'examine': 'A large pile of pork schnitzel.',
                              'take': 'You take a piece. Yum!',})
apple = Item(['apple strudel', 'strudel'], {'examine': 'A large pile of apple strudel.',
                              'take': 'You take a piece. Yum!',})
goose = Item(['goose'], {'examine': 'An unconscious grey goose.',
                              'take': 'You pocket the goose.',})
rose = Item(['rose'], {'examine': 'A pristine red rose.',
                              'take': 'You pluck a rose.',})
rainrose = Item(['drenched rose', 'rose'], {'examine': 'A red rose, drenched in rain.',
                              'take': 'huh?',})
doll = Item(['girl doll', 'doll', 'girl'], {'examine': 'A doll of a girl with a white dress.',
                              'take': 'You pocket the doll.',})
mittens = Item(['mittens'], {'examine': 'A pair of warm woolen mittens.',
                              'take': 'You pocket the mittens, as they are a bit big for you.',})
package = Item(['suspicious package', 'package'], {'examine': 'A suspicious package wrapped in brown paper. You think you hear a ticking noise.',
                              'take': 'You take the package. Hopefully nothing bad happens.',})
noodles = Item(['noodles', 'bowl'], {'examine': 'A bowl of noodles.',
                              'take': 'Taken.',})
food = Item(['schnitzel with noodles', 'noodles', 'schnitzel', 'food'], {'examine': 'A bowl of schnitzel and noodles.',
                              'take': 'huh?',})
pony = Item(['pony', 'horse'], {'examine': 'A beautiful pony with light fur.',
                              'take': 'You put the pony in your pocket. (Don\'t ask.)',})
rope = Item(['rope'], {'examine': 'A short coil of rope, about eight feet long.',
                              'take': 'You put the coil of rope in your pocket.',})
ocarina = Item(['ocarina'], {'examine': 'A beautiful ocarina that seems somehow familiar.',
                              'take': 'You put the ocarina in your pocket.',})

#utility functions

def knock_cat(p):
    p.set_tmp_milestone('catknock')
    
def knock_goose(p):
    p.set_tmp_milestone('gooseknock')
    
def drench_rose(p):
    p.set_milestone('rainrose')
    for i in range(len(p.items)-1, -1, -1):
        if rose.equals(p.items[i]):
            p.items.append(rainrose)
            p.items.remove(p.items[i])
    
def combine_dish(p):
    p.set_milestone('food')
    p.items.append(food)
    for i in range(len(p.items)-1, -1, -1):
        if schnit.equals(p.items[i]) or noodles.equals(p.items[i]):
            p.items.remove(p.items[i])
    
def attach_rope(p):
    p.set_milestone('grope')
    for i in p.items:
        for i in range(len(p.items)-1, -1, -1):
            if rope.equals(p.items[i]):
                p.items.remove(p.items[i])

# room data

global_actions = [UseAction(['ocarina'],
                            lambda p: p.set_tmp_milestone('tpony'),
                            lambda p: 'You play your ocarina. A pony trots up to you and nuzzles you.' if 'pony' not in p.milestones else 'You play your ocarina for a little while, but unfortunately you only know one song.'),
                  UseWithAction(['schnitzel', 'pork', 'pork schnitzel'], ['noodles'],
                      combine_dish,
                      lambda p: 'You make some schnitzel with noodles.'),
                  UseWithAction(['noodles'], ['schnitzel', 'pork', 'pork schnitzel'],
                      combine_dish,
                      lambda p: 'You make some schnitzel with noodles.'),
                   TakeAction(pony, '', reqs=['tpony']),
                  ]
          
room_map = collections.defaultdict(str)

room_map['start'] = Room(lambda p: 'You are standing %s a small brick building. Around you is a forest. %s%s' %
                                 ('at the end of a road before' if 'house' not in p.temp_milestones else 'on top of',
                                  'A small stream flows out of the building and down a gully.' if p.current_season != 'summer' else 'A dried-up stream bed leads into the building.',
                                 ' A sleigh is sitting near the chimney.' if 'house' in p.temp_milestones and p.current_season == 'winter' else ''),
          [BasicResponseAction(['stream', 'river', 'water'],
                               {'examine': lambda p: 'The water bubbles, crisp and clear.',
                                'drink': lambda p: 'You drink some water. You feel refreshed.',
                                'take': lambda p: 'You don\'t have anything to put it in. Besides, you doubt you\'ll need it.' }),
          BasicResponseAction(['house', 'building'],
                               {'examine': lambda p: 'A cute brick house%s. The door is slightly ajar.' %
                                            (', complete with a doorbell and chimney' if 'doorbell' not in p.milestones else ' with a chimney')}),
          BasicResponseAction(['sleigh'],
                               {'examine': lambda p: 'A standard sleigh, with lots of bells.' if 'house' in p.temp_milestones and p.current_season == 'winter' else 'I can\'t say I know what that is.',
                                'take': lambda p: 'It\'s much too heavy for you to carry the whole thing.' if 'house' in p.temp_milestones and p.current_season == 'winter' else 'I can\'t say I know what that is.'}),
           BasicResponseAction(['chimney'],
                               {'examine': lambda p: 'A nice chimney. Enough bricks are sticking out that you could climb up the house.',
                                'take': lambda p: 'Don\'t be silly.'}),
           
            SimpleToggleAction(['climb'], ['climb', 'jump'], ['house', 'building', 'up', 'down', 'chimney', 'roof'],
                               lambda p: 'You climb on top of the house. %s' % seasonal(['The bricks around the chimney look a little worn.',
                                                                                         'The bricks around the chimney look a little worn.',
                                                                                         'The bricks around the chimney look a little worn.',
                                                                                         'You see a sleigh parked by the chimney.'])(p.current_season),
                               lambda p: 'You climb down from on top of the house.'),
           TakeAction(doorbell, ''),
           TakeAction(sleighbell, '', seasons=['winter'], reqs=['house']),
           MoveAction(['up'], 'fe'),
           MoveAction(['left'], 'g'),
           MoveAction(['down'], 'start', reqs=['xx'], fdesc='An impassable cliff is to the south.'),
           MoveAction(['in', 'house'], 'house'),
           MoveAction(['right'], 'e', seasons=['summer'], fdesc='The stream blocks your path.'),
           ])
room_map['fe'] = Room(lambda p: 'You are standing at the edge of a forest to your north. A %s wind blows across the air. Cliffs are to your right and left.<br><br>You see an old woman sitting nearby.' % seasonal(['cool', 'warm', 'cool', 'chilly'])(p.current_season),
           [MoveAction(['down'], 'start'),
            MoveAction(['up'], 'f'),
            BasicResponseAction(['person', 'woman', 'lady', 'old woman', 'old lady'],
                               {'examine': lambda p: 'A well-kempt old lady with a white dress and faded blond hair. She seems a little unhappy.',
                                'take': lambda p: 'You could probably carry her, but feel like you shouldn\'t.',
                                'talk': lambda p: 'The woman says:<br>"For your final task: have you figured out my name?' if 'grod' in p.milestones else 'The woman says:<br>\
                                                         "Hello, traveler! I was traveling through the area and lost my favorite things. I know you\'re looking for something too, \
                                                         and I might be able to help you out if you can bring them all back!"%s' % p.generate_given() }),
           ])
room_map['f'] = Room(lambda p: 'You are in a large forest. Tall redwoods surround you. Paths lead left, right, down and up.',
           [MoveAction(['down'], 'fe'),
           MoveAction(['up'], 'snow'),
           MoveAction(['right'], 'f2'),
           MoveAction(['left'], 'f3'),
           TakeAction(rod, 'A mysterious rod lies at your feet.'),
           ])
room_map['snow'] = Room(lambda p: 'You are standing in an enclave of %s trees, with a path leading south. %s A stump sits in the center of the enclave%s.%s' % (seasonal(['green', 'green', 'orange', 'snow-capped'])(p.current_season),
                                                                                                                       seasonal(['A light rain is falling.','','','Snow is gently falling.'])(p.current_season),
                                                                                                                        (', which you are standing on' if 'stump' in p.temp_milestones else ''),
                                                                                                                        (' A rope hangs over a cliff to your north.' if 'grope' in p.milestones else '')),
           [MoveAction(['down'], 'f'),
            MoveAction(['up', 'climb'], 'n', reqs=['grope']),
            TakeAction(snowflake, '', seasons=['winter']),
            BasicResponseAction(['stump'],
                                 {'examine': lambda p: 'The stump is about two feet tall and rather old-looking.',
                                  'sit': lambda p: 'You sit on the stump for a while, thinking about the passing seasons.',
                                  'take': lambda p: 'Are you just going to try and take everything you come across?'}),
            SimpleToggleAction(['hop', 'stand', 'jump'], ['hop', 'jump', 'stand'], ['stump', 'tree'],
                    lambda p: 'You jump on top of the stump.',
                    lambda p: 'You jump down from the stump.'),
            UseAction(['rod'],
                      lambda p: p.change_season(),
                      lambda p: 'You swing your rod from on top of the stump. The trees change color to %s. %s' % (seasonal(['a warm green', 'a warm orange', 'a pale white', 'a pale green'])(p.current_season),
                                                                                                                seasonal(['The light rain stops.','','Snow begins to fall.', 'A light rain begins to fall.'])(p.current_season)),
                      reqs = ['stump']),
            UseWithAction(['rose'], ['rain'],
                      drench_rose,
                      lambda p: '%s' % ('You drench the rose with raindrops.' if 'rainrose' not in p.milestones and p.current_season == 'spring' else 'You can\'t use that like that.')),
           
           ])
room_map['f2'] = Room(lambda p: 'You are in a large forest. Paths lead north and west, and dense foliage is in the other directions.',
           [MoveAction(['left'], 'f'),
           MoveAction(['up'], 'c'),
            ])
room_map['f3'] = Room(lambda p: 'You are in a large forest. Paths lead north and east, and dense foliage is in the other directions.',
           [MoveAction(['right'], 'f'),
           MoveAction(['up'], 'ac'),
            ])
room_map['c'] = Room(lambda p: 'You are facing a large cliff face %s to your north. A path leads south, with a sign off to one side of it.' % (seasonal(['', ' with vines growing on its side', '', '']))(p.current_season),
           [MoveAction(['down'], 'f2'),
            MoveAction(['up', 'climb'], 'sword', seasons=['summer'], fdesc='You can\'t climb the cliff.'),
            BasicResponseAction(['sign'],
                               {'examine': lambda p: 'The sign says:<br>"In summer, vines grow tall and creeks dry up. Remember that."',
                                'take': lambda p: 'The sign is firmly rooted in the ground.'}),
            ])
room_map['ac'] = Room(lambda p: 'You are at %s. A path leads south.' % (seasonal(['a large impassable hole in the ground that blocks the way north',
                                                                                  'a large impassable hole in the ground that blocks the way north',
                                                                                  'a large pile of leaves filling a hole in the ground',
                                                                                  'a large impassable hole in the ground that blocks the way north']))(p.current_season),
           [MoveAction(['down'], 'f3'),
            MoveAction(['up'], 'ocarina', seasons=['autumn'], fdesc='You can\'t cross the hole.'),
            BasicResponseAction(['hole'],
                               {'examine': lambda p: 'The hole looks far too deep to cross, and it doesn\'t look like you can go around.',}),
            ])
room_map['sword'] = Room(lambda p: 'You are standing in a glade of evergreen trees looking over the rest of the land. A clearing is down a steep slope to your left, and vines lead down a cliff to the south.',
          [BasicResponseAction(['trees'],
                               {'examine': lambda p: 'The trees are imposing and look very old.'}),
          BasicResponseAction(['clearing'],
                               {'examine': lambda p: 'The clearing is about fifteen feet below you. You can slide down, but you won\'t be able to make it back up.'}),
           
           TakeAction(sword, 'A regal sword lies in a stone at the center of the glade.'),
           MoveAction(['down'], 'c'),
           MoveAction(['left'], 'n'),
           ])
room_map['ocarina'] = Room(lambda p: 'You are standing in a glade of trees. A pile of leaves is to the south, and a clearing is down a steep slope to your right.',
          [BasicResponseAction(['trees'],
                               {'examine': lambda p: 'Just your standard forest trees, about yea high.'}),
          BasicResponseAction(['clearing'],
                               {'examine': lambda p: 'The clearing is about fifteen feet below you. You can slide down, but you won\'t be able to make it back up.'}),
           
           TakeAction(ocarina, 'An ocarina lies on the ground.'),
           MoveAction(['down'], 'ac'),
           MoveAction(['right'], 'n'),
           ])
room_map['house'] = Room(lambda p: 'You are standing in the living room of a cottage. A sparse kitchen is to the left, and a cat purrs in the corner. A handwritten note rests by the fireplace. The entrance door is behind you.',
           [MoveAction(['out', 'outside', 'door'], 'start'),
            MoveAction(['left', 'kitchen'], 'kitchen'),
            TakeAction(rope, 'A short coil of rope sits in the corner.'),
            TakeAction(whiskers, '', reqs=['catknock']),
            BasicResponseAction(['fireplace'],
                                 {'examine': lambda p: 'A tidy fireplace. Looks like it hasn\'t been used in a long time.',
                                  'take': lambda p: 'Don\'t be silly.'}),
            BasicResponseAction(['note', 'paper'],
                               {'examine': lambda p: 'The note says:<br>"Santa Welcome!!!"',
                                'take': lambda p: 'Better not. Someone might get angry.'}),
            BasicResponseAction(['cat', 'whiskers'],
                                 {'examine': lambda p: 'The cat is energetic and young, and has golden-brown fur and long whiskers.',
                                  'take': lambda p: 'You try to catch the cat, but it always manages to wriggle free of your grasp. Perhaps a little more force is necessary.' if 'catknock' not in p.temp_milestones else 'You don\'t feel like you need the whole cat.'}),
            UseWithAction(['sword'], ['cat'],
                      knock_cat,
                      lambda p: '%s' % ('You strike at the cat with the blunt of your blade, who is not fast enough to evade you. The cat collapses, unconscious.' if 'catknock' not in p.temp_milestones else 'You\'re pretty rude, but not rude enough to do that again.')),
           ])
room_map['kitchen'] = Room(lambda p: 'You are in the kitchen of a cottage. A refrigerator is in one corner with its door %s, and various pots, pans and knives line the walls. A living room is to your east.' %
                           ('open and tons of food inside' if 'fridge' in p.temp_milestones else 'closed'),
           [MoveAction(['outside'], 'start'),
            MoveAction(['back', 'right', 'living room', 'entrance', 'out'], 'house'),
            TakeAction(kettle, 'A copper kettle on the stove catches your eye.'),
            TakeAction(schnit, '', reqs=['fridge']),
            TakeAction(apple, '', reqs=['fridge']),
            BasicResponseAction(['fridge', 'refrigerator'],
                               {'examine': lambda p: 'A white refrigerator. Looks heavy.' if 'fridge' not in p.temp_milestones else 'A white refrigerator with tons of pork schnitzel and apple strudel inside!',
                                'take': lambda p: 'Unfortunately, you don\'t work out enough to carry this.'}),
            BasicResponseAction(['pot', 'pan', 'pots', 'pans', 'knife', 'knives', 'utensils'],
                                 {'examine': lambda p: 'The kitchen utensils are highly polished and looking spotless.',
                                  'take': lambda p: 'Somehow you don\'t feel as if you need these.'}),
            SimpleToggleAction(['open'], ['close'], ['fridge', 'refrigerator', 'door'],
                               lambda p: 'You open the refrigerator door.',
                               lambda p: 'You close the refrigerator door.')
           ])
room_map['e'] = Room(lambda p: 'You are standing on a large, grassy knoll. Wild geese flock about and the sun shines bright. A house with a dry river is to your west, and you are otherwise surrounded by cliffs.',
           [MoveAction(['left'], 'start'),
            TakeAction(goose, '', reqs=['gooseknock']),
            BasicResponseAction(['goose', 'geese'],
                                 {'examine': lambda p: 'A beautiful flock of wild geese.',
                                  'take': lambda p: 'You try to catch a goose, but you don\'t even come close. Perhaps something with a little more force will help.'}),
            UseWithAction(['sword'], ['geese', 'goose'],
                      knock_goose,
                      lambda p: '%s' % ('You strike at a nearby goose with the blunt of your blade. It falls to your feet, unconscious.' if 'gooseknock' not in p.temp_milestones else 'You definitely don\'t need another goose.')),
           
           ])
room_map['g'] = Room(lambda p: 'You are standing on a grassy knoll. A house is to your east, and you are otherwise surrounded by cliffs.%s' % seasonal([' Roses dot the landscape.', ' It is warm and sunny, and you can see a few dead flowers around.', '', ' There is no snow, but the wind is harsh.'])(p.current_season),
           [MoveAction(['right'], 'start'),
            TakeAction(rose, '', seasons=['spring']),
            ])
room_map['n'] = Room(lambda p: 'You are standing in a clearing.%s An enclave with a stump at its center is to the south, down a cliff of about six feet. A sturdy tree root is visible near the cliff.' % seasonal([' A lake is to the north.', ' A lake is to the north.', ' A lake is to the north.', ' A frozen lake is to the north.'])(p.current_season),
           [MoveAction(['up'], 'cabin', seasons=['winter'], fdesc='Unfortunately, you can\'t swim.'),
            MoveAction(['down'], 'snow'),
            MoveAction(['left', 'right'], 'start', reqs=['xx'], fdesc='The slope is too steep to ascend.'),
            BasicResponseAction(['root'],
                {'examine': lambda p: 'A root about half a foot thick, probably from a nearby tree.',
                 'take': lambda p: 'There\'s no way you can detach this from the tree.' }),
            BasicResponseAction(['stump'],
                {'examine': lambda p: 'It looks like the same stump you came across earlier.',
                 'take': lambda p: 'Are you just going to try and take everything you come across?' }),
            BasicResponseAction(['lake', 'pond'],
                {'examine': lambda p: 'A lake with clear water. Unfortunately, you can\'t swim very well.' if p.current_season != 'winter' else 'A frozen lake. You can probably cross to the other side.' }),
            UseWithAction(['rope'], ['root', 'branch'],
                      attach_rope,
                      lambda p: 'You tie your rope to the branch and let it fall over the cliff. Now you can get back up from the clearing!'),
            ])
room_map['cabin'] = Room(lambda p: 'You are standing in front of a one-room wooden cabin. You are on the shore of a frozen lake, which is to your south.',
           [MoveAction(['in', 'cabin'], 'incabin'),
            MoveAction(['down'], 'n'),
            TakeAction(doll, 'A doll of a girl in a white dress is lying in the snow.'),
            BasicResponseAction(['cabin', 'house'],
                {'examine': lambda p: 'A one-room cabin.' }),
            BasicResponseAction(['lake', 'pond'],
                {'examine': lambda p: 'A lake with clear water. Unfortunately, you can\'t swim very well.' if p.current_season != 'winter' else 'A frozen lake. You can probably cross to the other side.' }),
            ])
room_map['incabin'] = Room(lambda p: 'You are standing inside a small cabin. It is dimly lit, and there is a small table in the center of the room.',
           [MoveAction(['out', 'outside', 'door'], 'cabin'),
            TakeAction(mittens, 'A pair of mittens is on the table.'),
            TakeAction(package, 'A suspicious package is on the table.'),
            TakeAction(noodles, 'A bowl of noodles is on the table, uneaten.'),
            BasicResponseAction(['table'],
                {'examine': lambda p: 'A simple square table, about three feet to a side.' }),
            ])

# misc

help_text = 'Mystical Seed of Harmony is an exciting text-based adventure!<br>\
            For best results, type a COMMAND followed by a TARGET. For instance, use \'go\' to get around -- e.g. "go up" or "go in".<br>\
            -Look at the area with "look", or look at an object with "look" followed by the item.<br>\
            -Take an item with "take", and use it with "use". You can use an item X with another item Y by typing "use X with Y".<br>\
            -You can view your inventory by typing "inventory".<br>\
            -There are other commands that are more situation-specific! If you have a good idea, try to see if it works!'
