from random import randint
from world import english_utils
from evennia import utils
from evennia.utils.spawner import spawn

def exp_gain(caller, target):
    # self.db.exp_level = 10  # this is the relative level of the creature
    # self.db.exp_multiplier = 4  # If you're under the level, subtract player level from NPC level and multiply by the multiplier.
    # self.db.exp_max_level = 20  # At this level you won't gain any experience from killing this NPC.
    #
    # self.db.home_location = "#2"  # This should be set!
    #
    # # So normally any kill is worth 1% exp.
    # # But if your level is under the npc's level, you get a bonus
    # # The bonus is level difference * multiplier.
    #
    # # This multiplier equation could similarly be used when attacking people below your current level, so you might
    # # level up multiple times from killing a high-level person.

    exp_gain_amount = target.db.level - caller.db.level

    if exp_gain_amount < 0 and utils.inherits_from(target, "typeclasses.npcs.Combat_Mob"):
        exp_gain_amount = 0
    elif exp_gain_amount < 1:
        exp_gain_amount = 1

    exp_gain_amount = exp_gain_amount * target.db.exp_multiplier

    caller.db.exp = caller.db.exp + exp_gain_amount

    while caller.db.exp > 99 and caller.db.level < 101:
        caller.db.exp = caller.db.exp - 100
        caller.db.level = caller.db.level + 1

        level_string = str(caller.db.level)
        level_suffix = "th"

        if level_string[-1:] == "1":
            level_suffix = "st"
        elif level_string[-1:] == "2":
            level_suffix = "nd"
        elif level_string[-1:] == "3":
            level_suffix = "rd"

        caller.msg("Your aura overflows with power, producing a ringing sound as you reach the %s%s level!" % (caller.db.level, level_suffix))
        string = "A ringing sound can be heard as %s reaches the %s%s level!" % (caller.name, caller.db.level, level_suffix)
        caller.location.msg_contents(string, exclude=caller)

        new_max_health = caller.db.base_constitution * caller.db.level

        new_max_health = new_max_health + 100

        caller.db.max_health = new_max_health

def death_movement(caller, target):
    # give caller some exp
    # take some exp away from target
    caller.msg("|wYou have defeated %s!|n" % target.name)
    string = ("%s has defeated %s!" % (caller.name, target.name))
    caller.location.msg_contents(string, exclude=[caller, target])

    for i in target.contents:
        if i not in target.db.clothes_objects and i not in target.db.girdle:
            i.move_to(target.location, quiet=True)
            target.msg("You drop %s." % (i.name,))
            target.location.msg_contents("%s drops %s." %
                                         (target.name, i.name),
                                         exclude=target)


    silver_name = False
    silver_amount_int = target.db.silver_carried

    if silver_amount_int:
        if 1 <= silver_amount_int <= 4:
            silver_name = "a few silver sovereigns"

        elif 5 <= silver_amount_int <= 8:
            silver_name = "several silver sovereigns"

        elif 9 <= silver_amount_int <= 15:
            silver_name = "about a dozen silver sovereigns"

        elif 16 <= silver_amount_int <= 20:
            silver_name = "a small pile of silver sovereigns"

        elif 21 <= silver_amount_int <= 40:
            silver_name = "a pile of silver sovereigns"

        elif 41 <= silver_amount_int <= 70:
            silver_name = "a sizable stack of silver sovereigns"

        elif 71 <= silver_amount_int <= 99:
            silver_name = "a large pile of silver sovereigns"

        elif 100 <= silver_amount_int <= 200:
            silver_name = "a huge pile of silver sovereigns"

        elif 201 <= silver_amount_int:
            silver_name = "a massive pile of silver sovereigns"

    if silver_name:
        dropped_silver = {"key": silver_name,
                          "typeclass": "typeclasses.dropped_silver.Dropped_Silver",
                          "aliases": ["money", "coins"],
                          "desc": "Silver sovereigns have the likeness of a mighty lion engraved upon their surface on one side and the Tower of Corinth on the other.",
                          "location": target.location,
                          "coins_value": silver_amount_int}

    if silver_amount_int > 0:
        string = "You drop {:,} silver.".format(silver_amount_int)
        target.msg(string)
        string = "{} drops {:,} silver.".format(target.name, silver_amount_int)
        target.location.msg_contents(string, exclude=target)
        target.db.silver_carried = 0
        new_object = spawn(dropped_silver, location=caller.location)

    target.db.dead = True
    destination = target.search("#740", global_search=True)
    target.msg(
        "Bested at last, you collapse to the ground. You have been slain by %s.\nEverything goes black..." % caller.name)
    target.move_to(destination, quiet=True)
    target.db.death_ticker = 0
    target.db.moving = False
    target.db.current_magic = 0
    target.db.open_pvp = 0

    exp_gain_amount = target.db.level - caller.db.level

    if exp_gain_amount < 0 and utils.inherits_from(target, "typeclasses.npcs.Combat_Mob"):
        exp_gain_amount = 0
    elif exp_gain_amount < 1:
        exp_gain_amount = 1

    target.db.exp = target.db.exp - 40

    if target.db.exp < 0:
        if target.db.level > 1:
            target.db.level = target.db.level - 1

            level_string = str(target.db.level)
            level_suffix = "th"

            if level_string[-1:] == "1":
                level_suffix = "st"
            elif level_string[-1:] == "2":
                level_suffix = "nd"
            elif level_string[-1:] == "3":
                level_suffix = "rd"

            target.msg("You shiver as you fall to the %s%s level." % (target.db.level, level_suffix))

        target.db.exp = 100 + target.db.exp

        new_max_health = target.db.base_constitution * target.db.level

        new_max_health = new_max_health + 100

        target.db.max_health = new_max_health

    return

