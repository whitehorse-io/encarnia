# -*- coding: utf-8 -*-

# mygame/world/batchcode_world.py

from evennia import create_object, search_object
from typeclasses import rooms, exits
from evennia.utils import evtable
from world import map_module

# We begin by creating our rooms so we can detail them later.

centre = create_object(rooms.Room, key="crossroads")
north = create_object(rooms.Room, key="castle")
east = create_object(rooms.Room, key="cottage")
south = create_object(rooms.Room, key="camp")
west = create_object(rooms.Room, key="coast")

# This is where we set up the cross roads.
# The rooms description is what we see with the 'look' command.

# Replace the descriptions with the below code.

# The cross roads.
# We pass what we want in our table and EvTable does the rest.
# Passing two arguments will create two columns but we could add more.
# We also specify no border.
centre.db.desc = evtable.EvTable(map_module.return_minimap(4,5),
                 "The merger of two roads. A single lamp post dimly " \
                 "illuminates the lonely crossroads. To the north " \
                 "looms a mighty castle. To the south the glow of " \
                 "a campfire can be seen. To the east lie a wall of " \
                 "mountains and to the west the dull roar of the open sea.",
                 border=None)
# EvTable allows formatting individual columns and cells. We use that here
# to set a maximum width for our description, but letting the map fill
# whatever space it needs.
centre.db.desc.reformat_column(1, width=70)

# [...]

# The northern castle.
north.db.desc = evtable.EvTable(map_module.return_minimap(4,2),
                "An impressive castle surrounds you. There might be " \
                "a princess in one of these towers.",
                border=None)
north.db.desc.reformat_column(1, width=70)

# [...]

# The eastern cottage.
east.db.desc = evtable.EvTable(map_module.return_minimap(6,5),
               "A cosy cottage nestled among mountains stretching " \
               "east as far as the eye can see.",
               border=None)
east.db.desc.reformat_column(1, width=70)

# [...]

# The southern camp.
south.db.desc = evtable.EvTable(map_module.return_minimap(4,7),
                "Surrounding a clearing are a number of tribal tents " \
                "and at their centre a roaring fire.",
                border=None)
south.db.desc.reformat_column(1, width=70)

# [...]

# The western coast.
west.db.desc = evtable.EvTable(map_module.return_minimap(2,5),
               "The dark forest halts to a sandy beach. The sound of " \
               "crashing waves calms the soul.",
               border=None)
west.db.desc.reformat_column(1, width=70)