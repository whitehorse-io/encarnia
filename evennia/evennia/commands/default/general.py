"""
General Character commands usually available to all characters
"""
from django.conf import settings
from evennia.utils import utils, evtable
from evennia.typeclasses.attributes import NickTemplateInvalid
import time
from evennia.utils.spawner import spawn

COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)

# limit symbol import for API
__all__ = ("CmdHome", "CmdLook", "CmdNick",
           "CmdInventory", "CmdGet", "CmdDrop", "CmdGive",
           "CmdSay", "CmdWhisper", "CmdPose", "CmdAccess")

class CmdHome(COMMAND_DEFAULT_CLASS): #WHN: For reasons I don't understand, Encarnia explodes if I disable this command... it might be stored somewhere else too.
    """
    Move up to limbo or another divine demesne.

    Usage:
      ascend

    Teleports you to your home location.
    """

    key = "ascend"
    aliases = ["home", "asc"]
    locks = "cmd:perm(home) or perm(Builders)"
    arg_regex = r"$"

    def func(self):
        """Implement the command"""
        caller = self.caller
        home = caller.home
        if not home:
            caller.msg("You have no home!")
        elif home == caller.location:
            caller.msg("You are already home!")
        else:
            caller.msg("There's no place like home ...")
            caller.move_to(home)

class CmdDescend(COMMAND_DEFAULT_CLASS):
    """
    Move down to Encarnia.

    Usage:
      descend

    Teleports you to your home location.
    """

    key = "descend"
    aliases = ["des"]
    locks = "cmd:perm(home) or perm(Builders)"
    arg_regex = r"$"

    def func(self):
        """Implement the command"""
        caller = self.caller
        destination = caller.search("#280", global_search=True)
        caller.msg("You descend from the heavens down towards Encarnia, landing neatly in Ashlan square.")
        caller.move_to(destination)

class CmdLook(COMMAND_DEFAULT_CLASS):
    """
    look at location or object

    Usage:
      look
      look <obj>
      look *<player>

    Observes your location or objects in your vicinity.
    """
    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("You have no location to look at!")
                return
        else:
            target = caller.search(self.args, use_dbref=caller.check_permstring("Builders"))
            if not target:
                return
        self.msg(caller.at_look(target))


