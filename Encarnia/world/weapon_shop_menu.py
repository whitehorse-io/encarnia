from evennia import utils
from evennia.utils import search
from evennia.utils.spawner import spawn
import time

def weapon_list(caller):
    text = \
    """
    Welcome! Take a |wlook|n around to see which weapons are for sale today.
    
    Note that you can |wquit|n the shop area at any time or after you're done.
    """
    options = ({"desc": "A ruddy bronze broadsword: 10 silver.",
                "exec": _buy_broadsword},
               {"desc": "A steel gladius: 9 silver.",
                       "exec": _buy_gladius},
               {"desc": "A cold iron axe: 7 silver.",
                "exec": _buy_axe},
               {"desc": "A long hunter's spear: 6 silver.",
                        "exec": _buy_spear},
               {"desc": "A cheap dagger: 4 silver.",
                        "exec": _buy_dagger},
               {"desc": "A serrated steel katana: 14 silver",
                        "exec": _buy_katana})

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

def _buy_broadsword(caller):
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

    if caller.db.silver_carried < 10:
        caller.msg("You don't have enough silver - this costs 10 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 10
        caller.msg("The shopkeeper hands you a ruddy bronze broadsword in return for 10 silver sovereigns.")
        wpn = spawn(bronze_broadsword, location=caller)

def _buy_gladius(caller):
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

    if caller.db.silver_carried < 9:
        caller.msg("You don't have enough silver - this costs 9 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 9
        caller.msg("The shopkeeper hands you a sturdy steel gladius in return for 9 silver sovereigns.")
        wpn = spawn(steel_gladius, location=caller)

def _buy_axe(caller):
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

    if caller.db.silver_carried < 7:
        caller.msg("You don't have enough silver - this costs 7 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 7
        caller.msg("The shopkeeper hands you a cold iron axe in return for 7 silver sovereigns.")
        wpn = spawn(cold_iron_axe, location=caller)

def _buy_spear(caller):
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

    if caller.db.silver_carried < 6:
        caller.msg("You don't have enough silver - this costs 6 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 6
        caller.msg("The shopkeeper hands you a long hunter's spear in return for 6 silver sovereigns.")
        wpn = spawn(hunters_spear, location=caller)

def _buy_dagger(caller):
    cheap_dagger = {"key": "a cheap iron dagger",
                    "typeclass": "typeclasses.arms.Weapons",
                    "aliases": ["weapon"],
                    "short_name": "iron dagger",
                    "desc": "This \"happy\" iron dagger is heavier than it looks but would a useful weapon in close quarters.\nThis weapon has the following attributes:\nOpen Terrain: -5, Cluttered Terrain: +10, Narrow Terrain: 0.\nBalance: Very light.\nDamage: Very low.",
                    "open_terrain": -5,
                    "cluttered_terrain": 10,
                    "narrow_terrain": 0,
                    "damage_multiplier": 0.70,
                    "balance_duration_change": -1.5,
                    "weapon_type": "dagger",
                    "location": caller,
                    "birth_time": time.time(),
                    "duration": 2000000.0}

    if caller.db.silver_carried < 4:
        caller.msg("You don't have enough silver - this costs 4 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 4
        caller.msg("The shopkeeper hands you a cheap iron dagger in return for 4 silver sovereigns.")
        wpn = spawn(cheap_dagger, location=caller)

def _buy_katana(caller):
    curved_katana = {"key": "a serrated steel katana",
                     "typeclass": "typeclasses.arms.Weapons",
                     "aliases": ["sword", "weapon"],
                     "short_name": "curved katana",
                     "desc": "This long, curved but thin sword is made from sturdy steel. It has to be due to its unique shape, otherwise it would break too easily in combat. It looks as if it could deal heavy damage, provided there is enough room to wield it properly.\nThis weapon has the following attributes:\nOpen Terrain: +10, Cluttered Terrain: -5, Narrow Terrain: 0.\nBalance: Very heavy.\nDamage: Very high.",
                     "open_terrain": 10,
                     "cluttered_terrain": -5,
                     "narrow_terrain": 0,
                     "damage_multiplier": 1.25,
                     "balance_duration_change": 1.0,
                     "weapon_type": "2hsword",
                     "location": caller,
                     "birth_time": time.time(),
                     "duration": 2000000.0}

    if caller.db.silver_carried < 14:
        caller.msg("You don't have enough silver - this costs 14 silver!")
    else:
        caller.db.silver_carried = caller.db.silver_carried - 14
        caller.msg("The shopkeeper hands you a serrated steel katana in return for 10 silver sovereigns.")
        wpn = spawn(curved_katana, location=caller)