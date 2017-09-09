"""
Commands

Commands describe the input the player can do to the game.

"""

from evennia import Command as BaseCommand
from evennia import utils
from evennia.commands.default.muxcommand import MuxCommand
from world import rules
from world import english_utils
from random import randint
from evennia.utils.spawner import spawn
import time
from evennia.comms.models import ChannelDB, SubscriptionHandler
from evennia.comms.channelhandler import CHANNELHANDLER

class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns True, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.

    """
    @staticmethod
    def show_balance(self):
        caller = self.caller

        # This happens if someone doesn't have balance back yet: the skill gives a message and aborts.
        if time.time() < caller.db.balance_time:
            if caller.db.balance_time - time.time() > 3:
                caller.msg("You need 3 more seconds!")
            elif caller.db.balance_time - time.time() > 2:
                caller.msg("You need 2 more seconds!")
            elif caller.db.balance_time - time.time() > 1:
                caller.msg("You need 1 more second!")
            elif caller.db.balance_time - time.time() > 0:
                caller.msg("You've almost regained balance!")
            return True

    def at_post_cmd(self):
        """
        This hook is called after the command has finished executing
        (after self.func()).
        """
        caller = self.caller

        if caller.db.health != None:
            if (float(caller.db.health) / float(caller.db.max_health)) > 0.80:
                prompt_hp_color = "|g"
            elif (float(caller.db.health) / float(caller.db.max_health)) > 0.36:
                prompt_hp_color = "|y"
            else:
                prompt_hp_color = "|r"

            if caller.db.stamina > 6:
                prompt_stamina_color = "|g"
            elif caller.db.stamina > 3:
                prompt_stamina_color = "|y"
            else:
                prompt_stamina_color = "|r"

            magic_level = "Asleep"
            if caller.db.current_magic == 0:
                magic_level = "Asleep"
            elif caller.db.current_magic > 7:
                magic_level = "|rRaging|n"
            elif caller.db.current_magic > 4:
                magic_level = "|yIrate|n"
            elif caller.db.current_magic > 0:
                magic_level = "|gAwoken|n"

            prompt = "%sHealth|n: %s%s|n - |gMagic|n: %s|n - %sStamina|n: %s%s." % (
            prompt_hp_color, prompt_hp_color, caller.db.health, magic_level, prompt_stamina_color, prompt_stamina_color,
            caller.db.stamina)

            caller.msg(prompt)

# class CmdMobCalm(MeleeCommand):
#     """
#     Turn off an npc's combat ticker (this may screw up always-hostile npcs!)
#
#     Usage:
#       mobcalm [<mob>]
#
#     """
#
#     key = "mobcalm"
#     #aliases = ["kill", "att"]
#     locks = "cmd:perm(Wizards)"
#     help_category = "Gods"
#
#     def parse(self):
#         "Very trivial parser"
#         self.target = self.args.strip()
#
#
#     def func(self):
#
#         caller = self.caller
#
#         if not self.target or self.target == "here":
#             caller.msg("Calm what?")
#             return
#         else:
#             target = caller.search(self.target)
#             if not target:
#                 caller.msg("%s isn't here to calm." % target.name)
#                 # caller.search handles error messages
#                 return
#
#         #tickerhandler.remove(target.db., myfunc) # Not finished yet!


def find_channel(caller, channelname, silent=False, noaliases=False):
    """
    Helper function for searching for a single channel with
    some error handling.
    """
    channels = ChannelDB.objects.channel_search(channelname)
    if not channels:
        if not noaliases:
            channels = [chan for chan in ChannelDB.objects.get_all_channels()
                        if channelname in chan.aliases.all()]
        if channels:
            return channels[0]
        if not silent:
            caller.msg("Channel '%s' not found." % channelname)
        return None
    elif len(channels) > 1:
        matches = ", ".join(["%s(%s)" % (chan.key, chan.id) for chan in channels])
        if not silent:
            caller.msg("Multiple channels match (be more specific): \n%s" % matches)
        return None
    return channels[0]


class CmdScore(Command):
    """
    See basic information about your character.

    Usage:
      score

    """
    key = "score"
    #aliases = ["status", "stat"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        string = "|c" + caller.name + ".|n"
        caller.msg(string)
        caller.msg("You are %s %s %s." % (english_utils.iart(caller.db.gender), caller.db.physique, str(caller.db.race).capitalize()))
        caller.msg("You currently are level %s and are %s%% of the way to the next level." % (caller.db.level, caller.db.exp))
        caller.msg("You are a citizen of Corinth, in good standing with the Tower.")
        caller.msg("You are not a member of any guild or a part of any clans.")
        caller.msg("You have no affiliation towards the Seelie or Unseelie Courts.")
        caller.msg("Only you know how old you are!")

        string= "You are carrying {:,} silver sovereigns.".format(caller.db.silver_carried)
        caller.msg(string)

        string = "You have {:,} silver sovereigns in your bank account.".format(caller.db.tower_bank_account)
        caller.msg(string)

