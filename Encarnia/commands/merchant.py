from evennia import Command as BaseCommand
from evennia import utils
from evennia.commands.default.muxcommand import MuxCommand
from world import rules
from world import english_utils
import time
from evennia.utils.evmenu import EvMenu

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

            prompt = "%sHealth|n: %s%s|n - |gMagic|n: Asleep - %sStamina|n: %s%s." % (
                prompt_hp_color, prompt_hp_color, caller.db.health, prompt_stamina_color, prompt_stamina_color,
                caller.db.stamina)

            caller.msg(prompt)

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

class CmdSell(BaseCommand):
    """
    Check which items are for sale in a given shop.

    Usage:
        goods
    """

    key = "sell"
    #aliases = ["lend", "donate"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Business"

    # def func(self):
    #     string = "You have {:,} silver sovereigns available for withdrawal from your Tower bank account.".format(self.caller.db.tower_bank_account)
    #     self.caller.msg(string)

    # key = "shop"
    # aliases = ["wares", "goods"]
    # locks = "cmd:all()"
    # arg_regex = r"\s$"
    # help_category = "Business"
    #

    # in for example a chargen command (you would probably
    # not start with this node though)

    def func(self):
        caller = self.caller

        total = 0
        merchant_name = "none"
        item_sold = "none"

        for i in caller.location.contents:
            if utils.inherits_from(i, "typeclasses.npcs.Combat_Merchant_Mob"):
                merchant_name = i.name

        for i in caller.contents:
            if i.name == "a small and crude fur pelt":
                total = total + 1
                item_sold = "pelt"
                i.delete()
            elif i.name == "a small fur pelt":
                total = total + 2
                item_sold = "pelt"
                i.delete()
            elif i.name == "a small but fine fur pelt":
                total = total +3
                item_sold = "pelt"
                i.delete()

        if item_sold == "none":
            caller.msg("You have nothing to sell!")

        if item_sold == "pelt":
            string = merchant_name + " gives you " + str(total) + " silver sovereigns in return for your pelts."
            caller.msg(string)
            caller.db.silver_carried = caller.db.silver_carried + total

            string_r = merchant_name + " gives " + caller.name + " " + str(total) + " silver sovereigns in return for " + caller.db.genderp + " pelts."
            caller.location.msg_contents(string_r, exclude=caller)

