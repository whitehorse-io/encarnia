"""
Readables

A readable plaque.

"""
from evennia import DefaultObject, Command, CmdSet
from world import english_utils
from evennia.utils import list_to_string
from random import randint
import time
from typeclasses.objects import Object

# the "read" command

class CmdReadSign(Command):
    """
    Hit a box until it breaks

    Usage:
      hit box

    If the object is breakable, it will eventually
    break down after enough hits.
    """
    key = "read sign"
    #aliases = ["hit", "break box", "break"]
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        # this Command sits on the box, so we don't need to search for it
        self.caller.msg(self.obj.db.text)


class SignCmdSet(CmdSet):
    key = "read_sign_cmdset"

    def at_cmdset_creation(self):
        self.add(CmdReadSign())

class Sign(DefaultObject):
    """

     """

    def at_object_creation(self):
        # Inherit the object properties.
        super(Plaque, self).at_object_creation()

        self.aliases.add([])

        self.db.desc = False

        self.db.text = "Beware: Lions..."

        self.cmdset.add(SignCmdSet, permanent=True)