class CmdNick(COMMAND_DEFAULT_CLASS):
    """
    define a personal alias/nick

    Usage:
      nick[/switches] <string> [= [replacement_string]]
      nick[/switches] <template> = <replacement_template>
      nick/delete <string> or number
      nick/test <test string>

    Switches:
      inputline - replace on the inputline (default)
      object    - replace on object-lookup
      player    - replace on player-lookup
      delete    - remove nick by name or by index given by /list
      clearall  - clear all nicks
      list      - show all defined aliases (also "nicks" works)
      test      - test input to see what it matches with

    Examples:
      nick hi = say Hello, I'm Sarah!
      nick/object tom = the tall man
      nick build $1 $2 = @create/drop $1;$2     - (template)
      nick tell $1 $2=@page $1=$2               - (template)

    A 'nick' is a personal string replacement. Use $1, $2, ... to catch arguments.
    Put the last $-marker without an ending space to catch all remaining text. You
    can also use unix-glob matching:

        * - matches everything
        ? - matches a single character
        [seq] - matches all chars in sequence
        [!seq] - matches everything not in sequence

    Note that no objects are actually renamed or changed by this command - your nicks
    are only available to you. If you want to permanently add keywords to an object
    for everyone to use, you need build privileges and the @alias command.

    """
    key = "nick"
    aliases = ["nickname", "nicks", "@nick", "@nicks", "alias"]
    locks = "cmd:all()"

    def func(self):
        """Create the nickname"""

        caller = self.caller
        switches = self.switches
        nicktypes = [switch for switch in switches if switch in ("object", "player", "inputline")] or ["inputline"]

        nicklist = utils.make_iter(caller.nicks.get(return_obj=True) or [])

        if 'list' in switches or self.cmdstring in ("nicks", "@nicks"):

            if not nicklist:
                string = "|wNo nicks defined.|n"
            else:
                table = evtable.EvTable("#", "Type", "Nick match", "Replacement")
                for inum, nickobj in enumerate(nicklist):
                    _, _, nickvalue, replacement = nickobj.value
                    table.add_row(str(inum + 1), nickobj.db_category, nickvalue, replacement)
                string = "|wDefined Nicks:|n\n%s" % table
            caller.msg(string)
            return

        if 'clearall' in switches:
            caller.nicks.clear()
            caller.msg("Cleared all nicks.")
            return

        if not self.args or not self.lhs:
            caller.msg("Usage: nick[/switches] nickname = [realname]")
            return

        nickstring = self.lhs
        replstring = self.rhs
        old_nickstring = None
        old_replstring = None

        if replstring == nickstring:
            caller.msg("No point in setting nick same as the string to replace...")
            return

        # check so we have a suitable nick type
        errstring = ""
        string = ""
        for nicktype in nicktypes:
            oldnick = caller.nicks.get(key=nickstring, category=nicktype, return_obj=True)
            if oldnick:
                _, _, old_nickstring, old_replstring = oldnick.value
            else:
                # no old nick, see if a number was given
                arg = self.args.lstrip("#")
                if arg.isdigit():
                    # we are given a index in nicklist
                    delindex = int(arg)
                    if 0 < delindex <= len(nicklist):
                        oldnick = nicklist[delindex-1]
                        _, _, old_nickstring, old_replstring = oldnick.value
                    else:
                        errstring += "Not a valid nick index."
                else:
                    errstring += "Nick not found."
            if "delete" in switches or "del" in switches:
                # clear the nick
                if old_nickstring and caller.nicks.has(old_nickstring, category=nicktype):
                    caller.nicks.remove(old_nickstring, category=nicktype)
                    string += "\nNick removed: '|w%s|n' -> |w%s|n." % (old_nickstring, old_replstring)
                else:
                    errstring += "\nNick '|w%s|n' was not deleted." % old_nickstring
            elif replstring:
                # creating new nick
                errstring = ""
                if oldnick:
                    string += "\nNick '|w%s|n' updated to map to '|w%s|n'." % (old_nickstring, replstring)
                else:
                    string += "\nNick '|w%s|n' mapped to '|w%s|n'." % (nickstring, replstring)
                try:
                    caller.nicks.add(nickstring, replstring, category=nicktype)
                except NickTemplateInvalid:
                    caller.msg("You must use the same $-markers both in the nick and in the replacement.")
                    return
            elif old_nickstring and old_replstring:
                # just looking at the nick
                string += "\nNick '|w%s|n' maps to '|w%s|n'." % (old_nickstring, old_replstring)
                errstring = ""
        string = errstring if errstring else string
        caller.msg(string)


class CmdInventory(COMMAND_DEFAULT_CLASS):
    """
    view inventory

    Usage:
      inventory
      inv

    Shows your inventory.
    """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        items = self.caller.contents
        if not items:
            string = "You are not carrying anything."
        else:
            table = evtable.EvTable(border="header")
            for item in items:
                table.add_row("|C%s|n" % item.name, item.db.desc or "")
            string = "|wYou are carrying:\n%s" % table
        self.caller.msg(string)


class CmdGet(COMMAND_DEFAULT_CLASS):
    """
    pick up something

    Usage:
      get <stuff>

    Picks up an object from your location and puts it in your inventory.

    To manipulate multiple items, use get 2-item to get the second item and so-on.
    """
    key = "get"
    aliases = "grab"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """implements the command."""

        caller = self.caller

        if not self.args:
            caller.msg("Get what?")
            return
        obj = caller.search(self.args, location=caller.location)
        if not obj:
            caller.msg("Get what?")
            return
        if caller == obj:
            caller.msg("You can't get yourself.")
            return
        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        if obj.db.birth_time:
            if obj.db.birth_time + obj.db.duration < time.time():
                caller.msg("%s crumbles to dust when you touch it! Just how old was that thing?" % str.capitalize(str(obj.name)))
                obj.delete()
                return

        obj.move_to(caller, quiet=True)
        caller.msg("You pick up %s." % obj.name)
        caller.location.msg_contents("%s picks up %s." %
                                     (caller.name,
                                      obj.name),
                                     exclude=caller)
        # calling hook method
        obj.at_get(caller)

        if utils.inherits_from(obj, "typeclasses.dropped_silver.Dropped_Silver"):
            caller.db.silver_carried = caller.db.silver_carried + obj.db.coins_value
            obj.delete()
            return