class CmdStat(Command):
    """
    See basic numerical information about your character.

    Usage:
      stat

    """
    key = "stat"
    aliases = ["status"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        string = "|c" + caller.name + ".|n"
        caller.msg(string)
        caller.msg("Health: %s / %s." % (caller.db.health, caller.db.max_health))
        caller.msg("Strength: %s / %s." % (caller.db.current_strength, caller.db.base_strength))
        caller.msg("Agility: %s / %s." % (caller.db.current_agility, caller.db.base_agility))
        caller.msg("Constitution: %s / %s." % (caller.db.current_constitution, caller.db.base_constitution))
        caller.msg("Endurance: %s vs. a d20 chance to lose stamina on most physical combat actions." % caller.db.endurance)
        caller.msg("Magic: %s maximum magical power and control." % (caller.db.magic))

        if caller.db.enchantments:
            for i in caller.db.enchantments:
                caller.msg("You have %s enchantment in place." % english_utils.iart(i))

class CmdMap(Command):
    """
    See basic information about your character.

    Usage:
      score

    """
    key = "map"
    help_category = "Equipment"
    #aliases = ["status", "stat"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        string = "You don't possess a map for the current area (sorry, mapping is not implemented yet)."
        caller.msg(string)

        if caller.location.tags.get('city', category='corinth'):
            caller.msg("Since you are in Corinth, you may |wwalk to|n different destinations.")

class CmdDrawMap(Command):
    """
    Draws a map (WIP).

    Usage:
      drawmap

    """
    key = "drawmap"
    help_category = "Equipment"
    #aliases = ["status", "stat"]
    locks = "perm(Builders)"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        string = "Map drawing is not implemented yet but I'm working on it!"
        caller.msg(string)

class CmdWalkTo(Command):
    """
    Walk to areas of interest within your city.
    Entering |wwalk to|n without a destination will list the available options.

    Usage:
      walk to <destination>

    """
    key = "walk to"
    #aliases = ["status", "stat"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def keep_walking(self):

        caller = self.caller

        if caller.db.auto_walking:
            if not caller.location.db.walk_to:
                caller.msg("Directions are not available from this part of the city, sorry!")
                caller.db.auto_walking = False
            if caller.db.following:
                caller.msg("You stop following %s." % caller.db.following.name)
                caller.db.following = False
            else:
                for k, v in caller.location.db.walk_to.iteritems():
                    if k == caller.db.auto_walk_target:
                        if v == "here":
                            caller.db.auto_walking = False
                            caller.msg("You have arrived!")
                            return
                        destination = caller.search(v)
                        caller.msg("You continue walking towards the %s area." % caller.db.auto_walk_target)
                        caller.move_to(destination)
                        #utils.delay(0.2, callback=self.at_after_traverse(self, traversing_object))
                utils.delay(0.3, callback=self.keep_walking)

    def func(self):
        """implements the command."""

        caller = self.caller
        target = self.target

        locations = ["inn", "armor", "weapons", "clothing", "bank", "church", "catacombs", "north gate", "south gate"]

        if not caller.location.tags.get('city', category ='corinth'):
            caller.msg("You can only |wwalk to|n locations when you are within a city.")
            return

        if not self.target or self.target == "here":
            caller.msg("You can |wwalk to|n the following locations: inn, armor, weapons, clothing, bank, church, catacombs, north gate, south gate.")
            return
        elif target not in locations:
            caller.msg("You can |wwalk to|n the following locations: inn, armor, weapons, clothing, bank, church, catacombs, north gate, south gate.")
            return
        elif target in locations:
            caller.msg("Walking to: %s." % target)
            caller.db.auto_walking = True
            caller.db.auto_walk_target = target

        if not caller.location.db.walk_to:
            caller.msg("Directions are not available from this part of the city, sorry!")
            caller.db.auto_walking = False
            return
        else:
            self.keep_walking()

class CmdHonors(Command):
    """
    See basic information about another.

    Usage:
      honors <person>

    """
    key = "honors"
    help_category = "Comms"
    aliases = ["honours", "reputation", "rep"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        """implements the command."""

        caller = self.caller

        if not self.target or self.target == "here" or utils.inherits_from(self.target, "typeclasses.characters.Character"):
            caller.msg("Examine whose reputation?")
            return
        else:
            target = caller.search(self.target, global_search=True)
            if not target:
                caller.msg("No one seems to know of a %s." % str.capitalize(str(self.target)))
                # caller.search handles error messages
                return

        string = "|c" + target.name + ".|n"
        caller.msg(string)
        caller.msg("%s is %s %s." % (str.capitalize(target.db.genders), english_utils.iart(target.db.physique), target.db.race))
        caller.msg("%s is currently level %s." % (str.capitalize(target.db.genders), target.db.level))
        caller.msg("%s is a citizen of Corinth, in good standing with the Tower." % str.capitalize(target.db.genders))
        caller.msg("%s is not a member of any guild or a part of any clans." % str.capitalize(target.db.genders))
        caller.msg("%s has no affiliation towards the Seelie or Unseelie Courts." % str.capitalize(target.db.genders))
        caller.msg("It is not known how old %s is." % target.db.genders)

class CmdFollow(Command):
    """
    Follow another character as they move around.

    Usage:
      follow <person>

    """
    key = "follow"
    help_category = "General"
    #aliases = ["honours", "reputation", "rep"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        """implements the command."""

        caller = self.caller

        if not self.target or self.target == "here" or utils.inherits_from(self.target, "typeclasses.characters.Character"):
            caller.msg("Follow who?")
            return
        else:
            target = caller.search(self.target)
            if not target:
                caller.msg("You do not see %s here." % str(self.target))
                # caller.search handles error messages
                return

        caller.db.following = target
        if not target.db.followed_by:
            target.db.followed_by = []
        if caller not in target.db.followed_by:
            target.db.followed_by.append(caller)

        caller.msg("You begin to follow %s." % target.name)
        target.msg("%s appears to be following you." % caller.name)
        string_r = "%s seems to be following %s." % (caller.name, target.name)
        caller.location.msg_contents(string_r, exclude=[caller, target])

class CmdLose(Command):
    """
    Stop another character from following you.

    Usage:
      lose <person>

    """
    key = "lose"
    help_category = "General"
    #aliases = ["honours", "reputation", "rep"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        """implements the command."""

        caller = self.caller

        if not self.target or self.target == "here" or utils.inherits_from(self.target, "typeclasses.characters.Character"):
            caller.msg("Lose who?")
            return
        else:
            target = caller.search(self.target)
            if not target:
                caller.msg("You do not see %s here." % str(self.target))
                # caller.search handles error messages
                return

        if target in caller.db.followed_by:
            caller.db.followed_by.remove(target)
            caller.msg("You subtly give %s the slip." % target.name)
            target.db.following = False
        else:
            caller.msg("%s is not following you." % target.name)

class CmdSkin(Command):
    """
    Skin a slain creature to acquire its pelt or scales.

    Usage:
      skin <remains>

    """
    key = "skin"
    #aliases = ["honours", "reputation", "rep"]
    help_category = "General"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        """implements the command."""

        caller = self.caller

        crude_small_pelt = {"key": "a small and crude fur pelt",
                                "typeclass": "typeclasses.objects.Object",
                                "desc": "This small fur pelt was barely removed successfully and it shows.",
                                "location": caller,
                                "birth_time": time.time(),
                                "duration": 2000000.0}

        small_pelt = {"key": "a small fur pelt",
                          "desc": "This is a generic small fur pelt; not too high in quality but not too bad either.",
                          "location": caller,
                          "birth_time": time.time(),
                          "duration": 2000000.0}

        fine_small_pelt = {"key": "a small but fine fur pelt",
                               "typeclass": "typeclasses.objects.Object",
                               "desc": "This is an exemplary fur pelt, removed from a fine beast by a skilled skinner.",
                               "location": caller,
                               "birth_time": time.time(),
                               "duration": 2000000.0}

        if not self.target or self.target == "here":
            caller.msg("Skin what?")
            return
        else:
            target = caller.search(self.target)
            if not target:
                caller.msg("You do not see that here.")
                # caller.search handles error messages
                return

        if target.db.skinned_yet:
            caller.msg("That has already been skinned.")
            return

        if target.db.alive:
            caller.msg("It's still alive!")
            return

        if not utils.inherits_from(target, "typeclasses.npcs.Combat_Mob"):
            caller.msg("You can't skin %s." % target.name)
            return

        d3 = randint(1, 3)
        target.db.skinned_yet = True

        # I need to add lists that work with
        if d3 == 1:
            skin = spawn(crude_small_pelt, location=caller)
            string = "You skin the remains and produce a crude fur pelt."
            string_r = "%s skins %s and produces a crude fur pelt." % (caller.name, target.name)
        if d3 == 2:
            skin = spawn(small_pelt, location=caller)
            string = "You skin the remains and produce a fur pelt."
            string_r = "%s skins %s and produces a fur pelt." % (caller.name, target.name)
        if d3 == 3:
            skin = spawn(fine_fur_pelt, location=caller)
            string = "You skin the remains and produce a fine fur pelt."
            string_r = "%s skins %s and produces a fine fur pelt." % (caller.name, target.name)

        caller.msg(string)
        caller.location.msg_contents(string_r,
                                     exclude=caller)

        destination = caller.search("#1731", global_search=True)
        target.move_to(destination, quiet=True)

class CmdWield(Command):
    """
    Wields a weapons that you have in your inventory.

    Usage:
      wield <weapon>

    Examples:
      wield pitchfork

    What weapons you are wielding can be checked via the |wwielded|n command, other's weapons can be seen via
    the |wassess|n command.
    """

    key = "wield"
    aliases = ["draw", "unsheathe"]
    help_category = "Equipment"

    def parse(self):
        "Very trivial parser"
        self.args = self.args.strip()

    def func(self):
        """
        This performs the actual command.
        """

        caller = self.caller

        if not self.args:
            caller.msg("Usage: |wwield|n <weapon>")
            return
        #weapon = caller.search(self.arglist[0], candidates=caller.contents) # His string slice was wrong in the case of weapons with longer names.  It should do everything but the last list item.
        weapon = caller.search(self.args, candidates=caller.contents)
        #weaponstyle = False

        if not weapon:
            caller.msg("Wield what?")
            return
        # if not utils.inherits_from(weapon, "typeclasses.arms.Weapon"):
        #     caller.msg("That's not a weapon.")
        #     return

        if Command.show_balance(self): # Checks balance, stops if you don't have it.
            return

        if weapon.name in caller.db.wielding:
            caller.msg("You are already wielding %s." % weapon)
            return
        elif caller.db.wielding:
            caller.msg("You are already wielding %s." % caller.db.wielding[0])
            return
        elif weapon not in caller.db.girdle:
            caller.msg("%s is bundled up in your inventory.\nYou must |wsecure|n it to a sheath in your weapon girdle before you can wield it." % str.capitalize(str(weapon.name)))
        else:
            caller.db.wielding.append(weapon)
            caller.msg("You draw %s from a sheath in your weapon girdle." % weapon.name)
            caller.location.msg_contents("%s draws %s from a sheath in %s weapon girdle." %
                                                 (caller.name,
                                                  weapon.name,
                                                  caller.db.genderp),
                                                 exclude=caller)
            caller.db.balance_time = time.time() + 1
            return

class CmdUnwield(Command):
    """
    Stops wielding a weapon and stores it in your inventory.  You might want to wear or sheath it afterwards it it has those abilities.

    Usage:
      unwield <weapon>

    Examples:
      unwield pitchfork
      
    """

    key = "unwield"
    aliases = ["sheathe"]
    help_category = "Equipment"

    def parse(self):
        "Very trivial parser"
        self.args = self.args.strip()

    def func(self):
        """
        This performs the actual command.
        """
        if not self.args:
            self.caller.msg("Usage: |wunwield|n <weapon>")
            return

        caller = self.caller

        #weapon = self.caller.search(self.arglist[0], candidates=self.caller.contents) # String slice wrong again.
        weapon = caller.search(self.args, candidates=caller.contents) #was caller.contents

        if not weapon:
            caller.msg("Unwield what?")
            return

        if Command.show_balance(self): # Checks balance, stops if you don't have it.
            return

        if weapon not in caller.db.wielding:
            caller.msg("You aren't wielding %s." % weapon)
            return
        else:
            caller.db.wielding = []
            caller.db.stance = "no stance"
            caller.msg("You sheathe %s into your weapon girdle." % weapon.name)
            caller.location.msg_contents("%s sheaths %s into %s weapon girdle." %
                                                 (caller.name,
                                                  weapon.name,
                                                  caller.db.genderp),
                                                 exclude=caller)
            caller.db.balance_time = time.time() + 1.5
            return

class CmdSecure(BaseCommand):
    """
    Sheathe a weapon in your weapon girdle, allowing you to easily |wwield|n it in combat at a later time.

    Usage:
      sheathe <weapon>

    Note that you cannot |wwield|n a weapon for combat unless it has been |wsheathe|nd or otherwise |wsecure|nd to your weapon girdle.
    It is possible to carry extra weapons but they will be bundled up in your inventory in such a way that they are harmless.
    """

    key = "secure"
    aliases = ["attach"]
    help_category = "Equipment"

    def parse(self):
        "Very trivial parser"
        self.args = self.args.strip()

    def func(self):
        """
        This performs the actual command.
        """

        caller = self.caller

        if not self.args:
            caller.msg("Usage: |wsheathe|n <weapon>")
            return
        #weapon = caller.search(self.arglist[0], candidates=caller.contents) # His string slice was wrong in the case of weapons with longer names.  It should do everything but the last list item.
        weapon = caller.search(self.args, candidates=caller.contents)
        #weaponstyle = False

        if not weapon:
            caller.msg("Sheathe what?")
            return
        if not utils.inherits_from(weapon, "typeclasses.arms.Weapons"):
            caller.msg("That's not a weapon.")
            return
        if not "girdle" in caller.db.wearing:
            caller.msg("You aren't wearing a suitable weapon girdle.")
            return

        if Command.show_balance(self): # Checks balance, stops if you don't have it.
            return

        if weapon.db.birth_time:
            if weapon.db.birth_time + weapon.db.duration < time.time():
                caller.msg("%s crumbles to dust when you touch it! Just how old was that thing?" % str.capitalize(str(weapon.name)))
                weapon.delete()
                return

        if weapon in caller.db.girdle:
            caller.msg("This is already sheathed in your girdle.")
            return
        elif len(caller.db.girdle) > 1:
            caller.msg("Your girdle is full and cannot support any more weapons!")
            return
        elif len(caller.db.girdle) < 2:
            caller.db.girdle.append(weapon)
            caller.msg("You arrange it so that %s can be sheathed to your weapon girdle." % weapon.name)
            caller.location.msg_contents("%s arranges %s equipment so that %s can be sheathed to %s weapon girdle." %
                                                 (caller.name, caller.db.genderp,
                                                  weapon.name,
                                                  caller.db.genderp),
                                                 exclude=caller)
            caller.db.balance_time = time.time() + 3.5
            return

class CmdDetach(BaseCommand):
    """
    Disconnect a weapon from its associated moorings on your weapon girdle.

    Usage:
      detach <weapon>

    Note that you cannot |wwield|n a weapon for combat unless it has been |wsheathe|nd or otherwise |wsecure|nd to your weapon girdle.
    It is possible to carry extra weapons but they will be bundled up in your inventory in such a way that they are harmless.
    """

    key = "detach"
    aliases = ["unsecure"]
    help_category = "Equipment"

    def parse(self):
        "Very trivial parser"
        self.args = self.args.strip()

    def func(self):
        """
        This performs the actual command.
        """

        caller = self.caller

        if not self.args:
            caller.msg("Usage: |wdetach|n <weapon>")
            return
        #weapon = caller.search(self.arglist[0], candidates=caller.contents) # His string slice was wrong in the case of weapons with longer names.  It should do everything but the last list item.
        weapon = caller.search(self.args, candidates=caller.contents)
        #weaponstyle = False

        if not weapon:
            caller.msg("Detach what?")
            return

        if weapon in caller.db.wielding:
            caller.msg("You have to stop wielding %s first." % weapon)
            return

        if Command.show_balance(self): # Checks balance, stops if you don't have it.
            return

        if weapon not in caller.db.girdle:
            caller.msg("That is not attached to your girdle.")
            return
        elif weapon in caller.db.girdle:
            caller.db.girdle.remove(weapon)
            caller.msg("You detach the sheath for %s from your weapon girdle." % weapon.name)
            caller.location.msg_contents("%s detaches the sheath for %s from %s weapon girdle." %
                                                 (caller.name, weapon.name, caller.db.genderp),
                                                 exclude=caller)
            caller.db.balance_time = time.time() + 4.5

        if weapon.db.birth_time:
            if weapon.db.birth_time + weapon.db.duration < time.time():
                caller.msg("%s crumbles to dust when you touch it! Just how old was that thing?" % str.capitalize(str(weapon.name)))
                weapon.delete()
                return

class CmdWear(BaseCommand):
    """
    Wear clothing or armor that you are holding.

    Usage:
      wear <item>

    Examples:
      wear leather

    """

    key = "wear"
    help_category = "equipment"

    def parse(self):
        "Very trivial parser"
        self.args = self.args.strip()

    def func(self):
        """
        This performs the actual command.
        """

        caller = self.caller

        if not self.args:
            caller.msg("Usage: wear <obj> [position]")
            return

        clothing = caller.search(self.args, candidates=caller.contents)

        if not clothing:
            caller.msg("Wear what?")
            return

        if not clothing.is_typeclass("typeclasses.clothing.Clothes"):
            caller.msg("Nice try but those aren't clothes!")
            return

        if clothing.db.type in caller.db.wearing:
            caller.msg("You are already wearing something similar.")
            return

        if clothing.db.birth_time:
            if clothing.db.birth_time + clothing.db.duration < time.time():
                caller.msg("%s crumbles to dust when you touch it! Just how old was that thing?" % str.capitalize(str(clothing.name)))
                clothing.delete()
                return

        if clothing.name in caller.db.clothes_objects:
            caller.msg("You are already wearing %s!" % clothing)
            return
        else:
            caller.db.wearing.append(str(clothing.db.type))
            caller.db.clothes_objects.append(clothing)
            caller.db.shown_clothes.append(str(clothing.name))
            caller.msg(clothing.db.wear_msg)
        # else:
        #     caller.db.wearing.append(str(clothing.db.type)) # Appends to the types list
        #     caller.msg(clothing.db.wear_msg)
        #     if clothing.name not in caller.db.shown_clothes:
        #         caller.db.shown_clothes.append(str(clothing.name)) # Appends to the displayed list

        if clothing.db.wear_msg_room_2:
            caller.location.msg_contents("%s %s %s %s" % (caller.name, clothing.db.wear_msg_room_1, caller.db.genderp, clothing.db.wear_msg_room_2), exclude=caller)
        elif clothing.db.wear_msg_room_1:
            caller.location.msg_contents("%s %s" % (caller.name, clothing.db.wear_msg_room_1),
                                         exclude=caller)
        else:
            caller.location.msg_contents("%s wears %s." % (caller.name, clothing.name), exclude=caller)

        # for k, v in caller.db.wearing.iteritems():
        #     for c in clothing.db.coverage:
        #         if k == c:
        #             if v != "naked":
        #                 caller.msg("You are already wearing something on your %s." % k)
        #                 return
        #             else:
        #                 caller.db.wearing[k] = str(clothing.name)

        if clothing.db.armor_value:
            caller.db.armor_bonus = clothing.db.armor_value

class CmdRemove(BaseCommand):
    """
    Removes clothing or armor that you are wearing.

    Usage:
      remove <item>

    Examples:
      remove leather

    """

    key = "remove"
    help_category = "Equipment"

    def parse(self):
        "Very trivial parser"
        self.args = self.args.strip()

    def func(self):
        """
        This performs the actual command.
        """

        caller = self.caller

        if not self.args:
            caller.msg("Usage: remove <item>")
            return

        clothing = caller.search(self.args, candidates=caller.contents)

        if not clothing:
            caller.msg("Remove what?")
            return

        # if not clothing.is_typeclass("typeclasses.clothing.Clothes"):
        #     caller.msg("Nice try but those aren't clothes!")
        #     return
        if clothing.db.type == "girdle" and caller.db.girdle:
            caller.msg("You can't remove the girdle while it contains weapons.")
            return

        if clothing not in caller.db.clothes_objects:
            caller.msg("You are not wearing %s" % clothing)
            return
        else:
            caller.db.wearing.remove(str(clothing.db.type))
            caller.db.clothes_objects.remove(clothing)
            caller.db.shown_clothes.remove(str(clothing.name))

            caller.msg("You slip out of %s." % clothing.name)
            caller.location.msg_contents("%s slips out of %s." % (caller.name, clothing.name), exclude=caller)

        # if clothing.db.type not in caller.db.wearing:
        #     caller.msg("You are not wearing %s." % clothing)
        #     return
        # else:
        #     caller.db.wearing.remove(str(clothing.db.type))
        #     caller.msg("You slip out of %s." % clothing.name)
        #     caller.location.msg_contents("%s slips out of %s." % (caller.name, clothing.name), exclude=caller)
        #     if clothing.name in caller.db.shown_clothes:
        #         caller.db.shown_clothes.remove(str(clothing.name))  # Appends to the displayed list

        # was_worn = False
        #
        # for k, v in caller.db.wearing.iteritems():
        #     for c in clothing.db.coverage:
        #         if k == c and v != "naked":
        #             caller.db.wearing[k] = "naked"
        #             was_worn = clothing.name
        #
        # if not was_worn:
        #     caller.msg("You aren't wearing that!")
        # else:
        #     caller.msg("You remove %s." % was_worn)

        if clothing.db.armor_value:
            caller.db.armor_bonus = caller.db.armor_bonus - clothing.db.armor_value

        if clothing.db.birth_time:
            if clothing.db.birth_time + clothing.db.duration < time.time():
                caller.msg("%s crumbles to dust when you touch it! Just how old was that thing?" % str.capitalize(str(clothing.name)))
                clothing.delete()
                return
        
class CmdInventory(Command):
    """
    View your current inventory.

    You can also use wielded to show you only what items, if any you are wielding.

    Usage:
      inventory

    Shows your inventory.
    """
    # Alternate version of the inventory command which separates
    # worn,carried, and wielded items.

    key = "inventory"
    help_category = "Equipment"
    aliases = ["inv"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""

        caller = self.caller

        if not caller.contents:
            caller.msg("You are not carrying or wearing anything!")
            return

        if caller.db.wielding:
            caller.msg("|wYou are wielding %s.|n" % caller.db.wielding[0])

        if caller.db.shown_clothes:
            caller.msg("|cYou are wearing %s.|n" % english_utils.iart_list(caller.db.shown_clothes))
        else:
            caller.msg("You're naked...")

        if caller.db.girdle:
            caller.msg("|gYou have sheaths for the following weapons attached to your girdle:|n %s." % english_utils.iart_list(caller.db.girdle))

        carried_inventory = []
        exceptions = []

        for i in caller.contents:
            carried_inventory.append(str(i))
            if str(i) in caller.db.shown_clothes or i in caller.db.girdle:
                    exceptions.append(str(i))

        exceptions = list(set(exceptions))

        for i in exceptions:
            if i in carried_inventory:
                carried_inventory.remove(i)

        if carried_inventory:
            caller.msg("You are carrying %s." % english_utils.iart_list(carried_inventory))

        if caller.db.silver_carried > 0:
            if caller.db.silver_carried == 1:
                string = "You are carrying a single silver sovereign."
            else:
                string = "You are carrying {:,} silver sovereigns.".format(caller.db.silver_carried)
            caller.msg(string)
            #caller.msg("You have %s silver sovereigns." % caller.db.silver_carried)
        else:
            caller.msg("You aren't carrying any money.")

# -------------------------------------------------------------
#
# The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this copy of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
# -------------------------------------------------------------

from evennia.utils import utils


class MuxCommand(Command):
    """
    This sets up the basis for a MUX command. The idea
    is that most other Mux-related commands should just
    inherit from this and don't have to implement much
    parsing of their own unless they do something particularly
    advanced.

    Note that the class's __doc__ string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.
    """
    def has_perm(self, srcobj):
        """
        This is called by the cmdhandler to determine
        if srcobj is allowed to execute this command.
        We just show it here for completeness - we
        are satisfied using the default check in Command.
        """
        return super(MuxCommand, self).has_perm(srcobj)

    def at_pre_cmd(self):
        """
        This hook is called before self.parse() on all commands
        """
        pass

    def at_post_cmd(self):
        """
        This hook is called after the command has finished executing
        (after self.func()).
        """
        caller = self.caller

        if caller.db.health != None:
            if (float(caller.db.health) / float(caller.db.max_health)) > 0.80:
                prompt_hp_color = "|g"
            elif (float(caller.db.health) / float(caller.db.max_health)) > 0.36:
                prompt_hp_color = "|y"
            else:
                prompt_hp_color = "|r"

            if caller.db.stamina > 6:
                prompt_stamina_color = "|g"
            elif caller.db.stamina > 3:
                prompt_stamina_color = "|y"
            else:
                prompt_stamina_color = "|r"

            magic_level = "Asleep"
            if caller.db.current_magic == 0:
                magic_level = "Asleep"
            elif caller.db.current_magic > 7:
                magic_level = "|rRaging|n"
            elif caller.db.current_magic > 4:
                magic_level = "|yIrate|n"
            elif caller.db.current_magic > 0:
                magic_level = "|gAwoken|n"

            prompt = "%sHealth|n: %s%s|n - |gMagic|n: %s|n - %sStamina|n: %s%s." % (
            prompt_hp_color, prompt_hp_color, caller.db.health, magic_level, prompt_stamina_color, prompt_stamina_color,
            caller.db.stamina)

            caller.msg(prompt)

    def parse(self):
        """
        This method is called by the cmdhandler once the command name
        has been identified. It creates a new set of member variables
        that can be later accessed from self.func() (see below)

        The following variables are available for our use when entering this
        method (from the command definition, and assigned on the fly by the
        cmdhandler):
           self.key - the name of this command ('look')
           self.aliases - the aliases of this cmd ('l')
           self.permissions - permission string for this command
           self.help_category - overall category of command

           self.caller - the object calling this command
           self.cmdstring - the actual command name used to call this
                            (this allows you to know which alias was used,
                             for example)
           self.args - the raw input; everything following self.cmdstring.
           self.cmdset - the cmdset from which this command was picked. Not
                         often used (useful for commands like 'help' or to
                         list all available commands etc)
           self.obj - the object on which this command was defined. It is often
                         the same as self.caller.

        A MUX command has the following possible syntax:

          name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]

        The 'name[ with several words]' part is already dealt with by the
        cmdhandler at this point, and stored in self.cmdname (we don't use
        it here). The rest of the command is stored in self.args, which can
        start with the switch indicator /.

        This parser breaks self.args into its constituents and stores them in the
        following variables:
          self.switches = [list of /switches (without the /)]
          self.raw = This is the raw argument input, including switches
          self.args = This is re-defined to be everything *except* the switches
          self.lhs = Everything to the left of = (lhs:'left-hand side'). If
                     no = is found, this is identical to self.args.
          self.rhs: Everything to the right of = (rhs:'right-hand side').
                    If no '=' is found, this is None.
          self.lhslist - [self.lhs split into a list by comma]
          self.rhslist - [list of self.rhs split into a list by comma]
          self.arglist = [list of space-separated args (stripped, including '=' if it exists)]

          All args and list members are stripped of excess whitespace around the
          strings, but case is preserved.
        """
        raw = self.args
        args = raw.strip()

        # split out switches
        switches = []
        if args and len(args) > 1 and args[0] == "/":
            # we have a switch, or a set of switches. These end with a space.
            switches = args[1:].split(None, 1)
            if len(switches) > 1:
                switches, args = switches
                switches = switches.split('/')
            else:
                args = ""
                switches = switches[0].split('/')
        arglist = [arg.strip() for arg in args.split()]

        # check for arg1, arg2, ... = argA, argB, ... constructs
        lhs, rhs = args, None
        lhslist, rhslist = [arg.strip() for arg in args.split('//')], [] #WHN: Attempting to change these splitters from a comma (',') to double slashes ('//')
        if args and '=' in args:
            lhs, rhs = [arg.strip() for arg in args.split('=', 1)]
            lhslist = [arg.strip() for arg in lhs.split('//')]
            rhslist = [arg.strip() for arg in rhs.split('//')]

        # save to object properties:
        self.raw = raw
        self.switches = switches
        self.args = args.strip()
        self.arglist = arglist
        self.lhs = lhs
        self.lhslist = lhslist
        self.rhs = rhs
        self.rhslist = rhslist

        # if the class has the player_caller property set on itself, we make
        # sure that self.caller is always the player if possible. We also create
        # a special property "character" for the puppeted object, if any. This
        # is convenient for commands defined on the Player only.
        if hasattr(self, "player_caller") and self.player_caller:
            if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
                # caller is an Object/Character
                self.character = self.caller
                self.caller = self.caller.player
            elif utils.inherits_from(self.caller, "evennia.players.players.DefaultPlayer"):
                # caller was already a Player
                self.character = self.caller.get_puppet(self.session)
            else:
                self.character = None

# WHN: Adding stuff from here on.

class CharGenSelect(Command):
    """
    Set a character attribute.

    Usage:
      select <1-5>

    """

    key = "select"
    help_category = "Character Generation"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        caller = self.caller

        "This performs the actual command"
        errmsg = "Syntax error; |wlook|n to display the options again."
        selected = self.target
        selected = str(selected)
        selected = str.lower(selected)

        ############
        # Starting equipment dictionaries.
        ############

        male_newbie_armor = {"key": "some scuffed leather armor with an overly high and tight neck",
                             "typeclass": "typeclasses.clothing.Clothes",
                             "aliases": ["armour"],
                             "desc": "This suit of armor looks sturdy enough but it was either made for a very strangely proportioned person or some error happened during its fabrication.  This is clear because the neck is strangely small and too tall.",
                             "wear_msg": "You squeeze into a scuffed suit of leather armor.",
                             "wear_msg_room_1": "squeezes into a scuffed suit of leather armor.",  # name
                             "type": "armor",
                             "armor_value": 8,
                             "armor_type": "leather",
                             "location": caller,
                             "birth_time": time.time(),
                             "duration": 2000000.0}

        female_newbie_armor = {"key": "some revealing leather armor that doesn't protect very much",
                               "typeclass": "typeclasses.clothing.Clothes",
                               "aliases": ["armour"],
                               "desc": "This suit of armor looks like it was made as a joke, or perhaps by someone who didn't intend to use it in a fight. Most of the chest and back are fully exposed and it doesn't cover the legs at all.",
                               "wear_msg": "You squeeze into a revealing suit of leather \"armor.\"",
                               "wear_msg_room_1": "squeezes into a scuffed suit of leather \"armor.\"",  # name
                               "type": "armor",
                               "armor_value": 8,
                               "armor_type": "leather",
                               "location": caller,
                               "birth_time": time.time(),
                               "duration": 2000000.0}

        grandmas_newbie_armor = {"key": "grandma's old leather armor",
                                 "typeclass": "typeclasses.clothing.Clothes",
                                 "aliases": ["armour"],
                                 "desc": "This ancient suit of leather armor is about the right size for a female dwarf. The coverage provided and workmanship are good but the item's age is showing.",
                                 "wear_msg": "You squeeze into an ancient suit of leather armor.",
                                 "wear_msg_room_1": "squeezes into an ancient suit of leather armor.",  # name
                                 "type": "armor",
                                 "armor_value": 8,
                                 "armor_type": "leather",
                                 "location": caller,
                                 "birth_time": time.time(),
                                 "duration": 2000000.0}

        grandpas_newbie_armor = {"key": "grandpa's old leather armor",
                                 "typeclass": "typeclasses.clothing.Clothes",
                                 "aliases": ["armour"],
                                 "desc": "This ancient suit of leather armor is about the right size for a male dwarf. The coverage provided and workmanship are good but the item's age is showing.",
                                 "wear_msg": "You squeeze into an ancient suit of leather armor.",
                                 "wear_msg_room_1": "squeezes into an ancient suit of leather armor.",  # name
                                 "type": "armor",
                                 "armor_value": 8,
                                 "armor_type": "leather",
                                 "birth_time": time.time(),
                                 "location": caller,
                                 "duration": 2000000.0}

        black_hoodie = {"key": "a long hooded black cloak",
                        "typeclass": "typeclasses.clothing.Clothes",
                        "aliases": ["hoodie"],
                        "desc": "This long black hoodie cloak looks dramatic, so dramatic.",
                        "wear_msg": "You sweep a hooded black cloak over your shoulders.",
                        "wear_msg_room_1": "sweeps a hooded black cloak over",  # name
                        "wear_msg_room_2": "shoulders.",  # his or her
                        "type": "cloak",
                        "location": caller,
                        "birth_time": time.time(),
                        "duration": 2000000.0}

        leaf_hoodie = {"key": "a woven green and grey, leaf-patterned cloak",
                       "typeclass": "typeclasses.clothing.Clothes",
                       "aliases": ["hoodie"],
                       "desc": "This woven green and grey cloak shows exceptional workmanship in its patterned leaves.",
                       "wear_msg": "You sweep a woven green and grey, leaf-patterned cloak over your shoulders.",
                       "wear_msg_room_1": "sweeps a woven green and grey, leaf-patterned cloak over",
                       "wear_msg_room_2": "shoulders.",
                       "type": "cloak",
                       "location": caller,
                       "birth_time": time.time(),
                       "duration": 2000000.0}

        riding_hoodie = {"key": "a hooded red riding cloak",
                         "typeclass": "typeclasses.clothing.Clothes",
                         "aliases": ["hoodie"],
                         "desc": "This hooded red cloak looks like it has seen the road before.",
                         "wear_msg": "You sweep a hooded red riding cloak over your shoulders.",
                         "wear_msg_room_1": "sweeps a hooded red riding cloak over",
                         "wear_msg_room_2": "shoulders.",
                         "type": "cloak",
                         "location": caller,
                         "birth_time": time.time(),
                         "duration": 2000000.0}

        black_leather_girdle = {"key": "a black leather weapon girdle",
                                "typeclass": "typeclasses.clothing.Clothes",
                                # "aliases" : ["armour"],
                                "desc": "This sturdy girdle acts as a belt, bodily protection and a place to affix sheaths or other kinds of equipment onto the body. It includes some efficient-looking leather suspenders to help support the weight.",
                                "wear_msg": "You strap on a black leather weapon girdle.",
                                "wear_msg_room_1": "straps on a black leather weapon girdle.",  # name
                                "type": "girdle",
                                "location": caller,
                                "birth_time": time.time(),
                                "duration": 2000000.0}

        sturdy_dwarven_girdle = {"key": "a sturdy dwarven weapon girdle",
                                 "typeclass": "typeclasses.clothing.Clothes",
                                 # "aliases" : ["armour"],
                                 "desc": "This sturdy girdle acts as a belt, bodily protection and a place to affix sheaths or other kinds of equipment onto the body. It includes some efficient-looking leather suspenders to help support the weight.",
                                 "wear_msg": "You strap on a sturdy dwarven weapon girdle.",
                                 "wear_msg_room_1": "straps on a sturdy dwarven weapon girdle.",  # name
                                 "type": "girdle",
                                 "location": caller,
                                 "birth_time": time.time(),
                                 "duration": 2000000.0}

        toolbelt_girdle = {"key": "a leather tool belt and weapon girdle",
                           "typeclass": "typeclasses.clothing.Clothes",
                           # "aliases" : ["armour"],
                           "desc": "This sturdy girdle acts as a belt, bodily protection and a place to affix sheaths or other kinds of equipment onto the body. It includes some efficient-looking leather suspenders to help support the weight and pockets for other kinds of tools or supplies.",
                           "wear_msg": "You strap on a leather tool belt and weapon girdle.",
                           "wear_msg_room_1": "straps on a leather tool belt and  weapon girdle.",  # name
                           "type": "girdle",
                           "location": caller,
                           "birth_time": time.time(),
                           "duration": 2000000.0}

        bandolier_girdle = {"key": "a leather bandolier",
                            "typeclass": "typeclasses.clothing.Clothes",
                            "aliases": ["girdle"],
                            "desc": "This sturdy bandolier goes over the shoulder instead of around the waste, but otherwise performs the same purpose that a weapon girdle would, to hold sheaths for weapons.",
                            "wear_msg": "You strap on a leather tool belt and weapon girdle.",
                            "wear_msg_room_1": "straps on a leather tool belt and  weapon girdle.",  # name
                            "type": "girdle",
                            "location": caller,
                            "birth_time": time.time(),
                            "duration": 2000000.0}

        wooden_sandals = {"key": "sturdy wooden sandals",
                          "typeclass": "typeclasses.clothing.Clothes",
                          "aliases": ["shoes"],
                          "desc": "These sturdy wooden sandals make the wearer look a bit taller",
                          "wear_msg": "You don a pair of sturdy wooden sandals.",
                          "wear_msg_room_1": "straps a pair of sturdy wooden sandals to",
                          "wear_msg_room_2": "feet.",
                          "type": "shoes",
                          "location": caller,
                          "birth_time": time.time(),
                          "duration": 2000000.0}

        laced_boots = {"key": "laced up leather boots",
                       "typeclass": "typeclasses.clothing.Clothes",
                       "aliases": ["shoes"],
                       "desc": "These leather boots have a lot of laces for a firm grip.",
                       "wear_msg": "You lace up a pair of leather boots.",
                       "wear_msg_room_1": "laces up a pair of leather boots.",
                       "type": "shoes",
                       "location": caller,
                       "birth_time": time.time(),
                       "duration": 2000000.0}

        grey_trousers = {"key": "plain grey woolen trousers",
                         "typeclass": "typeclasses.clothing.Clothes",
                         "aliases": ["pants"],
                         "desc": "These grey woolen trousers look sturdy and warm.",
                         "wear_msg": "You pull on a pair of plain grey woolen trousers.",
                         "wear_msg_room_1": "pulls on a pair of plain grey woolen trousers.",
                         "type": "pants",
                         "location": caller,
                         "birth_time": time.time(),
                         "duration": 2000000.0}

        cold_iron_axe = {"key": "a cold iron axe",
                         "typeclass": "typeclasses.arms.Weapons",
                         "aliases": ["weapon"],
                         "short_name": "iron axe",
                         "desc": "This heavy axe is made from cold iron, making it affordable if somewhat heavy.\nThis weapon has the following attributes:\nOpen Terrain: +5, Cluttered Terrain: 0, Narrow Terrain: -5.\nBalance: Heavy.\nDamage: High.",
                         "open_terrain": 5,
                         "cluttered_terrain": 0,
                         "narrow_terrain": -5,
                         "damage_multiplier": 1.15,
                         "balance_duration_change": 0.5,
                         "weapon_type": "1haxe",
                         "location": caller,
                         "birth_time": time.time(),
                         "duration": 2000000.0}

        hunters_spear = {"key": "a long hunter's spear",
                         "typeclass": "typeclasses.arms.Weapons",
                         "aliases": ["weapon"],
                         "short_name": "hunter's spear",
                         "desc": "This light spear has a sharp steel tip, as well as a leather strap for being secured when carrying and a leather cover for the head.\nThis weapon has the following attributes:\nOpen Terrain: 0, Cluttered Terrain: 0, Narrow Terrain: +10.\nBalance: Light.\nDamage: Low.",
                         "open_terrain": 0,
                         "cluttered_terrain": 0,
                         "narrow_terrain": 10,
                         "damage_multiplier": 0.85,
                         "balance_duration_change": -1,
                         "weapon_type": "1hspear",
                         "location": caller,
                         "birth_time": time.time(),
                         "duration": 2000000.0}

        steel_gladius = {"key": "a sturdy steel gladius",
                         "typeclass": "typeclasses.arms.Weapons",
                         "aliases": ["sword", "weapon"],
                         "short_name": "steel gladius",
                         "desc": "This short sword is good for both stabbing and slashing. It is made from reliable steel and has leather wrapped about the handle above a round pomel.\nThis weapon has the following attributes:\nOpen Terrain: +3, Cluttered Terrain: +2, Narrow Terrain: 0.\nBalance: Neutral.\nDamage: Average.",
                         "open_terrain": 3,
                         "cluttered_terrain": 2,
                         "narrow_terrain": 0,
                         "damage_multiplier": 1.0,
                         "balance_duration_change": 0.0,
                         "weapon_type": "1hsword",
                         "location": caller,
                         "birth_time": time.time(),
                         "duration": 2000000.0}

        bronze_broadsword = {"key": "a ruddy bronze broadsword",
                             "typeclass": "typeclasses.arms.Weapons",
                             "aliases": ["sword", "weapon"],
                             "short_name": "ruddy bronze broadsword",
                             "desc": "This sharp, thick broadsword is made from fine, if expensive bronze.\nThis weapon has the following attributes:\nOpen Terrain: +3, Cluttered Terrain: +2, Narrow Terrain: 0.\nBalance: Neutral.\nDamage: Average.",
                             "open_terrain": 3,
                             "cluttered_terrain": 2,
                             "narrow_terrain": 0,
                             "damage_multiplier": 1.0,
                             "balance_duration_change": 0.0,
                             "weapon_type": "1hsword",
                             "location": caller,
                             "birth_time": time.time(),
                             "duration": 2000000.0}

        #################################
        ## Race selection starts here. ##
        #################################

        if caller.location.tags.get('race_selection_room'):
            if selected == "1" or selected == "human" or selected == "humans":
                caller.db.race = "human"
                caller.msg("You are now a part of the Human race!")
                caller.db.citizenship = "Corinth"

                # channel = ChannelDB.objects.get_channel("Corinth")
                # #channel.connect(caller)
                # channel.unmute(caller)
                channel = find_channel(caller, "Corinth")
                channel.connect(caller)

                channel = find_channel(caller, "Newbie")
                channel.connect(caller)

                channel = find_channel(caller, "Rage")
                channel.connect(caller)

                channel = find_channel(caller, "OOC")
                channel.connect(caller)

                wpn = spawn(bronze_broadsword, location=caller)
                item = spawn(black_hoodie, location=caller)
                item = spawn(black_leather_girdle, location=caller)
                item = spawn(laced_boots, location=caller)
                item = spawn(grey_trousers, location=caller)
            elif selected == "2" or selected == "dwarf" or selected == "dwarves" or selected == "dwarfs":
                caller.db.race = "dwarf"
                caller.msg("You are now a part of the proud Dwarf race!")
                caller.db.citizenship = "Corinth"

                channel = find_channel(caller, "Corinth")
                channel.connect(caller)

                channel = find_channel(caller, "Newbie")
                channel.connect(caller)

                channel = find_channel(caller, "Rage")
                channel.connect(caller)

                channel = find_channel(caller, "OOC")
                channel.connect(caller)

                wpn = spawn(cold_iron_axe, location=caller)
                item = spawn(riding_hoodie, location=caller)
                item = spawn(sturdy_dwarven_girdle, location=caller)
                item = spawn(laced_boots, location=caller)
                item = spawn(grey_trousers, location=caller)
            elif selected == "3" or selected == "otherkin" or selected == "kin" or selected == "otherkins":
                caller.db.race = "otherkin"
                caller.msg("You are now a part of the Otherkin race!")
                caller.db.citizenship = "Corinth"

                channel = find_channel(caller, "Corinth")
                channel.connect(caller)

                channel = find_channel(caller, "Newbie")
                channel.connect(caller)

                channel = find_channel(caller, "Rage")
                channel.connect(caller)

                channel = find_channel(caller, "OOC")
                channel.connect(caller)

                wpn = spawn(hunters_spear, location=caller)
                item = spawn(leaf_hoodie, location=caller)
                item = spawn(toolbelt_girdle, location=caller)
                item = spawn(wooden_sandals, location=caller)
                item = spawn(grey_trousers, location=caller)
            elif selected == "4" or selected == "elf" or selected == "elves" or selected == "elven":
                caller.db.race = "elf"
                caller.msg("You are now a part of the Elven race!")
                wpn = spawn(steel_gladius, location=caller)
                item = spawn(leaf_hoodie, location=caller)
                item = spawn(bandolier_girdle, location=caller)
                item = spawn(laced_boots, location=caller)
                item = spawn(grey_trousers, location=caller)
            # elif selected == "5" or selected == "undead":
            #     caller.db.race = "undead"
            #     caller.msg("You are now part of the Vulk.")
            #     caller.db.citizenship = "Vulkyragh"
            else:
                caller.msg(errmsg)
                return

        if caller.location.tags.get('gender_selection_room'):
            if selected == "1" or selected == "male":
                caller.db.gender = "male"
                caller.db.genders = "he"
                caller.db.gendero = "him"
                caller.db.genderp = "his"
                caller.db.genderl = "himself"
                caller.msg("You are now male.")

                if caller.db.race == "dwarf":
                    item = spawn(grandpas_newbie_armor, location=caller)
                else:
                    item = spawn(male_newbie_armor, location=caller)

            elif selected == "2" or selected == "female":
                caller.db.gender = "female"
                caller.db.genders = "she"
                caller.db.gendero = "her"
                caller.db.genderp = "her"
                caller.db.genderl = "herself"
                caller.msg("You are now female.")

                if caller.db.race == "dwarf":
                    item = spawn(grandmas_newbie_armor, location=caller)
                else:
                    item = spawn(female_newbie_armor, location=caller)

            else:
                caller.msg(errmsg)
                return

        if caller.location.tags.get('physique_selection_room'):
            if selected == "1" or selected == "corinthian" or selected == "corinth":
                caller.db.physique = "Corinthian"
                caller.db.base_strength = 10
                caller.db.strength = 10
                caller.db.current_strength = 10

                caller.db.base_strength = 10
                caller.db.agility = 10
                caller.db.base_agility = 10

                caller.db.base_strength = 10
                caller.db.constitution = 10
                caller.db.base_constitution = 10

                caller.db.endurance = 10

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10
                caller.db.magic = 10

                caller.msg("You are now part of the Corinthian people.")

            elif selected == "2" or selected == "khitani" or selected == "khitan":
                caller.db.physique = "Khitani"
                caller.db.base_strength = 9
                caller.db.strength = 9
                caller.db.current_strength = 9

                caller.db.base_agility = 12
                caller.db.agility = 12
                caller.db.current_agility = 12

                caller.db.base_constitution = 9
                caller.db.constitution = 9
                caller.db.current_constitution = 9

                caller.db.endurance = 10

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10
                caller.db.magic = 10

                caller.msg("You are now part of the Khitani people.")

            elif selected == "3" or selected == "cimmerian" or selected == "cimmeria":
                caller.db.physique = "Cimmerian"

                caller.db.base_strength = 12
                caller.db.current_strength = 12
                caller.db.strength = 12

                caller.db.base_agility = 8
                caller.db.current_agility = 8
                caller.db.agility = 8

                caller.db.base_constitution = 11
                caller.db.current_constitution = 11
                caller.db.constitution = 11

                caller.db.endurance = 9

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10
                caller.db.magic = 10

                caller.msg("You are now part of the Cimmerian people.")

            elif selected == "4" or selected == "shemitish" or selected == "shem":
                caller.db.physique = "Shemitish"

                caller.db.base_strength = 11
                caller.db.current_agility = 7
                caller.db.strength = 11

                caller.db.base_agility =7
                caller.db.current_agility =7
                caller.db.agility = 7

                caller.db.base_constitution = 14
                caller.db.current_constitution = 14
                caller.db.constitution = 14

                caller.db.endurance = 8

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 10

                caller.msg("You are now part of the Shemitish people.")

            elif selected == "5" or selected == "hyrkanian" or selected == "hyrkania":
                caller.db.physique = "Hyrkanian"

                caller.db.base_strength = 8
                caller.db.current_strength = 8
                caller.db.strength = 8

                caller.db.base_agility = 10
                caller.db.current_agility = 10
                caller.db.agility = 10

                caller.db.base_constitution = 9
                caller.db.current_constitution = 9
                caller.db.constitution = 9

                caller.db.endurance = 13

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 10

                caller.msg("You now part of the Hyrkanian people.")

            elif selected == "6" or selected == "Zamoran" or selected == "Zamora":
                caller.db.physique = "Zamoran"

                caller.db.base_strength = 9
                caller.db.current_strength = 9
                caller.db.strength = 9

                caller.db.base_agility = 9
                caller.db.current_agility = 9
                caller.db.agility = 9

                caller.db.base_constitution = 9
                caller.db.current_constitution = 9
                caller.db.constitution = 9

                caller.db.endurance = 9

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10
                caller.db.magic = 14

                caller.msg("You are now part of the Zamoran people.")

            else:
                caller.msg(errmsg)
                return

        if caller.location.tags.get('otherkin_tribe_selection_room'):
            if selected == "1" or selected == "fox":
                caller.db.physique = "fox"

                caller.db.base_strength = 10
                caller.db.current_strength = 10
                caller.db.strength = 10

                caller.db.base_agility = 10
                caller.db.current_agility = 10
                caller.db.agility = 10

                caller.db.base_constitution = 10
                caller.db.current_constitution = 10
                caller.db.constitution = 10

                caller.db.endurance = 10

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 10

                caller.msg("You are now part of the Otherkin Fox tribe.")

            elif selected == "2" or selected == "feline" or selected == "cat":
                caller.db.physique = "feline"

                caller.db.base_strength = 9
                caller.db.current_strength = 9
                caller.db.strength = 9

                caller.db.base_agility = 12
                caller.db.current_agility = 12
                caller.db.agility = 12

                caller.db.base_constitution = 9
                caller.db.current_constitution = 9
                caller.db.constitution = 9

                caller.db.endurance = 10

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 10

                caller.msg("You now part of the Otherkin Feline tribe.")

            elif selected == "3" or selected == "bear" or selected == "usrine":
                caller.db.physique = "bear"

                caller.db.base_strength = 13
                caller.db.current_strength = 13
                caller.db.strength = 13

                caller.db.base_agility = 7
                caller.db.current_agility = 7
                caller.db.agility = 7

                caller.db.base_constitution = 12
                caller.db.current_constitution = 12
                caller.db.constitution = 12


                caller.db.endurance = 9


                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 9

                caller.msg("You are now part of the Otherkin Bear tribe.")

            elif selected == "4" or selected == "centaur" or selected == "horse":
                caller.db.physique = "centaur"

                caller.db.base_strength = 11
                caller.db.current_strength = 11
                caller.db.strength = 11

                caller.db.base_agility = 5
                caller.db.current_agility = 5
                caller.db.agility = 5

                caller.db.base_constitution = 14
                caller.db.current_constitution = 14
                caller.db.constitution = 14

                caller.db.endurance = 11

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 9

                caller.msg("You are now part of the Otherkin Centaur tribe.")

            elif selected == "5" or selected == "rabbit" or selected == "bunny":
                caller.db.physique = "rabbit"

                caller.db.base_strength = 8
                caller.db.current_strength = 8
                caller.db.strength = 8

                caller.db.base_agility = 11
                caller.db.current_agility = 11
                caller.db.agility = 11

                caller.db.base_constitution = 8
                caller.db.current_constitution = 8
                caller.db.constitution = 8

                caller.db.endurance = 12

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 11

                caller.msg("You are now part of the Otherkin Rabbit tribe.")

            elif selected == "6" or selected == "satyr" or selected == "nymph":

                if caller.db.gender == "male":
                    caller.db.physique = "satyr"
                else:
                    caller.db.physique = "nymph"

                caller.db.base_strength = 8
                caller.db.current_strength = 8
                caller.db.strength = 8

                caller.db.base_agility = 10
                caller.db.current_agility = 10
                caller.db.agility = 10

                caller.db.base_constitution = 10
                caller.db.current_constitution = 10
                caller.db.constitution = 10

                caller.db.endurance = 10

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 12

                if caller.db.gender == "male":
                    caller.msg("You are now part of the Otherkin Satyr tribe.")
                else:
                    caller.msg("You are now part of the Otherkin Nymph tribe.")

            else:
                caller.msg(errmsg)
                return

        if caller.location.tags.get('elven_people_selection_room'):
            if selected == "1" or selected == "high elf" or selected == "high elven" or selected == "high elves":
                caller.db.physique = "high"
                caller.db.citizenship = "Corinth"

                channel = find_channel(caller, "Corinth")
                channel.connect(caller)

                channel = find_channel(caller, "Newbie")
                channel.connect(caller)

                channel = find_channel(caller, "Rage")
                channel.connect(caller)

                channel = find_channel(caller, "OOC")
                channel.connect(caller)

                caller.db.base_strength = 7
                caller.db.current_strength = 7
                caller.db.strength = 7

                caller.db.base_agility = 12
                caller.db.current_agility = 12
                caller.db.agility = 12

                caller.db.base_constitution = 8
                caller.db.current_constitution = 8
                caller.db.constitution = 8


                caller.db.endurance = 7

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 16

                caller.msg("You are now part of the high elven people.")

            elif selected == "2" or selected == "wood" or selected == "wood elf" or selected == "wood elves":
                caller.db.physique = "wood"
                caller.db.citizenship = "Corinth"

                channel = find_channel(caller, "Corinth")
                channel.connect(caller)

                channel = find_channel(caller, "Newbie")
                channel.connect(caller)

                channel = find_channel(caller, "Rage")
                channel.connect(caller)

                channel = find_channel(caller, "OOC")
                channel.connect(caller)

                caller.db.base_strength = 8
                caller.db.current_strength = 8
                caller.db.strength = 8

                caller.db.base_agility = 11
                caller.db.current_agility = 11
                caller.db.agility = 11

                caller.db.base_constitution = 9
                caller.db.current_constitution = 9
                caller.db.constitution = 9

                caller.db.endurance = 8

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 14

                caller.msg("You now part of the wood elven people.")

            elif selected == "3" or selected == "half" or selected == "half elf" or selected == "half elven":
                caller.db.physique = "half"
                caller.db.citizenship = "Corinth"

                channel = find_channel(caller, "Corinth")
                channel.connect(caller)

                channel = find_channel(caller, "Newbie")
                channel.connect(caller)

                channel = find_channel(caller, "Rage")
                channel.connect(caller)

                channel = find_channel(caller, "OOC")
                channel.connect(caller)

                caller.db.base_strength = 9
                caller.db.current_strength = 9
                caller.db.strength = 9

                caller.db.base_agility = 10
                caller.db.current_agility = 10
                caller.db.agility = 10

                caller.db.base_constitution = 10
                caller.db.current_constitution = 10
                caller.db.constitution = 10

                caller.db.endurance = 9

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 12

                caller.msg("You are now part of the half elven people.")

            # elif selected == "4" or selected == "dark" or selected == "dark elf" or selected == "dark elves" or selected == "dark elf":
            #     caller.db.physique = "dark"
            #     caller.db.citizenship = "Vulkyragh"
            #
            #     caller.db.base_strength = 9
            #     caller.db.current_strength = 8
            #     caller.db.strength = 8
            #
            #     caller.db.base_agility = 10
            #     caller.db.current_agility = 10
            #     caller.db.agility = 10
            #
            #     caller.db.base_constitution = 8
            #     caller.db.current_constitution = 8
            #     caller.db.constitution = 8
            #
            #     caller.db.endurance = 8
            #
            #     caller.db.health = 100 + caller.db.constitution
            #     caller.db.max_health = 100 + caller.db.constitution
            #
            #     caller.db.stamina = 10
            #
            #     caller.db.magic = 16
            #
            #     caller.msg("You are now part of the dark elven people.")
            else:
                caller.msg(errmsg)
                return

        if caller.location.tags.get('dwarven_people_selection_room'):
            if selected == "1" or selected == "mountain dwarf" or selected == "mountain dwarves":
                caller.db.physique = "mountain"

                caller.db.base_strength = 12
                caller.db.current_strength = 12
                caller.db.strength = 12

                caller.db.base_agility = 6
                caller.db.current_agility = 6
                caller.db.agility = 6

                caller.db.base_constitution = 15
                caller.db.current_constitution = 15
                caller.db.constitution = 15

                caller.db.endurance = 9

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 8

                caller.msg("You are now part of the proud mountain Dwarf people.")

            elif selected == "2" or selected == "urbanized dwarf" or selected == "urbanized" or selected == "urban":
                caller.db.physique = "urbanized"

                caller.db.base_strength = 10
                caller.db.current_strength = 10
                caller.db.strength = 10

                caller.db.base_agility = 8
                caller.db.current_agility = 8
                caller.db.agility = 8

                caller.db.base_constitution = 13
                caller.db.current_constitution = 13
                caller.db.constitution = 13

                caller.db.endurance = 9

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 9

                caller.msg("You now part of the urbanized dwarven people.")

            elif selected == "3" or selected == "countryside dwarf" or selected == "countryside" or selected == "country":
                caller.db.physique = "countryside"

                caller.db.base_strength = 11
                caller.db.current_strength = 11
                caller.db.strength = 11

                caller.db.base_agility = 7
                caller.db.current_agility = 7
                caller.db.agility = 7

                caller.db.base_constitution = 14
                caller.db.current_constitution = 14
                caller.db.constitution = 14

                caller.db.endurance = 9

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 9

                caller.msg("You are now part of the countryside dwarven people.")

            elif selected == "4" or selected == "underdark dwarf" or selected == "underdark" or selected == "dark":
                caller.db.physique = "underdark"

                caller.db.base_strength = 10
                caller.db.current_strength = 10
                caller.db.strength = 10

                caller.db.base_agility = 7
                caller.db.current_agility = 7
                caller.db.agility = 7

                caller.db.base_constitution = 13
                caller.db.current_constitution = 13
                caller.db.constitution = 13

                caller.db.endurance = 8

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 12
                caller.msg("You are now part of the underdark-dwelling dwarven people.")

        if caller.location.tags.get('undead_form_selection_room'):
            if selected == "1" or selected == "ghoul":
                caller.db.physique = "ghoulish"
                caller.db.base_strength = 11
                caller.db.strength = 11
                caller.db.current_strength = 11

                caller.db.base_strength = 11
                caller.db.agility = 11
                caller.db.base_agility = 11

                caller.db.base_strength = 11
                caller.db.constitution = 11
                caller.db.base_constitution = 11

                caller.db.endurance = 10

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10
                caller.db.magic = 7

                caller.msg("You are now an ugly ghoul, have fun!")

            elif selected == "2" or selected == "spectre" or selected == "specter" or selected == "banshee":
                if caller.db.gender == "male":
                    caller.db.physique = "spectral"
                else:
                    caller.db.physique = "spectral"
                    caller.db.gender = "banshee"

                caller.db.base_strength = 7
                caller.db.strength = 7
                caller.db.current_strength = 7

                caller.db.base_agility = 12
                caller.db.agility = 12
                caller.db.current_agility = 12

                caller.db.base_constitution = 9
                caller.db.constitution = 9
                caller.db.current_constitution = 9

                caller.db.endurance = 10

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10
                caller.db.magic = 12

                caller.msg("You now have a spectral form.")

            elif selected == "3" or selected == "ghast" or selected == "ghastly":
                caller.db.physique = "ghastly"

                caller.db.base_strength = 13
                caller.db.current_strength = 13
                caller.db.strength = 13

                caller.db.base_agility = 9
                caller.db.current_agility = 9
                caller.db.agility = 9

                caller.db.base_constitution = 12
                caller.db.current_constitution = 12
                caller.db.constitution = 12

                caller.db.endurance = 9

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10
                caller.db.magic = 8

                caller.msg("You now a raging ghast!")

            elif selected == "4" or selected == "wight":
                caller.db.physique = "pallid"
                caller.db.race = "wight"

                caller.db.base_strength = 8
                caller.db.current_strength = 8
                caller.db.strength = 8

                caller.db.base_agility = 7
                caller.db.current_agility = 7
                caller.db.agility = 7

                caller.db.base_constitution = 12
                caller.db.current_constitution = 12
                caller.db.constitution = 12

                caller.db.endurance = 13

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10

                caller.db.magic = 10

                caller.msg("You are now a tireless wight!")

            elif selected == "5" or selected == "lich":
                caller.db.physique = "dessicated"
                caller.db.race = "lich"

                caller.db.base_strength = 7
                caller.db.current_strength = 7
                caller.db.strength = 7

                caller.db.base_agility = 8
                caller.db.current_agility = 8
                caller.db.agility = 8

                caller.db.base_constitution = 10
                caller.db.current_constitution = 10
                caller.db.constitution = 10

                caller.db.endurance = 9

                caller.db.health = 100 + caller.db.constitution
                caller.db.max_health = 100 + caller.db.constitution

                caller.db.stamina = 10
                caller.db.magic = 16

                caller.msg("You are now a dessicated lich!")

            else:
                caller.msg(errmsg)
                return

        ###########################################################################################################
        # End of sub-race selection code
        ###########################################################################################################

        ###########################################################################################################
        # Room teleportation code
        ###########################################################################################################

        # if char.location.tags.get('raceselectroom', category='chargen'): Do_that_race_chargen_thing()
        if caller.location.tags.get('race_selection_room'): #and race == X
            destination = caller.search("#569", global_search=True)
            #caller.msg(destination)
            caller.move_to(destination, quiet = True)

            for i in caller.contents:
                if i.is_typeclass("typeclasses.clothing.Clothes"):
                    caller.db.wearing.append(str(i.db.type))
                    caller.db.clothes_objects.append(i)
                    caller.db.shown_clothes.append(str(i.name))
                if i.is_typeclass("typeclasses.arms.Weapons"):
                    caller.db.girdle.append(i)

            return

        if caller.location.tags.get('gender_selection_room'):
            """ There's a lot of different rooms they could go to at this point, so this needs to reflect that."""
            if caller.db.race == "human":
                destination = caller.search("#565", global_search=True)
                # caller.msg(destination)
                caller.move_to(destination, quiet = True)
            if caller.db.race == "dwarf":
                destination = caller.search("#568", global_search=True)
                # caller.msg(destination)
                caller.move_to(destination, quiet = True)
            if caller.db.race == "elf":
                destination = caller.search("#567", global_search=True)
                # caller.msg(destination)
                caller.move_to(destination, quiet = True)
            if caller.db.race == "otherkin":
                destination = caller.search("#566", global_search=True)
                # caller.msg(destination)
                caller.move_to(destination, quiet = True)
            if caller.db.race == "undead":
                destination = caller.search("#570", global_search=True)
                # caller.msg(destination)
                caller.move_to(destination, quiet = True)

            for i in caller.contents:
                if i.db.type == "armor":
                    caller.db.wearing.append(str(i.db.type))
                    caller.db.clothes_objects.append(i)
                    caller.db.shown_clothes.append(str(i.name))

            caller.db.armor_bonus = 8

            return

        if caller.location.tags.get('physiqueselectroom'): # or any of the other final rooms
            destination = caller.search("#212", global_search=True)
            #caller.msg(destination)
            caller.msg("After the many trials and travails of your life, you finally find yourself at an inn in Corinth. They say this city will take anyone, recruit anyone, so long as you pledge your loyalty. Members of every race can be found mingling in these streets. This is your chance to start a new life!")
            caller.move_to(destination)
            return