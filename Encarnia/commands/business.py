from evennia import Command as BaseCommand
from evennia import utils
from evennia.commands.default.muxcommand import MuxCommand
from world import rules
from world import english_utils
import time

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

class CmdDeposit(BaseCommand):
    """
    Deposit some silver sovereigns into the bank.

    Usage:
        deposit <silver>

    Hint: The fruit is fake.
    """
    key = "deposit"
    #aliases = ["lend", "donate"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Business"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):

        value = self.target
        value_s = str(value)

        caller = self.caller

        if not value:
            caller.msg("Deposit how much?")
            return
        elif not str.isdigit(value_s):
            caller.msg("You must specify a number (and only a number) that you wish to deposit.")
            # caller.search handles error messages
            return
        elif caller.db.silver_carried < int(value):
            caller.msg("That's more silver than you're carrying!")
            return
        elif caller.db.silver_carried >= int(value):
            string = "You deposit {:,} silver sovereigns into your Tower bank account.".format(int(value))
            caller.msg(string)
            caller.db.silver_carried = caller.db.silver_carried - int(value)
            caller.db.tower_bank_account = caller.db.tower_bank_account + int(value)
            return

class CmdWithdraw(BaseCommand):
    """
    Withdraw some silver sovereigns from the bank.

    Usage:
        withdraw <silver>

    Hint: The fruit is fake.
    """
    key = "withdraw"
    #aliases = ["lend", "donate"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Business"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):

        value = self.target
        value_s = str(value)

        caller = self.caller

        if not value:
            caller.msg("Withdraw how much?")
            return
        elif not str.isdigit(value_s):
            caller.msg("You must specify a number (and only a number) that you wish to withdraw.")
            # caller.search handles error messages
            return
        elif caller.db.tower_bank_account < int(value):
            caller.msg("That's more silver than you have in your account!")
            return
        elif caller.db.tower_bank_account >= int(value):
            string = "You withdraw {:,} silver sovereigns from your Tower bank account.".format(int(value))
            caller.msg(string)
            caller.db.silver_carried = caller.db.silver_carried + int(value)
            caller.db.tower_bank_account = caller.db.tower_bank_account - int(value)
            return

class CmdBalance(BaseCommand):
    """
    Check the outstanding balance in your bank account.

    """
    key = "balance"
    #aliases = ["lend", "donate"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Business"

    def func(self):
        string = "You have {:,} silver sovereigns available for withdrawal from your Tower bank account.".format(self.caller.db.tower_bank_account)
        self.caller.msg(string)

class CmdDonate(BaseCommand):
    """
    Donate some silver sovereigns to Corinth's city coffers.  City offers are primarily used for law enforcement and military purposes.

    Usage:
        donate <silver>

    """
    key = "donate"
    #aliases = ["lend", "donate"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "Business"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):

        value = self.target
        value_s = str(value)

        caller = self.caller

        sphere = caller.search("#609", global_search=True)

        if not value:
            caller.msg("Donate how much to Corinth?")
            return
        elif not str.isdigit(value_s):
            caller.msg("You must specify a number (and only a number) that you wish to donate.")
            # caller.search handles error messages
            return
        elif caller.db.silver_carried < int(value):
            caller.msg("That's more silver than you're carrying!")
            return
        elif caller.db.silver_carried >= int(value):
            string = "You deposit {:,} silver sovereigns into Corinth's city coffers.".format(int(value))
            caller.msg(string)
            caller.db.silver_carried = caller.db.silver_carried - int(value)
            sphere.db.coffers = sphere.db.coffers + int(value)
            return

# class CmdBuy(BaseCommand):
#     """
#     Buy an item from a shop.
#
#     Usage:
#         deposit <silver>
#
#     Hint: The fruit is fake.
#     """
#     key = "buy"
#     #aliases = ["lend", "donate"]
#     locks = "cmd:all()"
#     arg_regex = r"\s|$"
#
#     def parse(self):
#         "Very trivial parser"
#         self.target = self.args.strip()
#
#     def func(self):
#
#         value = self.target
#         value_s = str(value)
#
#         caller = self.caller
#
#         if not value:
#             caller.msg("Deposit how much?")
#             return
#         elif not str.isdigit(value_s):
#             caller.msg("You must specify a number (and only a number) that you wish to deposit.")
#             # caller.search handles error messages
#             return
#         elif caller.db.silver_carried < int(value):
#             caller.msg("That's more silver than you're carrying!")
#             return
#         elif caller.db.silver_carried >= int(value):
#             string = "You deposit {:,} silver sovereigns into your Tower bank account.".format(int(value))
#             caller.msg(string)
#             caller.db.silver_carried = caller.db.silver_carried - int(value)
#             caller.db.tower_bank_account = caller.db.tower_bank_account + int(value)
#             return