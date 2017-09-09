from evennia import utils
from evennia.utils import search
from evennia.utils.spawner import spawn
import time


def armor_list(caller):
    text = \
        """
        Welcome! Take a |wlook|n around to see which suits of armor are for sale today.
        
        Unfortunately, supplies and artisans are scarce right now so only leather armor is available.
        
        Note that you can |wquit|n the shop area at any time or after you're done.
        """
    options = ({"desc": "A scuffed, poorly proportioned suit of leather armor: 10 silver.",
                "exec": _buy_human_male_armor},
               {"desc": "A revealing, questionably protective suit of leather armor: 10 silver.",
                "exec": _buy_human_female_armor},
               {"desc": "A low quality suit of full body leather armor: 11 silver.",
                "exec": _buy_full_leather_armor},
               {"desc": "A black leather weapon girdle: 7 silver.",
                "exec": _buy_black_girdle},
               {"desc": "A white leather weapon girdle: 7 silver.",
                "exec": _buy_white_girdle},
               {"desc": "An iron ringed weapon girdle: 7 silver.",
                "exec": _buy_iron_girdle},
               {"desc": "A sturdy dwarven girdle: 8 silver.",
                "exec": _buy_dwarven_girdle},
               {"desc": "A leather tool belt and weapon girdle: 8 silver.",
                "exec": _buy_toolbelt_girdle},
               {"desc": "A leather bandolier: 7 silver.",
                "exec": _buy_leather_bandolier},
                )

    return text, options


# def produce_weapon(self, caller):
#     """
#     This will produce a new weapon from the rack,
#     assuming the caller hasn't already gotten one. When
#     doing so, the caller will get Tagged with the id
#     of this rack, to make sure they cannot keep
#     pulling weapons from it indefinitely.
#     """
#
#     # use the spawner to create a new Weapon from the
#     # spawner dictionary, tag the caller
#     prototype = random.choice(self.db.available_weapons)
#     wpn = spawn(WEAPON_PROTOTYPES[prototype], prototype_parents=WEAPON_PROTOTYPES)[0]
#     caller.tags.add(rack_id, category="tutorial_world")
#     wpn.location = caller
#     caller.msg(self.db.get_weapon_msg % wpn.key)

def _buy_human_male_armor(caller):
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

    if caller.db.silver_carried < 10:
        caller.msg("You don't have enough silver - this costs 10 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 10
        caller.msg("The shopkeeper hands you some scuffed leather armor in return for 10 silver sovereigns.")
        item = spawn(male_newbie_armor, location=caller)


def _buy_human_female_armor(caller):
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

    if caller.db.silver_carried < 10:
        caller.msg("You don't have enough silver - this costs 10 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 10
        caller.msg("The shopkeeper hands you some revealing leather armor in return for 10 silver sovereigns.")
        item = spawn(female_newbie_armor, location=caller)


def _buy_full_leather_armor(caller):
    full_leathers = {"key": "a full body suit of woven leather strips",
                     "typeclass": "typeclasses.clothing.Clothes",
                     "aliases": ["armour", "armor"],
                     "desc": "This suit of leather \"armor\" covers the whole body from ankles to neck but its long-term viability is questionable; it looks like it was made in a rush.",
                     "wear_msg": "You wrap yourself up into a full body suit of woven leather strips.",
                     "wear_msg_room_1": "wraps a full body suit of woven leather strips around",  # name
                     "wear_msg_room_1": "body.",  # gender (his or her)
                     "type": "armor",
                     "armor_value": 8,
                     "armor_type": "leather",
                     "location": caller,
                     "birth_time": time.time(),
                     "duration": 2000000.0}

    if caller.db.silver_carried < 11:
        caller.msg("You don't have enough silver - this costs 11 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 11
        caller.msg("The shopkeeper hands you a suit of full leather armor in return for 11 silver sovereigns.")
        item = spawn(full_leathers, location=caller)

def _buy_black_girdle(caller):
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

    if caller.db.silver_carried < 7:
        caller.msg("You don't have enough silver - this costs 7 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 7
        caller.msg("The shopkeeper hands you a black leather weapon girdle in return for 7 silver sovereigns.")
        item = spawn(black_leather_girdle, location=caller)

def _buy_white_girdle(caller):
    white_leather_girdle = {"key": "a white leather weapon girdle",
                            "typeclass": "typeclasses.clothing.Clothes",
                            # "aliases" : ["armour"],
                            "desc": "This sturdy girdle acts as a belt, bodily protection and a place to affix sheaths or other kinds of equipment onto the body. It includes some efficient-looking leather suspenders to help support the weight.",
                            "wear_msg": "You strap on a white leather weapon girdle.",
                            "wear_msg_room_1": "straps on a white leather weapon girdle.",  # name
                            "type": "girdle",
                            "location": caller,
                            "birth_time": time.time(),
                            "duration": 2000000.0}

    if caller.db.silver_carried < 7:
        caller.msg("You don't have enough silver - this costs 7 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 7
        caller.msg("The shopkeeper hands you a white leather weapon girdle in return for 7 silver sovereigns.")
        item = spawn(white_leather_girdle, location=caller)

def _buy_iron_girdle(caller):
    iron_ringed_girdle = {"key": "an iron_ringed leather weapon girdle",
                          "typeclass": "typeclasses.clothing.Clothes",
                          # "aliases" : ["armour"],
                          "desc": "This sturdy girdle acts as a belt, bodily protection and a place to affix sheaths or other kinds of equipment onto the body. It includes some efficient-looking leather suspenders to help support the weight.",
                          "wear_msg": "You strap on an iron-ringed leather weapon girdle.",
                          "wear_msg_room_1": "straps on a iron-ringed leather weapon girdle.",  # name
                          "type": "girdle",
                          "location": caller,
                          "birth_time": time.time(),
                          "duration": 2000000.0}

    if caller.db.silver_carried < 7:
        caller.msg("You don't have enough silver - this costs 7 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 7
        caller.msg("The shopkeeper hands you an iron-ringed weapon girdle in return for 7 silver sovereigns.")
        item = spawn(iron_ringed_girdle, location=caller)

def _buy_dwarven_girdle(caller):
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

    if caller.db.silver_carried < 8:
        caller.msg("You don't have enough silver - this costs 8 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 8
        caller.msg("The shopkeeper hands you a sturdy dwarven girdle in return for 8 silver sovereigns.")
        item = spawn(sturdy_dwarven_girdle, location=caller)

def _buy_toolbelt_girdle(caller):
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

    if caller.db.silver_carried < 8:
        caller.msg("You don't have enough silver - this costs 8 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 8
        caller.msg("The shopkeeper hands you a cold iron axe in return for 8 silver sovereigns.")
        item = spawn(toolbelt_girdle, location=caller)

def _buy_leather_bandolier(caller):
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

    if caller.db.silver_carried < 7:
        caller.msg("You don't have enough silver - this costs 7 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 7
        caller.msg("The shopkeeper hands you a leather bandolier in return for 7 silver sovereigns.")
        item = spawn(bandolier_girdle, location=caller)