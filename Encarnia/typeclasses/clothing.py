"""
Clothing

The default clothing object.

"""
from evennia import DefaultObject
from world import english_utils
from evennia.utils import list_to_string
from random import randint
import time

class Clothes(DefaultObject):
    """
  
     """
    def at_object_creation(self):

        #Inherit the object properties.
        super(Clothes, self).at_object_creation()

        self.aliases.add([])

        self.db.desc = False
        self.db.wear_msg = False
        self.db.wear_msg_room_1 = False
        self.db.wear_msg_room_2 = False
        self.db.remove_msg = False
        self.db.remove_msg_room_1 = False
        self.db.remove_msg_room_2 = False
        self.db.type = ["vest"]

        self.db.is_worn = False

        self.db.duration = 0.0

    #         if not wearer.db.wearing[cover][self.db.slot] == "empty":
    #             taken.append(cover)