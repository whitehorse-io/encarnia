from evennia import utils
from evennia.utils import search
from evennia.utils.spawner import spawn
import time


def clothing_list(caller):
    text = \
        """
        Welcome! Take a |wlook|n around to see which suits of armor are for sale today.

        Unfortunately, supplies and artisans are scarce right now so only leather armor is available.

        Note that you can |wquit|n the shop area at any time or after you're done.
        """
    options = ({"desc": "A long hooded black cloak: 7 silver.",
                "exec": _buy_black_hoodie},
               {"desc": "A snow white cloak: 7 silver.",
                "exec": _buy_white_hoodie},
               {"desc": "A woven green and grey, leaf-patterned cloak: 9 silver.",
                "exec": _buy_leaf_hoodie},
               {"desc": "A hooded scarlet cloak: 8 silver.",
                "exec": _buy_red_hoodie},
               {"desc": "A white woolen scarf: 4 silver.",
                "exec": _buy_white_scarf},
               {"desc": "A grey woolen scarf: 3 silver.",
                "exec": _buy_grey_scarf},
               {"desc": "A black silken scarf: 7 silver.",
                "exec": _buy_black_silken_scarf},
               {"desc": "A red silken scarf: 8 silver.",
                "exec": _buy_red_silken_scarf},
               {"desc": "Wooden sandals: 4 silver.",
                "exec": _buy_wooden_sandals},
               {"desc": "Laced leather boots: 6 silver.",
                "exec": _buy_laced_boots},
               {"desc": "Steel toed leather boots: 7 silver.",
                "exec": _buy_steel_toed_boots},
               {"desc": "Green woolen trousers: 6 silver.",
                "exec": _buy_green_trousers},
               {"desc": "Grey woolen trousers: 5 silver.",
                "exec": _buy_grey_trousers},
               {"desc": "Black silken breeches: 9 silver.",
                "exec": _buy_black_breeches},
               {"desc": "White leather breeches: 8 silver.",
                "exec": _buy_white_breeches},
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

def _buy_black_hoodie(caller):
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

    if caller.db.silver_carried < 7:
        caller.msg("You don't have enough silver - this costs 7 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 7
        caller.msg("The shopkeeper hands you a long hooded black cloak in return for 7 silver sovereigns.")
        item = spawn(black_hoodie, location=caller)

def _buy_white_hoodie(caller):
    white_hoodie = {"key": "a snowy white cloak",
                    "typeclass": "typeclasses.clothing.Clothes",
                    "aliases": ["hoodie"],
                    "desc": "This snowy white hoodie cloak looks pretty, so pretty.",
                    "wear_msg": "You sweep a snowy white cloak over your shoulders.",
                    "wear_msg_room_1": "sweeps a snowy white cloak over",
                    "wear_msg_room_2": "shoulders.",
                    "type": "cloak",
                    "location": caller,
                    "birth_time": time.time(),
                    "duration": 2000000.0}

    if caller.db.silver_carried < 7:
        caller.msg("You don't have enough silver - this costs 7 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 7
        caller.msg("The shopkeeper hands you a snowy white cloak in return for 7 silver sovereigns.")
        item = spawn(white_hoodie, location=caller)

def _buy_leaf_hoodie(caller):
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

    if caller.db.silver_carried < 9:
        caller.msg("You don't have enough silver - this costs 9 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 9
        caller.msg("The shopkeeper hands you a leather bandolier in return for 9 silver sovereigns.")
        item = spawn(leaf_hoodie, location=caller)

def _buy_red_hoodie(caller):
    red_hoodie = {"key": "a hooded scarlet cloak",
                  "typeclass": "typeclasses.clothing.Clothes",
                  "aliases": ["hoodie"],
                  "desc": "This fine scarlet cloak must have cost quite a bit!",
                  "wear_msg": "You sweep a hooded scarlet cloak over your shoulders.",
                  "wear_msg_room_1": "sweeps a hooded scarlet cloak over",
                  "wear_msg_room_2": "shoulders.",
                  "type": "cloak",
                  "location": caller,
                  "birth_time": time.time(),
                  "duration": 2000000.0}

    if caller.db.silver_carried < 8:
        caller.msg("You don't have enough silver - this costs 8 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 8
        caller.msg("The shopkeeper hands you a leather bandolier in return for 8 silver sovereigns.")
        item = spawn(red_hoodie, location=caller)

def _buy_riding_hoodie(caller):
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

    if caller.db.silver_carried < 6:
        caller.msg("You don't have enough silver - this costs 6 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 6
        caller.msg("The shopkeeper hands you a hooded red riding cloak in return for 6 silver sovereigns.")
        item = spawn(riding_hoodie, location=caller)

def _buy_white_scarf(caller):
    white_scarf = {"key": "a white woolen scarf",
                   "typeclass": "typeclasses.clothing.Clothes",
                   # "aliases" : ["scarf"],
                   "desc": "This pristine white woolen scarf looks warm indeed!",
                   "wear_msg": "You wrap a white woolen scarf around your neck.",
                   "wear_msg_room_1": "wraps a white woolen scarf around",
                   "wear_msg_room_2": "neck.",
                   "type": "scarf",
                   "location": caller,
                   "birth_time": time.time(),
                   "duration": 2000000.0}

    if caller.db.silver_carried < 4:
        caller.msg("You don't have enough silver - this costs 4 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 4
        caller.msg("The shopkeeper hands you a white woolen scarf in return for 4 silver sovereigns.")
        item = spawn(white_scarf, location=caller)

def _buy_grey_scarf(caller):
    grey_scarf = {"key": "a grey woolen scarf",
                  "typeclass": "typeclasses.clothing.Clothes",
                  # "aliases" : ["scarf"],
                  "desc": "This simple grey woolen scarf looks warm indeed!",
                  "wear_msg": "You wrap a grey woolen scarf around your neck.",
                  "wear_msg_room_1": "wraps a grey woolen scarf around",
                  "wear_msg_room_2": "neck.",
                  "type": "scarf",
                  "location": caller,
                  "birth_time": time.time(),
                  "duration": 2000000.0}

    if caller.db.silver_carried < 3:
        caller.msg("You don't have enough silver - this costs 3 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 3
        caller.msg("The shopkeeper hands you a grey woolen scarf in return for 3 silver sovereigns.")
        item = spawn(grey_scarf, location=caller)

def _buy_black_silken_scarf(caller):
    black_silken_scarf = {"key": "a black silken scarf",
                          "typeclass": "typeclasses.clothing.Clothes",
                          # "aliases" : ["scarf"],
                          "desc": "This black silken scarf looks stylish!",
                          "wear_msg": "You wrap a black silken scarf around your neck.",
                          "wear_msg_room_1": "wraps a black silken scarf around",
                          "wear_msg_room_2": "neck.",
                          "type": "scarf",
                          "location": caller,
                          "birth_time": time.time(),
                          "duration": 2000000.0}

    if caller.db.silver_carried < 7:
        caller.msg("You don't have enough silver - this costs 7 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 7
        caller.msg("The shopkeeper hands you a black silken scarf in return for 7 silver sovereigns.")
        item = spawn(black_silken_scarf, location=caller)

def _buy_red_silken_scarf(caller):
    red_silken_scarf = {"key": "a red silken scarf",
                        "typeclass": "typeclasses.clothing.Clothes",
                        # "aliases" : ["scarf"],
                        "desc": "This red silken scarf looks stylish!",
                        "wear_msg": "You wrap a red silken scarf around your neck.",
                        "wear_msg_room_1": "wraps a red silken scarf around",
                        "wear_msg_room_2": "neck.",
                        "type": "scarf",
                        "location": caller,
                        "birth_time": time.time(),
                        "duration": 2000000.0}

    if caller.db.silver_carried < 8:
        caller.msg("You don't have enough silver - this costs 8 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 8
        caller.msg("The shopkeeper hands you a red silken scarf in return for 8 silver sovereigns.")
        item = spawn(red_silken_scarf, location=caller)

def _buy_wooden_sandals(caller):
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

    if caller.db.silver_carried < 5:
        caller.msg("You don't have enough silver - this costs 5 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 5
        caller.msg("The shopkeeper hands you a leather bandolier in return for 5 silver sovereigns.")
        item = spawn(wooden_sandals, location=caller)

def _buy_laced_boots(caller):
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

    if caller.db.silver_carried < 6:
        caller.msg("You don't have enough silver - this costs 6 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 6
        caller.msg("The shopkeeper hands you some laced leather boots in return for 6 silver sovereigns.")
        item = spawn(laced_boots, location=caller)

def _buy_steel_toed_boots(caller):
    steel_toed_boots = {"key": "steel toed leather boots",
                        "typeclass": "typeclasses.clothing.Clothes",
                        "aliases": ["shoes"],
                        "desc": "These steel-toed leather boots look very sturdy!",
                        "wear_msg": "You squeeze into a pair of steel-toed leather boots.",
                        "wear_msg_room_1": "squeezes a pair of steel-toed leather boots onto",
                        "wear_msg_room_2": "feet.",
                        "type": "shoes",
                        "location": caller,
                        "birth_time": time.time(),
                        "duration": 2000000.0}

    if caller.db.silver_carried < 8:
        caller.msg("You don't have enough silver - this costs 8 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 8
        caller.msg("The shopkeeper hands you some steel toed leather boots in return for 8 silver sovereigns.")
        item = spawn(steel_toed_boots, location=caller)

def _buy_green_trousers(caller):
    green_trousers = {"key": "woven green woolen trousers",
                      "typeclass": "typeclasses.clothing.Clothes",
                      "aliases": ["pants"],
                      "desc": "These green woolen trousers look sturdy and warm.",
                      "wear_msg": "You pull on a pair of woven green woolen trousers.",
                      "wear_msg_room_1": "pulls on a pair of woven green woolen trousers.",
                      "type": "pants",
                      "location": caller,
                      "birth_time": time.time(),
                      "duration": 2000000.0}

    if caller.db.silver_carried < 6:
        caller.msg("You don't have enough silver - this costs 6 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 6
        caller.msg("The shopkeeper hands you a leather bandolier in return for 6 silver sovereigns.")
        item = spawn(green_trousers, location=caller)

def _buy_grey_trousers(caller):
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

    if caller.db.silver_carried < 5:
        caller.msg("You don't have enough silver - this costs 5 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 5
        caller.msg("The shopkeeper hands you a leather bandolier in return for 5 silver sovereigns.")
        item = spawn(grey_trousers, location=caller)

def _buy_black_breeches(caller):
    black_silk_breeches = {"key": "black silken riding breeches",
                           "typeclass": "typeclasses.clothing.Clothes",
                           "aliases": ["pants"],
                           "desc": "These black silken breeches look good but might not stand up well to time.",
                           "wear_msg": "You pull on a pair of black silken riding breeches.",
                           "wear_msg_room_1": "pulls on a pair of black silken riding breeches.",
                           "type": "pants",
                           "location": caller,
                           "birth_time": time.time(),
                           "duration": 2000000.0}

    if caller.db.silver_carried < 9:
        caller.msg("You don't have enough silver - this costs 9 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 9
        caller.msg("The shopkeeper hands you a leather bandolier in return for 9 silver sovereigns.")
        item = spawn(black_silk_breeches, location=caller)

def _buy_white_breeches(caller):
    white_leather_breeches = {"key": "white leather riding breeches",
                              "typeclass": "typeclasses.clothing.Clothes",
                              "aliases": ["pants"],
                              "desc": "These white leather breeches look sturdy, if not sturdy enough to act as armor.",
                              "wear_msg": "You pull on a pair of white leather riding breeches.",
                              "wear_msg_room_1": "pulls on a pair of white leather riding breeches.",
                              "type": "pants",
                              "location": caller,
                              "birth_time": time.time(),
                              "duration": 2000000.0}

    if caller.db.silver_carried < 8:
        caller.msg("You don't have enough silver - this costs 8 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 8
        caller.msg("The shopkeeper hands you a leather bandolier in return for 8 silver sovereigns.")
        item = spawn(white_leather_breeches, location=caller)