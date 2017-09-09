"""
Weapon

The default weapon object, file is called Arms so that it doesn't conflict with a tutorial weapon object.

"""
from evennia import DefaultObject
from world import english_utils
from random import randint
import time


class Weapons(DefaultObject):
    """

     """

    def at_object_creation(self):

        # Inherit the object properties.
        super(Weapons, self).at_object_creation()

        self.aliases.add([])

        #self.name = "a ruddy bronze broadsword" # not sure if I need this
        self.db.short_name = "" # no preceding partical; may be much shorter
        self.db.desc = ""

        self.db.open_terrain = 10
        self.db.cluttered_terrain = 5
        self.db.narrow_terrain = 5

        self.db.damage_multiplier = 1.0

        self.db.balance_duration_change = 0.0

        self.db.weapon_type = "1hsword"

        #TODO: This will be changed to reflect how long the object lasts; get, wield and unwield can check this, turning it to dust when that action is done if the timer is used up.  That broadsword was older than you thought!
        self.db.duration = 0.0

        #self.db.get_err_msg = "This is too heavy to pick up."

        #self.locks.add("get:false()") -- adds locks to the object.