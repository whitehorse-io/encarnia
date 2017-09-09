"""
Weapon

The default weapon object, file is called Arms so that it doesn't conflict with a tutorial weapon object.

"""
from evennia import DefaultObject
from world import english_utils
from random import randint
import time


class Canteen(DefaultObject):
    """

     """

    def at_object_creation(self):

        # Inherit the object properties.
        super(Canteen, self).at_object_creation()

        self.aliases.add([])

        #self.name = "a ruddy bronze broadsword" # not sure if I need this
        self.db.short_name = "a tin canteen" # no preceding partical; may be much shorter
        self.db.desc = "This small tin canteen is perfect for holding some kind of drink, although the material might cause the contents to heat up in the wrong environment."

        self.db.max_sips = 4

        self.db.duration = 0.0

        #self.db.get_err_msg = "This is too heavy to pick up."

        #self.locks.add("get:false()") -- adds locks to the object.