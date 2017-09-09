# mygame/world/batchcode_map.py

from evennia import create_object
from evennia import DefaultObject
from world import map_module

map = create_object(DefaultObject, key="Map", location=caller.location)

map.db.desc = map_module.return_map()

caller.msg("A map appears out of thin air and falls to the ground.")