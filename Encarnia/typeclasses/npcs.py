"""
Weapon

The default weapon object, file is called Arms so that it doesn't conflict with a tutorial weapon object.

"""
from evennia import DefaultObject
from evennia import default_cmds, CmdSet, utils
from commands.default_cmdsets import ChargenCmdset, ShopCmdset, BankCmdset, MerchantCmdset
from world import english_utils, npc_rules # , npc_rules
from random import randint
import time
from evennia import TICKER_HANDLER as tickerhandler

class Combat_Mob(DefaultObject): # This mob will not attack people but it will defend itself from attack.
    """

     """

    def at_object_creation(self):

        # Inherit the object properties.
        super(Combat_Mob, self).at_object_creation()

        self.aliases.add([])

        #self.name = "a ruddy bronze broadsword" # not sure if I need this
        self.db.live_name = "a giant rat"
        self.db.defeated_name = "the mangled remains of some large vermin" # must not have 'rat' in it or it can't be targetted!
        self.db.alive = True
        self.db.desc = ""

        self.db.health = 35
        self.db.max_health = 35 # NPC damage, (player level * strength) * weapon damage ratio.
        # So a level 1 would do 10 damage a hit, then 20, then 30, up to 1,000 per hit at level 100.

        self.db.damage_amount = 15

        self.db.ticker_speed = 3 # how often it attempts to attack or move/attack if a target is not found.  This will only fire so many times before they 'forget'.
        self.db.counter_attack_chance = False # integer chance this npc will trigger a counter-attack.  Defaults as false.
        self.db.respawn_speed = 600 # SHOULD BE A MULTIPLE OF 100
        self.db.tries = 3 # how long it will spend trying to find its attacker before shutting down.

        self.db.exp_level = 10 # this is the relative level of the creature
        self.db.exp_multiplier = 4 # If you're under the level, subtract player level from NPC level and multiply by the multiplier.
        self.db.exp_max_level = 20 # At this level you won't gain any experience from killing this NPC.

        self.db.home_location = "#2" # This should be set!

        # So normally any kill is worth 1% exp.
        # But if your level is under the npc's level, you get a bonus
        # The bonus is level difference * multiplier.

        # This multiplier equation could similarly be used when attacking people below your current level, so you might
        # level up multiple times from killing a high-level person.

        self.db.offended_by = []

        self.db.lootable = False #can be LOOTed for silver.
        self.db.looted_yet = False
        self.db.silver_amount = 0

        self.db.skinnable = True #can be SKINNED for a pelt or skin item.
        self.db.skinned_yet = False
        self.db.pelt_name = "a giant rat pelt"

        self.db.attack_message_1 = "A giant rat hurls itself bodily into "
        self.db.attack_message_2 = "A giant rat claws and bites at "
        self.db.attack_message_3 = "With a resounding crunching sound, a giant rat bites into "

    def npc_active_ticks(self, *args, **kwargs):
        "Ticks after the NPC has been attacked."

        targets = False # Any targets in the room?

        # This should probably go below.
        if self.db.tries_left > 0:
            for i in self.location.contents:
                if i in self.db.offended_by:
                    targets = True
                    npc_rules.attack(self, i)
                    self.db.tries_left = 3
                    return

        if not targets:
            for k, v in self.location.db.trails.iteritems():
                target_name = str(self.db.offended_by[0])
                if k == target_name:
                    destination = self.search(v)
                    self.move_to(destination)
                    for i in self.location.contents:
                        if i in self.db.offended_by:
                            targets = True
                            npc_rules.attack(self, i)
                            self.db.tries_left = 3
                            break
                    break

        self.db.tries_left = self.db.tries_left - 1

        if self.db.tries_left < 0:
            self.db.offended_by = []
            self.db.tries_left = self.db.tries
            tickerhandler.remove(self.db.ticker_speed, self.npc_active_ticks)
            return

    def npc_revive_ticks(self, *args, **kwargs):
        "ticked when "

        self.db.alive = True

        self.name = self.db.live_name
        self.db.health = self.db.max_health

        self.db.looted_yet = False
        self.db.skinned_yet = False

        destination = self.search(self.db.home_location, global_search=True)
        self.move_to(destination)

        tickerhandler.remove(self.db.respawn_speed, self.npc_revive_ticks)
        return