def weapon_attack_messages(caller, target, weapon):
    "Returns a random one-handed sword attack message."

    d3 = randint(1,3)

    message_c = "Wielding your %s, you strike %s!" % (weapon.name, target.name)
    message_t = "%s strikes you with %s %s!" % (caller.name, caller.db.genderp, weapon.name)
    message_r = "%s wields %s %s against %s!" % (caller.name, caller.db.genderp, weapon.name, target.name)

    # 1hsword
    if weapon.db.weapon_type == "1hsword":
        if d3 == 1:
            message_c = "|wWielding your %s, you lunge towards %s!|n" % (weapon.db.short_name, target.name)
            message_t = "%s lunges at you, wielding %s in a cruel arc!" % (caller.name, weapon.name)
            message_r = "%s lunges towards %s, wielding %s!" % (caller.name, target.name, weapon.name)
        elif d3 == 2:
            message_c = "|wYou thrust towards %s with your %s!|n" % (target.name, weapon.db.short_name)
            message_t = "%s thrusts towards you with %s %s!" % (caller.name, caller.db.genderp, weapon.db.short_name)
            message_r = "%s thrusts %s %s towards %s!" % (caller.name, caller.db.genderp, weapon.db.short_name, target.name)
        else:
            message_c = "|wYou swing your %s at %s with all of your might!|n" % (weapon.db.short_name, target.name)
            message_t = "%s swings %s at you with all of %s might!" % (caller.name, weapon.name, caller.db.genderp)
            message_r = "%s swings %s at %s with all of %s might!" % (caller.name, weapon.name, target.name, caller.db.genderp)
    # 1haxe
    elif weapon.db.weapon_type == "1haxe":
        if d3 == 1:
            message_c = "|wWielding your %s, you swing mightily towards %s!|n" % (weapon.db.short_name, target.name)
            message_t = "%s swings mightily at you with %s!" % (caller.name, weapon.name)
            message_r = "%s swings mightily towards %s with %s!" % (caller.name, target.name, weapon.name)
        elif d3 == 2:
            message_c = "|wYou attempt to cleave %s asunder with your %s!|n" % (target.name, weapon.db.short_name)
            message_t = "%s is trying to cleave you apart with %s %s!" % (
            caller.name, caller.db.genderp, weapon.db.short_name)
            message_r = "Wielding %s, %s tries to cleave %s apart!" % (
            weapon.name, caller.name, target.name)
        else:
            message_c = "|wGrunting and puffing, you hack at %s with your %s!|n" % (target.name, weapon.db.short_name)
            message_t = "%s grunts and puffs as %s hacks away at you with %s!" % (caller.name, caller.db.genderp, weapon.name)
            message_r = "%s grunts and puffs as %s hacks away towards %s with %s!" % (
            caller.name, caller.db.genderp, target.name, weapon.name)
    # 1hspear
    elif weapon.db.weapon_type == "1hspear":
        if d3 == 1:
            message_c = "|wYour jab mercilessly towards %s with %s!|n" % (target.name, weapon.name) # something about lets fly
            message_t = "%s jabs mercilessly at you with %s!" % (caller.name, weapon.name)
            message_r = "%s jabs mercilessly towards %s with %s!" % (caller.name, target.name, weapon.name)
        elif d3 == 2:
            message_c = "|wYou thrust at %s with your %s!|n" % (target.name, weapon.db.short_name)
            message_t = "%s thrusts at you with %s %s!" % (
            caller.name, caller.db.genderp, weapon.db.short_name)
            message_r = "%s thrusts at %s with %s %s!" % (
            caller.name, target.name, caller.db.genderp, weapon.db.short_name)
        else:
            message_c = "|wYou let fly with the tip of your %s towards %s!|n" % (
            weapon.db.short_name, target.name)
            message_t = "%s lets fly with the tip of %s %s towards you!" % (
            caller.name, caller.db.genderp, weapon.db.short_name)
            message_r = "%s lets fly with the tip of %s %s towards %s!" % (
            caller.name, caller.db.genderp, weapon.db.short_name, target.name)
    # dagger
    elif weapon.db.weapon_type == "dagger":
        if d3 == 1:
            message_c = "|wYou stab rapidly at %s with your %s!|n" % (target.name, weapon.db.short_name)
            message_t = "%s stabs rapidly at you with %s!" % (caller.name, weapon.name)
            message_r = "%s stabs rapidly at %s with %s!" % (caller.name, target.name, weapon.name)
        elif d3 == 2:
            message_c = "|wYou seek to sheathe your %s in %s!|n" % (weapon.db.short_name, target.name)
            message_t = "%s seeks to sheathe %s %s in you!" % (
            caller.name, caller.db.genderp, weapon.db.short_name)
            message_r = "%s seeks to sheathe %s %s in %s!" % (
            caller.name, caller.db.genderp, weapon.db.short_name, target.name)
        else:
            message_c = "|wYou strike with your %s at %s heart!|n" % (weapon.db.short_name, english_utils.possessive(target.name))
            message_t = "%s strikes at your heart with %s!" % (caller.name, weapon.name)
            message_r = "%s strikes at %s heart with %s!" % (
            caller.name, english_utils.possessive(target.name), weapon.name)
    # 2hsword
    elif weapon.db.weapon_type == "2hsword":
        if d3 == 1:
            message_c = "|wYou raise your %s over your head before sending it whistling down towards %s!|n" % (weapon.db.short_name, target.name)
            message_t = "%s raises %s %s over %s head before sending it whistling down towards you!" % (caller.name, caller.db.genderp, weapon.db.short_name, caller.db.genderp)
            message_r = "%s raises %s %s over %s head before sending it whistling down towards %s!" % (caller.name, caller.db.genderp, weapon.db.short_name, caller.db.genderp, target.name)
        elif d3 == 2:
            message_c = "|wYou stab towards %s with your %s!|n" % (target.name, weapon.db.short_name)
            message_t = "%s stabs at you with %s %s!" % (
            caller.name, caller.db.genderp, weapon.db.short_name)
            message_r = "%s thrusts with %s %s towards %s!" % (
            caller.name, caller.db.genderp, weapon.db.short_name, target.name)
        else:
            message_c = "|wYou bring your %s around and slash at %s with all of your might!|n" % (weapon.db.short_name, target.name)
            message_t = "%s brings %s %s around before slashing at you with all of %s might!" % (caller.name, caller.db.genderp, weapon.db.short_name, caller.db.genderp)
            message_r = "%s brings %s %s around before slashing at %s with all of %s might!" % (
            caller.name, caller.db.genderp, weapon.db.short_name, target.name, caller.db.genderp)

    # And we're done!
    return message_c, message_t, message_r

