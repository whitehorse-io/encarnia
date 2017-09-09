"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom, default_cmds, CmdSet, utils
#from commands import BaseCommand

from evennia import TICKER_HANDLER as tickerhandler
from evennia.utils.evmenu import EvMenu

class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    pass

#WHN: Adding stuff from here on.
from commands.default_cmdsets import ChargenCmdset, ShopCmdset, BankCmdset

class ChargenRoom(Room):
    """
    This room class is used by character-generation rooms. It makes
    the ChargenCmdset available.
    """
    def at_object_creation(self):
        "this is called only at first creation"
        self.cmdset.add(ChargenCmdset, permanent=True)

    def return_appearance(self, looker):
        """
        The return from this method is what
        looker sees when looking at this object.
        """
        text = "|c" + self.name + "|n\n" + self.db.desc

        return text
        # text = super(Character, self).return_appearance(looker)
        # cscore = " (combat score: %s)" % self.db.combat_score
        # if "\n" in text:
        #     # text is multi-line, add score after first line
        #     first_line, rest = text.split("\n", 1)
        #     text = first_line + cscore + "\n" + rest
        # else:
        #     # text is only one line; add score to end
        #     text += cscore
        # return text

class BankRoom(Room):
    """
    This room class is used by character-generation rooms. It makes
    the ChargenCmdset available.
    """
    def at_object_creation(self):
        "this is called only at first creation"
        self.cmdset.add(BankCmdset, permanent=True)
        #self.add(business.CmdDeposit())

class ShopRoom(Room):
    """
    This room class is used by character-generation rooms. It makes
    the ChargenCmdset available.
    """

    def at_object_creation(self):
        "this is called only at first creation"
        self.cmdset.add(ShopCmdset, permanent=True)

class DeathRoom(Room):
    """
    A room that runs the death timer and blocks certain commands.

    Original death_room appeared to suffer from a bug... don't use it!
    """

    def return_appearance(self, looker):
        """
        The return from this method is what
        looker sees when looking at this object.
        """
        text = "|c" + self.name + ".|n\n" + self.db.desc

        return text

    def DeathRoom_Ticker(self, *args, **kwargs):
        "ticked at regular intervals"
        for i in self.contents:
            if utils.inherits_from(i, "typeclasses.characters.Character"):
                i.db.death_ticker = i.db.death_ticker + 1
                if i.db.death_ticker == 2:
                    i.msg("\nYou see nothing, hear nothing, feel nothing. Then you realize that your consciousness has returned.")
                elif i.db.death_ticker == 3:
                    i.msg("\nYou realize that there is something floating in the darkness ahead of you... a fearsome black lion! At first you are afraid, but then you realize that this can only be the One True King of Encarnia: Ashlan, the Black Lion!")
                elif i.db.death_ticker == 4:
                    i.msg("\n|cAshlan the King Roars, \"%s... %s! Go towards the light! The light!\"|n" % (i.name, i.name))
                elif i.db.death_ticker == 5:
                    i.msg("\nYou try to move towards the light but an invisible wall holds you back!")
                elif i.db.death_ticker == 6:
                    i.msg("\n|cAshlan says, \"Oh wow. Wow. Well, bye.\"|n")
                elif i.db.death_ticker == 7:
                    i.msg("\nA moment later you realize that Ashlan is gone.")
                elif i.db.death_ticker == 8:
                    i.msg("\nAfter an interminable amount of time, you notice something else in the darkness.  A massive, slow-moving snake!")
                elif i.db.death_ticker == 9:
                    i.msg("\n|cThe great Python hisses, \"%s! Go towards the light, or I shall devour your soul!\"|n" % i.name)
                elif i.db.death_ticker == 10:
                    i.msg("\nYou run towards the light, this time in a panic but it rejects you again.")
                elif i.db.death_ticker == 11:
                    i.msg("\n|cThe great Python hisses, \"Sucks to be you...\"|n and melts into the shadows.")
                elif i.db.death_ticker == 13:
                    i.msg("\nAfter another period of time; it might have been minutes or years, you don't know... you see another being in the shadows.")
                elif i.db.death_ticker == 14:
                    i.msg("\nUnlike the other two, this one is deathly pale. Cold iron chains sprout from his clawed hands, feet and neck.")
                elif i.db.death_ticker == 15:
                    i.msg("\n|m\"%s... you know me,\" the pale horror croaks.|n Uncomfortably, you look around for the light but it is nowhere to be seen!" % i.name)
                elif i.db.death_ticker == 16:
                    i.msg("\n|m\"You have fed off my might. Hidden in my shadow. Pretended that my power was your power. But it was not. And now, you are mine!\"|n")
                elif i.db.death_ticker == 17:
                    i.msg("\n|mThe pale horror continues, \"That fool Ashlan thinks me humiliated. He thinks his children have gotten the better of me. But this is only the beginning of our game. You are mine and you will not die until I permit it!\"|n")
                elif i.db.death_ticker == 18:
                    i.msg("\nThe horror twitches a hand towards you and cold iron shackles suddenly appear! They fasten onto your arms, your legs, your neck. They drag you off into the darkness...")
                elif i.db.death_ticker >= 19:
                    i.db.dead = False
                    destination = i.search("#737", global_search=True)
                    # caller.msg(destination)
                    i.msg(
                        "You wake up beneath a willow tree, next to a recently dug shallow grave.")
                    i.move_to(destination, quiet=True)
                    return

    def at_object_creation(self):
        # Ticker handler for timed effects; regeneration, bleeding, etc.
        tickerhandler.add(10, self.DeathRoom_Ticker)

    def at_object_receive(self, character, source_location):
        tickerhandler.add(10, self.DeathRoom_Ticker)