class Combat_Merchant_Mob(DefaultObject): # This mob will not attack people but it will defend itself from attack.
    """

     """

    def at_object_creation(self):

        # Inherit the object properties.
        super(Combat_Merchant_Mob, self).at_object_creation()

        self.cmdset.add(MerchantCmdset, permanent=True)

        self.aliases.add([])

        #self.name = "a ruddy bronze broadsword" # not sure if I need this
        self.db.live_name = "a giant rat"
        self.db.defeated_name = "the mangled remains of some large vermin" # must not have 'rat' in it or it can't be targetted!
        self.db.alive = True
        self.db.desc = ""

        self.db.trade_item = "pelts"

        self.db.health = 135
        self.db.max_health = 135 # NPC damage, (player level * strength) * weapon damage ratio.
        # So a level 1 would do 10 damage a hit, then 20, then 30, up to 1,000 per hit at level 100.

        self.db.damage_amount = 30

        self.db.ticker_speed = 3 # how often it attempts to attack or move/attack if a target is not found.  This will only fire so many times before they 'forget'.
        self.db.counter_attack_chance = False # integer chance this npc will trigger a counter-attack.  Defaults as false.
        self.db.respawn_speed = 600 # SHOULD BE A MULTIPLE OF 100
        self.db.tries = 3 # how long it will spend trying to find its attacker before shutting down.

        self.db.exp_level = 10 # this is the relative level of the creature
        self.db.exp_multiplier = 4 # If you're under the level, subtract player level from NPC level and multiply by the multiplier.
        self.db.exp_max_level = 20 # At this level you won't gain any experience from killing this NPC.

        self.db.home_location = "#2" # This should be set!

        # So normally any kill is worth 1% exp.
        # But if your level is under the npc's level, you get a bonus
        # The bonus is level difference * multiplier.

        # This multiplier equation could similarly be used when attacking people below your current level, so you might
        # level up multiple times from killing a high-level person.

        self.db.offended_by = []

        self.db.lootable = True #can be LOOTed for silver.
        self.db.looted_yet = False
        self.db.silver_amount = 10

        self.db.skinnable = False #can be SKINNED for a pelt or skin item.
        self.db.skinned_yet = False
        self.db.pelt_name = "a giant rat pelt"

        self.db.attack_message_1 = "A giant rat hurls itself bodily into "
        self.db.attack_message_2 = "A giant rat claws and bites at "
        self.db.attack_message_3 = "With a resounding crunching sound, a giant rat bites into "

    def npc_active_ticks(self, *args, **kwargs):
        "Ticks after the NPC has been attacked."

        targets = False # Any targets in the room?

        # This should probably go below.
        if self.db.tries_left > 0:
            for i in self.location.contents:
                if i in self.db.offended_by:
                    targets = True
                    npc_rules.attack(self, i)
                    self.db.tries_left = 3
                    return

        if not targets:
            for k, v in self.location.db.trails.iteritems():
                target_name = str(self.db.offended_by[0])
                if k == target_name:
                    destination = self.search(v)
                    self.move_to(destination)
                    for i in self.location.contents:
                        if i in self.db.offended_by:
                            targets = True
                            npc_rules.attack(self, i)
                            self.db.tries_left = 3
                            break
                    break

        self.db.tries_left = self.db.tries_left - 1

        if self.db.tries_left < 0:
            self.db.offended_by = []
            self.db.tries_left = self.db.tries
            tickerhandler.remove(self.db.ticker_speed, self.npc_active_ticks)
            return

    def npc_revive_ticks(self, *args, **kwargs):
        "ticked when "

        self.db.alive = True

        self.name = self.db.live_name
        self.db.health = self.db.max_health

        self.db.looted_yet = False
        self.db.skinned_yet = False

        destination = self.search(self.db.home_location, global_search=True)
        self.move_to(destination)

        tickerhandler.remove(self.db.respawn_speed, self.npc_revive_ticks)
        return