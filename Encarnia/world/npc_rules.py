from random import randint
from world import english_utils, rules
from evennia import TICKER_HANDLER as tickerhandler
from evennia.server.sessionhandler import SESSIONS

def attack(caller, target):
    "Returns a random one-handed sword attack message."

    d3 = randint(1,3)

    if d3 == 1:
        message_t = caller.db.attack_message_1 + " you!"
        message_r = caller.db.attack_message_1 + " %s!" % target.name

        armor_block = 100 - target.db.armor_bonus
        armor_block = float(armor_block) / 100
        damage_amount = caller.db.damage_amount
        damage_amount = damage_amount * armor_block
        damage_amount = int(damage_amount)
        target.db.health = target.db.health - damage_amount
        target.msg(message_t)
        target.location.msg_contents(message_r, exclude=target)
        if target.db.health <= 0:
            target.db.health = 0
            string = "|m%s has been slain by %s.|n" % (target.name, caller.name)
            SESSIONS.announce_all(string)
            rules.death_movement(caller, target)


    elif d3 == 2:
        message_t = caller.db.attack_message_2 + " you!"
        message_r = caller.db.attack_message_2 + " %s!" % target.name

        armor_block = 100 - target.db.armor_bonus
        armor_block = float(armor_block) / 100
        damage_amount = caller.db.damage_amount * 2
        damage_amount = damage_amount * armor_block
        damage_amount = int(damage_amount)
        target.db.health = target.db.health - damage_amount
        target.msg(message_t)
        target.location.msg_contents(message_r, exclude=target)
        if target.db.health <= 0:
            target.db.health = 0
            string = "|m%s has been slain by %s.|n" % (target.name, caller.name)
            SESSIONS.announce_all(string)
            rules.death_movement(caller, target)

    elif d3 == 3:
        message_t = caller.db.attack_message_3 + " you!"
        message_r = caller.db.attack_message_3 + " %s!" % target.name

        armor_block = 100 - target.db.armor_bonus
        armor_block = float(armor_block) / 100
        damage_amount = caller.db.damage_amount * 3
        damage_amount = damage_amount * armor_block
        damage_amount = int(damage_amount)
        target.db.health = target.db.health - damage_amount
        target.msg(message_t)
        target.location.msg_contents(message_r, exclude=target)
        if target.db.health <= 0:
            target.db.health = 0
            string = "|m%s has been slain by %s.|n" % (target.name, caller.name)
            SESSIONS.announce_all(string)
            rules.death_movement(caller, target)

    if (float(target.db.health) / float(target.db.max_health)) > 0.80:
        prompt_hp_color = "|g"
    elif (float(target.db.health) / float(target.db.max_health)) > 0.36:
        prompt_hp_color = "|y"
    else:
        prompt_hp_color = "|r"

    if target.db.stamina > 6:
        prompt_stamina_color = "|g"
    elif target.db.stamina > 3:
        prompt_stamina_color = "|y"
    else:
        prompt_stamina_color = "|r"

    prompt = "%sHealth|n: %s%s|n - |gMagic|n: |nAsleep|n - %sStamina|n: %s%s." % (prompt_hp_color, prompt_hp_color, target.db.health, prompt_stamina_color, prompt_stamina_color, target.db.stamina)
    target.msg(prompt)

def npc_attacked(self):
    self.db.tries_left = self.db.tries
    tickerhandler.add(self.db.ticker_speed, self.npc_active_ticks) # this would actually go into MeleeCommand's function for when an npc is hit.