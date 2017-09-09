"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds
from commands import command, emotes, movecommands, melee, gametime, business, shop, merchant, fae_magic
from evennia.commands.cmdset import CmdSet
from evennia.commands.default import help, comms, admin, system
from evennia.commands.default import building, player

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `PlayerCmdSet` when a Player puppets a Character.
    """
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(CharacterCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #

        self.add(command.CmdWear())
        self.add(command.CmdRemove())
        self.add(command.CmdScore())
        self.add(command.CmdInventory())
        self.add(command.CmdWield())
        self.add(command.CmdUnwield())
        self.add(command.CmdSecure())
        self.add(command.CmdDetach())
        self.add(command.CmdSkin())
        self.add(command.CmdMap())
        self.add(command.CmdDrawMap())
        self.add(command.CmdWalkTo())
        self.add(command.CmdStat())
        self.add(command.CmdFollow())
        self.add(command.CmdLose())

        # Misc
        self.add(gametime.CmdTime())
        self.add(command.CmdHonors())
        #self.add(command.MobCalm())

        # Comm commands
        self.add(comms.CmdAddCom())
        self.add(comms.CmdDelCom())
        self.add(comms.CmdAllCom())
        self.add(comms.CmdChannels())
        self.add(comms.CmdCdestroy())
        self.add(comms.CmdChannelCreate())
        self.add(comms.CmdClock())
        self.add(comms.CmdCBoot())
        self.add(comms.CmdCemit())
        self.add(comms.CmdCWho())
        self.add(comms.CmdCdesc())
        self.add(comms.CmdPage())
        self.add(comms.CmdIRC2Chan())
        self.add(comms.CmdIRCStatus())
        self.add(comms.CmdRSS2Chan())

        # TCN: Melee (basic combat skills) go here
        self.add(melee.CmdAssess2())
        self.add(melee.CmdWielded())
        self.add(melee.CmdAttack())
        self.add(melee.CmdDefend())
        self.add(melee.CmdFeint())
        self.add(melee.CmdMaul())
        self.add(melee.CmdStop())

        # ASH: Fae_Magic skills start here
        self.add(fae_magic.Regeneration())
        self.add(fae_magic.Mend())
        self.add(fae_magic.FaeFire())
        self.add(fae_magic.Web())
        self.add(fae_magic.Wisp())
        self.add(fae_magic.Circle())
        self.add(fae_magic.Pierce())

        # TCN: Default exit error commands (incomplete)
        self.add(movecommands.CmdExitErrorNorth())
        self.add(movecommands.CmdExitErrorEast())
        self.add(movecommands.CmdExitErrorSouth())
        self.add(movecommands.CmdExitErrorWest())

        self.add(movecommands.CmdExitErrorNorthWest())
        self.add(movecommands.CmdExitErrorNorthEast())
        self.add(movecommands.CmdExitErrorSouthWest())
        self.add(movecommands.CmdExitErrorSouthEast())

        self.add(movecommands.CmdExitErrorUp())
        self.add(movecommands.CmdExitErrorDown())

        # TCN: emotes.py
        self.add(emotes.CmdSmile())
        self.add(emotes.CmdGrin())
        self.add(emotes.CmdBow())
        self.add(emotes.CmdKneel())
        self.add(emotes.CmdBeg())
        self.add(emotes.CmdPray())
        self.add(emotes.CmdAnger())
        self.add(emotes.CmdSmirk())
        self.add(emotes.CmdNod())
        self.add(emotes.CmdShake())
        self.add(emotes.CmdSalute())
        self.add(emotes.CmdWink())
        self.add(emotes.CmdDance())
        self.add(emotes.CmdPat())
        self.add(emotes.CmdWince())
        self.add(emotes.CmdApologize())
        self.add(emotes.CmdThank())
        self.add(emotes.CmdLaugh())
        self.add(emotes.CmdWave())
        self.add(emotes.CmdCurtsey())
        self.add(emotes.CmdHug())
        self.add(emotes.CmdKiss())
        self.add(emotes.CmdFrown())
        self.add(emotes.CmdMutter())
        self.add(emotes.CmdScream())
        self.add(emotes.CmdWhine())
        self.add(emotes.CmdPoke())
        self.add(emotes.CmdTear())
        self.add(emotes.CmdCry())
        self.add(emotes.CmdPoint())
        self.add(emotes.CmdFacepalm())
        self.add(emotes.CmdParagon())
        self.add(emotes.CmdSmooth())
        self.add(emotes.CmdFistBump())
        self.add(emotes.CmdHi())
        self.add(emotes.CmdHeh())
        self.add(emotes.CmdOK())
        self.add(emotes.CmdYo())
        self.add(emotes.CmdPonder())
        self.add(emotes.CmdShrug())
        self.add(emotes.CmdGreet())
        self.add(emotes.CmdPet())
        
class PlayerCmdSet(default_cmds.PlayerCmdSet):
    """
    This is the cmdset available to the Player at all times. It is
    combined with the `CharacterCmdSet` when the Player puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """
    key = "DefaultPlayer"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(PlayerCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """
    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(UnloggedinCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """
    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super(SessionCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #

# TCN: More chargen stuff.
from evennia import CmdSet
from commands import command

#WHN: Adds the CmdSetPower command
class ChargenCmdset(CmdSet):
    """
    This cmdset it used in character generation areas.
    """
    key = "Chargen"
    def at_cmdset_creation(self):
        "This is called at initialization"
        self.add(command.CharGenSelect())

class BankCmdset(CmdSet):
    """
    This cmdset it used in character generation areas.
    """
    key = "bank"
    def at_cmdset_creation(self):
        "This is called at initialization"
        self.add(business.CmdDeposit())
        self.add(business.CmdWithdraw())
        self.add(business.CmdBalance())
        self.add(business.CmdDonate())

class ShopCmdset(CmdSet):
    """
    This cmdset it used in character generation areas.
    """
    key = "shop"
    def at_cmdset_creation(self):
        "This is called at initialization"
        self.add(shop.CmdShop())

class MerchantCmdset(CmdSet):
    """
    This cmdset it used in character generation areas.
    """
    key = "merchant"
    def at_cmdset_creation(self):
        "This is called at initialization"
        self.add(merchant.CmdSell())