class CmdDrop(COMMAND_DEFAULT_CLASS):
    """
    drop something

    Usage:
      drop <stuff>
      drop <amount of> silver

    Lets you drop an object from your inventory into the location you are currently in.

    To manipulate multiple items, use drop 2-item to drop the second item and so-on.
    """

    key = "drop"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement command"""

        caller = self.caller
        if not self.args:
            caller.msg("Drop what?")
            return

        args = self.args

        self.silver_amount = False
        self.silver_amount_int = False
        self.silver_name = False

        if args and ' silver' in args:
            # Note: the word "drop" isn't included in the args...
            self.lhs = args[:-7]
            self.rhs = args[-7:]
            self.lhs = self.lhs.strip()
            if self.lhs.isdigit():
                self.silver_amount = self.lhs
                self.silver_amount_int = int(self.silver_amount)
            else:
                self.caller.msg("That's not a number!")
                self.silver_amount = False
                return
            silver_name = "a single silver sovereign"

        if self.silver_amount_int:
            if 1 <= self.silver_amount_int <= 4:
                self.silver_name = "a few silver sovereigns"

            elif 5 <= self.silver_amount_int <= 8:
                self.silver_name = "several silver sovereigns"

            elif 9 <= self.silver_amount_int <= 15:
                self.silver_name = "about a dozen silver sovereigns"

            elif 16 <= self.silver_amount_int <= 20:
                self.silver_name = "a small pile of silver sovereigns"

            elif 21 <= self.silver_amount_int <= 40:
                self.silver_name = "a pile of silver sovereigns"

            elif 41 <= self.silver_amount_int <= 70:
                self.silver_name = "a sizable stack of silver sovereigns"

            elif 71 <= self.silver_amount_int <= 99:
                self.silver_name = "a large pile of silver sovereigns"

            elif 100 <= self.silver_amount_int <= 200:
                self.silver_name = "a huge pile of silver sovereigns"

            elif 201 <= self.silver_amount_int:
                self.silver_name = "a massive pile of silver sovereigns"


        if self.silver_name:
            dropped_silver = {"key": self.silver_name,
                             "typeclass": "typeclasses.dropped_silver.Dropped_Silver",
                             "aliases": ["money", "coins"],
                             "desc": "Silver sovereigns have the likeness of a mighty lion engraved upon their surface on one side and the Tower of Corinth on the other.",
                             "location": caller.location,
                              "coins_value": self.silver_amount_int}

        if self.silver_amount:
            if caller.db.silver_carried < self.silver_amount_int:
                caller.msg("You aren't carrying that much silver.")
                return
            else:
                string = "You drop {:,} silver.".format(self.silver_amount_int)
                caller.msg(string)
                string = "{} drops {:,} silver.".format(caller.name, self.silver_amount_int)
                caller.location.msg_contents(string, exclude=caller)

                caller.db.silver_carried = caller.db.silver_carried - self.silver_amount_int
                new_object = spawn(dropped_silver, location=caller.location)
                return

        obj = caller.search(self.args, location=caller,
                            nofound_string="You aren't carrying %s." % self.args,
                            multimatch_string="You carry more than one %s:" % self.args)
        if not obj:
            caller.msg("Drop what?")
            return

        if obj in caller.db.wielding:
            caller.msg("You have to stop wielding it before you can drop it.")
            return

        if obj in caller.db.clothes_objects:
            caller.msg("You have to remove it before you can drop it!")
            return

        if obj in caller.db.girdle:
            caller.msg("You have to detach it from your girdle before you can drop it.")
            return

        if obj.db.birth_time:
            if obj.db.birth_time + obj.db.duration < time.time():
                caller.msg("%s crumbles to dust when you touch it! Just how old was that thing?" % str.capitalize(str(obj.name)))
                obj.delete()
                return

        obj.move_to(caller.location, quiet=True)
        caller.msg("You drop %s." % (obj.name,))
        caller.location.msg_contents("%s drops %s." %
                                     (caller.name, obj.name),
                                     exclude=caller)
        # Call the object script's at_drop() method.
        obj.at_drop(caller)


class CmdGive(COMMAND_DEFAULT_CLASS):
    """
    Give an item or some silver to someone.

    Usage:
      give <item> to <target>
      give <#> silver to <target>

    """
    key = "give"
    aliases = ["lend"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def parse(self):
        "Not-so-trivial parser!"
        raw = self.args
        args = raw.strip()

        switches = []

        silver_amount = False

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
        lhslist, rhslist = [arg.strip() for arg in args.split(',')], []
        if args and ' silver to ' in args:
            lhs, rhs = [arg.strip() for arg in args.split(' to ', 1)]
            lhslist = [arg.strip() for arg in lhs.split(',')]
            rhslist = [arg.strip() for arg in rhs.split(',')]
            silver_amount = 10
        elif args and ' to ' in args:
            lhs, rhs = [arg.strip() for arg in args.split(' to ', 1)]
            lhslist = [arg.strip() for arg in lhs.split(',')]
            rhslist = [arg.strip() for arg in rhs.split(',')]

        # save to object properties:
        self.raw = raw
        self.switches = switches
        self.args = args.strip()
        self.arglist = arglist
        self.lhs = lhs
        self.lhslist = lhslist
        self.rhs = rhs
        self.rhslist = rhslist
        self.silver_amount = silver_amount

    def func(self):
        """Implement give"""

        caller = self.caller

        if self.silver_amount:
            if not self.args or not self.rhs:
                caller.msg("Usage: give <item> to <target>")
                return
            target = caller.search(self.rhs)
            if not target:
                caller.msg("Give how much silver to who?")
                return
            if target == caller:
                caller.msg("You decide not to give away your silver after all.")
                return

            # Start extra silver parsing here!
            lhs1 = self.lhs[:-7]
            lhs2 = "silver"
            silver_amount = int(lhs1)

            if caller.db.silver_carried < silver_amount:
                caller.msg("You are not carrying that much silver.")
                return
            elif not utils.inherits_from(target, "typeclasses.characters.Character"):
                caller.msg("You can't give silver to that.")
                return
            else:
                #string = "You are carrying {:,} silver sovereigns.".format(caller.db.silver_carried)
                string = "You give {:,} silver to {}.".format(silver_amount, target.name)
                caller.msg(string)
                string = "{} gives you {:,} silver sovereigns.".format(caller.name, silver_amount)
                target.msg(string)
                emit_string = ("%s gives %s some silver sovereigns." % (caller.name, target.name))
                caller.location.msg_contents(emit_string, exclude=(caller, target), from_obj=caller)
                caller.db.silver_carried = caller.db.silver_carried - silver_amount
                target.db.silver_carried = target.db.silver_carried + silver_amount
            return

        if not self.args or not self.rhs:
            caller.msg("Usage: give <item> to <target>")
            return
        to_give = caller.search(self.lhs, location=caller,
                                nofound_string="You aren't carrying %s." % self.lhs,
                                multimatch_string="You carry more than one %s:" % self.lhs)
        target = caller.search(self.rhs)
        if not (to_give and target):
            caller.msg("Give what to who?")
            return
        if target == caller:
            caller.msg("You keep %s to yourself." % to_give.key)
            return
        if not to_give.location == caller:
            caller.msg("You are not holding %s." % to_give.key)
            return

        if to_give in caller.db.wielding:
            caller.msg("You have to stop wielding it before you can give it away.")
            return

        if to_give in caller.db.clothes_objects:
            caller.msg("You have to remove it before you can give it away!")
            return

        if to_give in caller.db.girdle:
            caller.msg("You have to detach it from your girdle before you can give it away.")
            return

        if utils.inherits_from(target, "typeclasses.npcs.Combat_Merchant_Mob"):
            caller.msg("%s hands %s back to you.\n|c%s says, \"I trade in %s. If you have any you'd like to |wsell|c to me, I'm interested.\"" % (target.name, to_give, target.name, target.db.trade_item))
            return

        if not utils.inherits_from(target, "typeclasses.characters.Character"):
            caller.msg("You can't give %s to that." % to_give)
            return

        # give object
        caller.msg("You give %s to %s." % (to_give.key, target.key))
        to_give.move_to(target, quiet=True)
        target.msg("%s gives you %s." % (caller.key, to_give.key))
        emit_string = ("%s gives %s %s." % (caller.name, target.name, to_give.key))
        caller.location.msg_contents(emit_string, exclude=(caller, target), from_obj=caller)
        # Call the object script's at_give() method.
        to_give.at_give(caller, target)


class CmdDesc(COMMAND_DEFAULT_CLASS):
    """
    describe yourself

    Usage:
      desc <description>

    Add a description to yourself. This
    will be visible to people when they
    look at you.
    """
    key = "desc"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """add the description"""

        if not self.args:
            self.caller.msg("You must add a description.")
            return

        self.caller.db.desc = self.args.strip()
        self.caller.msg("You set your description.")


class CmdSay(COMMAND_DEFAULT_CLASS):
    """
    Speak as your character.

    Usage:
      say message
      \"Great!

    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"

    def func(self):
        """Run the say command"""

        caller = self.caller

        if not self.args:
            caller.msg("Say what?")
            return

        #WHN: Cleaning up the presentation.
        speech = self.args
        speech = speech.lstrip()
        speech = speech[0].upper() + speech[1:]
        speech_type = "say"
        if not speech.endswith(".") and not speech.endswith("!") and not speech.endswith("?"):
                    speech = speech + "."

        if speech.endswith("!"):
            speech_type = "exclaim"
        elif speech.endswith("?"):
            speech_type = "ask"

        # calling the speech hook on the location
        speech = caller.location.at_say(caller, speech)

        # Feedback for the object doing the talking.
        caller.msg('|cYou %s, "%s|c"|n' % (speech_type, speech))

        # Build the string to emit to neighbors.
        emit_string = '|c%s %ss, "%s|c"|n' % (caller.name, speech_type, speech)
        caller.location.msg_contents(emit_string, exclude=caller, from_obj=caller)