def weapon_miss_messages(caller, target, weapon):
    "Returns a random one-handed sword attack message."

    d3 = randint(1, 3)

    message_c = "%s barely dodges your attack!" % (target.name)
    message_t = "You barely dodge %s attack!" % (english_utils.possessive(caller.name))
    message_r = "%s barely dodges %s attack!" % (target.name, english_utils.possessive(caller.name))

    if d3 == 1:
        message_c = "%s barely dodges your attack!" % (target.name)
        message_t = "You barely dodge %s attack!" % (english_utils.possessive(caller.name))
        message_r = "%s barely dodges %s %s!" % (target.name, english_utils.possessive(caller.name), weapon.db.short_name)
    elif d3 == 2:
        message_c = "%s deflects your %s with a deft parry!" % (target.name, weapon.db.short_name)
        message_t = "You deflect %s %s with a deft parry!" % (english_utils.possessive(caller.name), weapon.db.short_name)
        message_r = "%s deftly parries %s %s!" % (target.name, english_utils.possessive(caller.name), weapon.db.short_name)
    else:
        message_c = "%s evades your weapon!" % (target.name)
        message_t = "You evade %s deadly weapon!" % (english_utils.possessive(caller.name))
        message_r = "%s assaults %s with %s but %s evades %s!" % (caller.name, target.name, weapon.name, target.db.genders, caller.db.gendero)

    # And we're done!
    return message_c, message_t, message_r



