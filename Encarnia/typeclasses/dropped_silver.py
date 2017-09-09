"""
Weapon

The default weapon object, file is called Arms so that it doesn't conflict with a tutorial weapon object.

"""
from evennia import DefaultObject
from world import english_utils
from random import randint
import time


class Dropped_Silver(DefaultObject):
    """

     """

    def at_object_creation(self):

        # Inherit the object properties.
        super(Dropped_Silver, self).at_object_creation()

        self.db.key = "a single silver sovereign"
        self.db.aliases = ["money", "coins"]
        self.db.desc = "Silver sovereigns have the likeness of a mighty lion engraved upon their surface on one side and the Tower of Corinth on the other."
        #self.location = caller.location
        self.db.coins_value = 1
        self.db.location = False