class CmdWhisper(COMMAND_DEFAULT_CLASS):
    """
    Speak privately as your character to another

    Usage:
      whisper <player> = <message>

    Talk privately to those in your current location, without
    others being informed.
    """

    key = "whisper"
    locks = "cmd:all()"

    def func(self):
        """Run the whisper command"""

        caller = self.caller

        if not self.lhs or not self.rhs:
            caller.msg("Usage: whisper <player> = <message>")
            return

        receiver = caller.search(self.lhs)

        if not receiver:
            return

        if caller == receiver:
            caller.msg("You can't whisper to yourself.")
            return

        speech = self.rhs
        speech = speech.lstrip()
        speech = speech[0].upper() + speech[1:]
        if not speech.endswith(".") and not speech.endswith("!") and not speech.endswith("?"):
            speech = speech + "."

        # Feedback for the object doing the talking.
        caller.msg('You whisper to %s, "%s|n"' % (receiver.key, speech))

        # Build the string to emit to receiver.
        emit_string = '%s whispers, "%s|n"' % (caller.name, speech)
        receiver.msg(text=(emit_string, {"type": "whisper"}), from_obj=caller)


class CmdPose(COMMAND_DEFAULT_CLASS):
    """
    strike a pose

    Usage:
      pose <pose text>
      pose's <pose text>

    Example:
      pose is standing by the wall, smiling.
       -> others will see:
      Tom is standing by the wall, smiling.

    Describe an action being taken. The pose text will
    automatically begin with your name.
    """
    key = "pose"
    aliases = [":", "emote"]
    locks = "cmd:all()"

    def parse(self):
        """
        Custom parse the cases where the emote
        starts with some special letter, such
        as 's, at which we don't want to separate
        the caller's name and the emote with a
        space.
        """
        args = self.args
        if args and not args[0] in ["'", ",", ":"]:
            args = " %s" % args.strip()
        self.args = args

    def func(self):
        """Hook function"""
        if not self.args:
            msg = "What do you want to do?"
            self.caller.msg(msg)
        else:
            msg = "%s%s" % (self.caller.name, self.args)
            self.caller.location.msg_contents(text=(msg, {"type": "pose"}),
                                              from_obj=self.caller)


class CmdAccess(COMMAND_DEFAULT_CLASS):
    """
    show your current game access

    Usage:
      access

    This command shows you the permission hierarchy and
    which permission groups you are a member of.
    """
    key = "access"
    aliases = ["groups", "hierarchy"]
    locks = "cmd:pperm(PlayerHelpers)"
    arg_regex = r"$"

    def func(self):
        """Load the permission groups"""

        caller = self.caller
        hierarchy_full = settings.PERMISSION_HIERARCHY
        string = "\n|wPermission Hierarchy|n (climbing):\n %s" % ", ".join(hierarchy_full)

        if self.caller.player.is_superuser:
            cperms = "<Superuser>"
            pperms = "<Superuser>"
        else:
            cperms = ", ".join(caller.permissions.all())
            pperms = ", ".join(caller.player.permissions.all())

        string += "\n|wYour access|n:"
        string += "\nCharacter |c%s|n: %s" % (caller.key, cperms)
        if hasattr(caller, 'player'):
            string += "\nPlayer |c%s|n: %s" % (caller.player.key, pperms)
        caller.msg(string)