#"Return how much a player can carry."
# def query_maximum_carry_weight(character):
#     return (character.db.weight / 10.0) + (character.db.strength * 2.2) + 20.0
#
# "Return how heavy an item is, including items it is carrying"
# def query_weight(item):
#
#     carried = item.contents
#     weight = 0.0
#
#     for weighed in carried:
#         weight += query_weight(weighed)
#
#     return item.db.weight + weight
#
# "Check if an item is too heavy to enter the inv of player."
# def check_weight(character, item):
#     if query_maximum_carry_weight(character) > query_weight(character) + item.db.weight:
#         return 1
#     return 0
#
# "Return the maximum health a player has."
# def query_maximum_health(character):
#     return character.db.constitution * 14.2 + 1000.0


# # Racial weight mapping
# racial_weight = {"dwarf": {"min": 150.0,
#                            "max": 300.0},
#                  "faeran": {"min": 100.0,
#                          "max": 200.0},
#                  "thrald": {"min": 80.0,
#                               "max": 280.0},
#                  "mill giant": {"min": 300.0,
#                                 "max": 900.0},
#                  "grishma": {"min": 200.0,
#                              "max": 500.0},
#                  "half-elf": {"min": 100.0,
#                               "max": 250.0},
#                  "human": {"min": 100.0,
#                            "max": 300.0},
#                  "rakhir": {"min": 150.0,
#                             "max": 300.0},
#                  "slime": {"min": 10.0,
#                            "max": 500.0},
#                  "big bird": {"min": 150.0,
#                               "max": 450.0},
#                  "masked being": {"min": 100.0,
#                                   "max": 300.0},
#                  "angel": {"min": 80.0,
#                            "max:": 280.0},
#                  "demon": {"min": 90.0,
#                            "max:": 400.0}
#                  }