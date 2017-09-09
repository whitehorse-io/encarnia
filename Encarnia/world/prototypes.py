import time

# in a module Evennia looks at for prototypes,
# (like mygame/server/conf/prototypes.py)

dropped_silver = {
        "key": "a single silver sovereign",
        "aliases": ["money", "coins"],
        "desc": "Silver sovereigns have the likeness of a mighty lion engraved upon their surface on one side and the Tower of Corinth on the other.",
        #self.location = caller.location
        "coins_value": 1}

giant_rat = {
    "key": "a giant rat",

    "locks": "get: perm(Wizards)",

    "typeclass": "typeclasses.npcs.Combat_Mob",

    "aliases": [],

    "live_name": "a giant rat",
    "defeated_name": "the mangled remains of some large vermin",  # must not have 'rat' in it or it can't be targetted!
    "alive": True,
    "desc": "This mangy beast slavers and nibbles upon anything nearby with its giant incisors.",

    "health": 35,
    "max_health": 35,

    "damage_amount": 15,

    "ticker_speed": 3,  # how often it attempts to attack or move/attack if a target is not found.  This will only fire so many times before they 'forget'.
    "counter_attack_chance": False,  # integer chance this npc will trigger a counter-attack.  Defaults as false.
    "respawn_speed": 600,  # SHOULD BE A MULTIPLE OF 100
    "tries": 3,  # how long it will spend trying to find its attacker before shutting down.

    "level": 10,  # this is the relative level of the creature
    "exp_multiplier": 4,  # If you're under the level, subtract player level from NPC level and multiply by the multiplier.
    "exp_max_level": 20,  # At this level you won't gain any experience from killing this NPC.

    "home_location": "#2",  # This should be set!

    # So normally any kill is worth 1% exp.
    # But if your level is under the npc's level, you get a bonus
    # The bonus is level difference * multiplier.

    # This multiplier equation could similarly be used when attacking people below your current level, so you might
    # level up multiple times from killing a high-level person.

    "offended_by": [],

    "lootable": False,  # can be LOOTed for silver.
    "looted_yet": False,
    "silver_amount": 0,

    "skinnable": True,  # can be SKINNED for a pelt or skin item.
    "skinned_yet": False,
    "pelt_name": "a giant rat pelt",

    "attack_message_1": "A giant rat hurls itself bodily into",
    "attack_message_2": "A giant rat claws and bites at",
    "attack_message_3": "With a resounding crunching sound, a giant rat bites into",
    }


######
# WHN: Consumables here.
######
crude_small_pelt = {"key":"a small and crude fur pelt",
              "typeclass": "typeclasses.objects.Object",
                     "desc": "This rat pelt was barely removed successfully and it shows.",
                     "birth_time": time.time(),
                     "duration": 2000000.0}

small_pelt = {"key":"a small fur pelt",
              "desc": "This is a generic giant rat pelt; not too high in quality but not too bad either.",
                     "birth_time": time.time(),
                     "duration": 2000000.0}

fine_small_pelt = {"key":"a small but fine fur pelt",
              "typeclass": "typeclasses.objects.Object",
              "desc": "This is an exemplary giant rat pelt, removed from a mighty rat by a skilled skinner.",
                     "birth_time": time.time(),
                     "duration": 2000000.0}

######
# WHN: Weapons start here.
######
bronze_broadsword = {"key":"a ruddy bronze broadsword",
              "typeclass": "typeclasses.arms.Weapons",
              "aliases" : ["sword", "weapon"],
              "short_name": "ruddy bronze broadsword",
              "desc": "This sharp, thick broadsword is made from fine, if expensive bronze.\nThis weapon has the following attributes:\nOpen Terrain: +3, Cluttered Terrain: +2, Narrow Terrain: 0.\nBalance: Neutral.\nDamage: Average.",
              "open_terrain": 3,
                     "cluttered_terrain": 2,
                     "narrow_terrain": 0,
                     "damage_multiplier": 1.0,
                     "balance_duration_change": 0.0,
                     "weapon_type": "1hsword",
                     "birth_time": time.time(),
                     "duration": 2000000.0}


steel_gladius = {"key":"a sturdy steel gladius",
              "typeclass": "typeclasses.arms.Weapons",
              "aliases" : ["sword", "weapon"],
              "short_name": "steel gladius",
                 "desc": "This short sword is good for both stabbing and slashing. It is made from reliable steel and has leather wrapped about the handle above a round pomel.\nThis weapon has the following attributes:\nOpen Terrain: +3, Cluttered Terrain: +2, Narrow Terrain: 0.\nBalance: Neutral.\nDamage: Average.",
              "open_terrain": 3,
                     "cluttered_terrain": 2,
                     "narrow_terrain": 0,
                     "damage_multiplier": 1.0,
                     "balance_duration_change": 0.0,
                     "weapon_type": "1hsword",
                     "birth_time": time.time(),
                     "duration": 2000000.0}

cold_iron_axe = {"key":"a cold iron axe",
              "typeclass": "typeclasses.arms.Weapons",
              "aliases" : ["weapon"],
              "short_name": "iron axe",
                 "desc": "This heavy axe is made from cold iron, making it affordable if somewhat heavy.\nThis weapon has the following attributes:\nOpen Terrain: +5, Cluttered Terrain: 0, Narrow Terrain: -5.\nBalance: Heavy.\nDamage: High.",
              "open_terrain": 5,
                     "cluttered_terrain": 0,
                     "narrow_terrain": -5,
                     "damage_multiplier": 1.15,
                     "balance_duration_change": 0.5,
                     "weapon_type": "1haxe",
                     "birth_time": time.time(),
                     "duration": 2000000.0}

hunters_spear = {"key":"a long hunter's spear",
              "typeclass": "typeclasses.arms.Weapons",
              "aliases" : ["weapon"],
              "short_name": "hunter's spear",
"desc": "This light spear has a sharp steel tip, as well as a leather strap for being secured when carrying and a leather cover for the head.\nThis weapon has the following attributes:\nOpen Terrain: 0, Cluttered Terrain: 0, Narrow Terrain: +10.\nBalance: Light.\nDamage: Low.",
              "open_terrain": 0,
                     "cluttered_terrain": 0,
                     "narrow_terrain": 10,
                     "damage_multiplier": 0.85,
                     "balance_duration_change": -1,
                     "weapon_type": "1hspear",
                     "birth_time": time.time(),
                     "duration": 2000000.0}

cheap_dagger = {"key":"a cheap iron dagger",
              "typeclass": "typeclasses.arms.Weapons",
              "aliases" : ["weapon"],
              "short_name": "iron dagger",
"desc": "This \"happy\" iron dagger is heavier than it looks but would a useful weapon in close quarters.\nThis weapon has the following attributes:\nOpen Terrain: -5, Cluttered Terrain: +10, Narrow Terrain: 0.\nBalance: Very light.\nDamage: Very low.",
              "open_terrain": -5,
                     "cluttered_terrain": 10,
                     "narrow_terrain": 0,
                     "damage_multiplier": 0.70,
                     "balance_duration_change": -1.5,
                     "weapon_type": "dagger",
                     "birth_time": time.time(),
                     "duration": 2000000.0}

curved_katana = {"key":"a serrated steel katana",
              "typeclass": "typeclasses.arms.Weapons",
              "aliases" : ["sword", "weapon"],
              "short_name": "curved katana",
"desc": "This long, curved but thin sword is made from sturdy steel. It has to be due to its unique shape, otherwise it would break too easily in combat. It looks as if it could deal heavy damage, provided there is enough room to wield it properly.\nThis weapon has the following attributes:\nOpen Terrain: +10, Cluttered Terrain: -5, Narrow Terrain: 0.\nBalance: Very heavy.\nDamage: Very high.",
              "open_terrain": 10,
                     "cluttered_terrain": -5,
                     "narrow_terrain": 0,
                     "damage_multiplier": 1.25,
                     "balance_duration_change": 1.0,
                     "weapon_type": "2hsword",
                     "birth_time": time.time(),
                     "duration": 2000000.0}

######
# WHN: Armor starts here.
######
# lion_leather = # same as clothing but has an armor_value number.

male_newbie_armor = {"key": "some scuffed leather armor with an overly high and tight neck",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["armour"],
                "desc" : "This suit of armor looks sturdy enough but it was either made for a very strangely proportioned person or some error happened during its fabrication.  This is clear because the neck is strangely small and too tall.",
                "wear_msg" : "You squeeze into a scuffed suit of leather armor.",
                "wear_msg_room_1" : "squeezes into a scuffed suit of leather armor.", # name
                "type" : "armor",
                "armor_value" : 8,
                "armor_type": "leather",
                "birth_time": time.time(),
                "duration": 2000000.0}

female_newbie_armor = {"key": "some revealing leather armor that doesn't protect very much",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["armour"],
                "desc" : "This suit of armor looks like it was made as a joke, or perhaps by someone who didn't intend to use it in a fight. Most of the chest and back are fully exposed and it doesn't cover the legs at all.",
                "wear_msg" : "You squeeze into a revealing suit of leather \"armor.\"",
                "wear_msg_room_1" : "squeezes into a scuffed suit of leather \"armor.\"", # name
                "type" : "armor",
                "armor_value" : 8,
                "armor_type": "leather",
                "birth_time": time.time(),
                "duration": 2000000.0}

grandmas_newbie_armor = {"key": "grandma's old leather armor",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["armour"],
                "desc" : "This ancient suit of leather armor is about the right size for a female dwarf. The coverage provided and workmanship are good but the item's age is showing.",
                "wear_msg" : "You squeeze into an ancient suit of leather armor.",
                "wear_msg_room_1" : "squeezes into an ancient suit of leather armor.", # name
                "type" : "armor",
                "armor_value" : 8,
                "armor_type": "leather",
                "birth_time": time.time(),
                "duration": 2000000.0}

grandpas_newbie_armor = {"key": "grandpa's old leather armor",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["armour"],
                "desc" : "This ancient suit of leather armor is about the right size for a male dwarf. The coverage provided and workmanship are good but the item's age is showing.",
                "wear_msg" : "You squeeze into an ancient suit of leather armor.",
                "wear_msg_room_1" : "squeezes into an ancient suit of leather armor.", # name
                "type" : "armor",
                "armor_value" : 8,
                "armor_type": "leather",
                "birth_time": time.time(),
                "duration": 2000000.0}

full_leathers = {"key": "a full body suit of woven leather strips",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["armour", "armor"],
                "desc" : "This suit of leather \"armor\" covers the whole body from ankles to neck but its long-term viability is questionable; it looks like it was made in a rush.",
                "wear_msg" : "You wrap yourself up into a full body suit of woven leather strips.",
                "wear_msg_room_1" : "wraps a full body suit of woven leather strips around", # name
                "wear_msg_room_1" : "body.", # gender (his or her)
                "type" : "armor",
                "armor_value" : 8,
                "armor_type": "leather",
                "birth_time": time.time(),
                "duration": 2000000.0}

scavenged_leathers = {"key": "a suit of bloodstained leather armor",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["armour"],
                "desc" : "This suit of leather armor covers much of the body but appears to have stitched back together at least once; it's unclear whether the blood came from a previous owner.",
                "wear_msg" : "You strap yourself into a bloodstained body of leather armor.",
                "wear_msg_room_1" : "straps into a bloodstained suit of leather armor.", # name
                "type" : "armor",
                "armor_value" : 8,
                "armor_type": "leather",
                "birth_time": time.time(),
                "duration": 2000000.0}

######
# WHN: Girdles start here.
######

black_leather_girdle = {"key": "a black leather weapon girdle",
              "typeclass": "typeclasses.clothing.Clothes",
                #"aliases" : ["armour"],
                "desc" : "This sturdy girdle acts as a belt, bodily protection and a place to affix sheaths or other kinds of equipment onto the body. It includes some efficient-looking leather suspenders to help support the weight.",
                "wear_msg" : "You strap on a black leather weapon girdle.",
                "wear_msg_room_1" : "straps on a black leather weapon girdle.", # name
                "type" : "girdle",
                "birth_time": time.time(),
                "duration": 2000000.0}

white_leather_girdle = {"key": "a white leather weapon girdle",
              "typeclass": "typeclasses.clothing.Clothes",
                #"aliases" : ["armour"],
                "desc" : "This sturdy girdle acts as a belt, bodily protection and a place to affix sheaths or other kinds of equipment onto the body. It includes some efficient-looking leather suspenders to help support the weight.",
                "wear_msg" : "You strap on a white leather weapon girdle.",
                "wear_msg_room_1" : "straps on a white leather weapon girdle.", # name
                "type" : "girdle",
                "birth_time": time.time(),
                "duration": 2000000.0}

iron_ringed_girdle = {"key": "an iron_ringed leather weapon girdle",
              "typeclass": "typeclasses.clothing.Clothes",
                #"aliases" : ["armour"],
                "desc" : "This sturdy girdle acts as a belt, bodily protection and a place to affix sheaths or other kinds of equipment onto the body. It includes some efficient-looking leather suspenders to help support the weight.",
                "wear_msg" : "You strap on an iron-ringed leather weapon girdle.",
                "wear_msg_room_1" : "straps on a iron-ringed leather weapon girdle.", # name
                "type" : "girdle",
                "birth_time": time.time(),
                "duration": 2000000.0}

sturdy_dwarven_girdle = {"key": "a sturdy dwarven weapon girdle",
              "typeclass": "typeclasses.clothing.Clothes",
                #"aliases" : ["armour"],
                "desc" : "This sturdy girdle acts as a belt, bodily protection and a place to affix sheaths or other kinds of equipment onto the body. It includes some efficient-looking leather suspenders to help support the weight.",
                "wear_msg" : "You strap on a sturdy dwarven weapon girdle.",
                "wear_msg_room_1" : "straps on a sturdy dwarven weapon girdle.", # name
                "type" : "girdle",
                "birth_time": time.time(),
                "duration": 2000000.0}

makeshift_girdle = {"key": "a makeshift weapon girdle",
              "typeclass": "typeclasses.clothing.Clothes",
                #"aliases" : ["armour"],
                "desc" : "This makeshift girdle acts as a belt, bodily protection and a place to affix sheaths or other kinds of equipment onto the body. It includes some efficient-looking leather suspenders to help support the weight.",
                "wear_msg" : "You strap on a makeshift weapon girdle.",
                "wear_msg_room_1" : "straps on a makeshift weapon girdle.", # name
                "type" : "girdle",
                "birth_time": time.time(),
                "duration": 2000000.0}

toolbelt_girdle = {"key": "a leather tool belt and weapon girdle",
              "typeclass": "typeclasses.clothing.Clothes",
                #"aliases" : ["armour"],
                "desc" : "This sturdy girdle acts as a belt, bodily protection and a place to affix sheaths or other kinds of equipment onto the body. It includes some efficient-looking leather suspenders to help support the weight and pockets for other kinds of tools or supplies.",
                "wear_msg" : "You strap on a leather tool belt and weapon girdle.",
                "wear_msg_room_1" : "straps on a leather tool belt and  weapon girdle.", # name
                "type" : "girdle",
                "birth_time": time.time(),
                "duration": 2000000.0}

bandolier_girdle = {"key": "a leather bandolier",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["girdle"],
                "desc" : "This sturdy bandolier goes over the shoulder instead of around the waste, but otherwise performs the same purpose that a weapon girdle would, to hold sheaths for weapons.",
                "wear_msg" : "You strap on a leather tool belt and weapon girdle.",
                "wear_msg_room_1" : "straps on a leather tool belt and  weapon girdle.", # name
                "type" : "girdle",
                "birth_time": time.time(),
                "duration": 2000000.0}

######
# WHN: Canteens starts here.
######
# leather_waterskin = {"key": "a leather waterskin",
#               "typeclass": "typeclasses.canteens.Canteen",
#                 #"aliases" : ["armour"],
#                 "desc" : "This leather waterskin will hold a fair amount of drink without easily springing a leak or being too heavy.",
#                 "max_sips" : 4,
#                 "birth_time": time.time(),
#                 "duration": 2000000.0}
#
# leather_wineskin = {"key": "a leather wineskin",
#               "typeclass": "typeclasses.canteens.Canteen",
#                 #"aliases" : ["armour"],
#                 "desc" : "This leather wineskin will hold a fair amount of drink without easily springing a leak or being too heavy.",
#                 "max_sips" : 4,
#                 "birth_time": time.time(),
#                 "duration": 2000000.0}
#
# silvery_canteen = {"key": "a silvery canteen",
#               "typeclass": "typeclasses.canteens.Canteen",
#                 #"aliases" : ["armour"],
#                 "desc" : "This silvery canteen is made from an unknown metal, but it seems as if it will hold a fair amount of drink without easily springing a leak or being too heavy.",
#                 "max_sips" : 4,
#                 "birth_time": time.time(),
#                 "duration": 2000000.0}


######
# WHN: Clothing starts here.
######
black_hoodie = {"key": "a long hooded black cloak",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["hoodie"],
                "desc" : "This long black hoodie cloak looks dramatic, so dramatic.",
                "wear_msg" : "You sweep a hooded black cloak over your shoulders.",
                "wear_msg_room_1" : "sweeps a hooded black cloak over", # name
                "wear_msg_room_2" : "shoulders.", # his or her
                "type" : "cloak",
                "birth_time": time.time(),
                "duration": 2000000.0}

white_hoodie = {"key": "a snowy white cloak",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["hoodie"],
                "desc" : "This snowy white hoodie cloak looks pretty, so pretty.",
                "wear_msg" : "You sweep a snowy white cloak over your shoulders.",
                "wear_msg_room_1" : "sweeps a snowy white cloak over",
                "wear_msg_room_2" : "shoulders.",
                "type" : "cloak",
                "birth_time": time.time(),
                "duration": 2000000.0}

leaf_hoodie = {"key": "a woven green and grey, leaf-patterned cloak",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["hoodie"],
                "desc" : "This woven green and grey cloak shows exceptional workmanship in its patterned leaves.",
                "wear_msg" : "You sweep a woven green and grey, leaf-patterned cloak over your shoulders.",
                "wear_msg_room_1" : "sweeps a woven green and grey, leaf-patterned cloak over",
                "wear_msg_room_2" : "shoulders.",
                "type" : "cloak",
                "birth_time": time.time(),
                "duration": 2000000.0}

red_hoodie = {"key": "a hooded scarlet cloak",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["hoodie"],
                "desc" : "This fine scarlet cloak must have cost quite a bit!",
                "wear_msg" : "You sweep a hooded scarlet cloak over your shoulders.",
                "wear_msg_room_1" : "sweeps a hooded scarlet cloak over",
                "wear_msg_room_2" : "shoulders.",
                "type" : "cloak",
                "birth_time": time.time(),
                "duration": 2000000.0}

riding_hoodie = {"key": "a hooded red riding cloak",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["hoodie"],
                "desc" : "This hooded red cloak looks like it has seen the road before.",
                "wear_msg" : "You sweep a hooded red riding cloak over your shoulders.",
                "wear_msg_room_1" : "sweeps a hooded red riding cloak over",
                "wear_msg_room_2" : "shoulders.",
                "type" : "cloak",
                "birth_time": time.time(),
                "duration": 2000000.0}

white_scarf = {"key": "a white woolen scarf",
              "typeclass": "typeclasses.clothing.Clothes",
                #"aliases" : ["scarf"],
                "desc" : "This pristine white woolen scarf looks warm indeed!",
                "wear_msg" : "You wrap a white woolen scarf around your neck.",
                "wear_msg_room_1" : "wraps a white woolen scarf around",
                "wear_msg_room_2" : "neck.",
                "type" : "scarf",
                "birth_time": time.time(),
                "duration": 2000000.0}

grey_scarf = {"key": "a grey woolen scarf",
              "typeclass": "typeclasses.clothing.Clothes",
                #"aliases" : ["scarf"],
                "desc" : "This simple grey woolen scarf looks warm indeed!",
                "wear_msg" : "You wrap a grey woolen scarf around your neck.",
                "wear_msg_room_1" : "wraps a grey woolen scarf around",
                "wear_msg_room_2" : "neck.",
                "type" : "scarf",
                "birth_time": time.time(),
                "duration": 2000000.0}

black_silken_scarf = {"key": "a black silken scarf",
              "typeclass": "typeclasses.clothing.Clothes",
                #"aliases" : ["scarf"],
                "desc" : "This black silken scarf looks stylish!",
                "wear_msg" : "You wrap a black silken scarf around your neck.",
                "wear_msg_room_1" : "wraps a black silken scarf around",
                "wear_msg_room_2" : "neck.",
                "type" : "scarf",
                "birth_time": time.time(),
                "duration": 2000000.0}

red_silken_scarf = {"key": "a red silken scarf",
              "typeclass": "typeclasses.clothing.Clothes",
                #"aliases" : ["scarf"],
                "desc" : "This red silken scarf looks stylish!",
                "wear_msg" : "You wrap a red silken scarf around your neck.",
                "wear_msg_room_1" : "wraps a red silken scarf around",
                "wear_msg_room_2" : "neck.",
                "type" : "scarf",
                "birth_time": time.time(),
                "duration": 2000000.0}

wooden_sandals = {"key": "sturdy wooden sandals",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["shoes"],
                "desc" : "These sturdy wooden sandals make the wearer look a bit taller",
                "wear_msg" : "You don a pair of sturdy wooden sandals.",
                "wear_msg_room_1" : "straps a pair of sturdy wooden sandals to",
                "wear_msg_room_2" : "feet.",
                "type" : "shoes",
                "birth_time": time.time(),
                "duration": 2000000.0}

laced_boots = {"key": "laced up leather boots",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["shoes"],
                "desc" : "These leather boots have a lot of laces for a firm grip.",
                "wear_msg" : "You lace up a pair of leather boots.",
                "wear_msg_room_1" : "laces up a pair of leather boots.",
                "type" : "shoes",
                "birth_time": time.time(),
                "duration": 2000000.0}

steel_toed_boots = {"key": "steel toed leather boots",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["shoes"],
                "desc" : "These steel-toed leather boots look very sturdy!",
                "wear_msg" : "You squeeze into a pair of steel-toed leather boots.",
                "wear_msg_room_1" : "squeezes a pair of steel-toed leather boots onto",
                "wear_msg_room_2" : "feet.",
                "type" : "shoes",
                "birth_time": time.time(),
                "duration": 2000000.0}

green_trousers = {"key": "woven green woolen trousers",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["pants"],
                "desc" : "These green woolen trousers look sturdy and warm.",
                "wear_msg" : "You pull on a pair of woven green woolen trousers.",
                "wear_msg_room_1" : "pulls on a pair of woven green woolen trousers.",
                "type" : "pants",
                "birth_time": time.time(),
                "duration": 2000000.0}

grey_trousers = {"key": "plain grey woolen trousers",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["pants"],
                "desc" : "These grey woolen trousers look sturdy and warm.",
                "wear_msg" : "You pull on a pair of plain grey woolen trousers.",
                "wear_msg_room_1" : "pulls on a pair of plain grey woolen trousers.",
                "type" : "pants",
                "birth_time": time.time(),
                "duration": 2000000.0}

black_silk_breeches = {"key": "black silken riding breeches",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["pants"],
                "desc" : "These black silken breeches look good but might not stand up well to time.",
                "wear_msg" : "You pull on a pair of black silken riding breeches.",
                "wear_msg_room_1" : "pulls on a pair of black silken riding breeches.",
                "type" : "pants",
                "birth_time": time.time(),
                "duration": 2000000.0}

white_leather_breeches = {"key": "white leather riding breeches",
              "typeclass": "typeclasses.clothing.Clothes",
                "aliases" : ["pants"],
                "desc" : "These white leather breeches look sturdy, if not sturdy enough to act as armor.",
                "wear_msg" : "You pull on a pair of white leather riding breeches.",
                "wear_msg_room_1" : "pulls on a pair of white leather riding breeches.",
                "type" : "pants",
                "birth_time": time.time(),
                "duration": 2000000.0}

"""
Prototypes

A prototype is a simple way to create individualized instances of a
given `Typeclass`. For example, you might have a Sword typeclass that
implements everything a Sword would need to do. The only difference
between different individual Swords would be their key, description
and some Attributes. The Prototype system allows to create a range of
such Swords with only minor variations. Prototypes can also inherit
and combine together to form entire hierarchies (such as giving all
Sabres and all Broadswords some common properties). Note that bigger
variations, such as custom commands or functionality belong in a
hierarchy of typeclasses instead.

Example prototypes are read by the `@spawn` command but is also easily
available to use from code via `evennia.spawn` or `evennia.utils.spawner`.
Each prototype should be a dictionary. Use the same name as the
variable to refer to other prototypes.

Possible keywords are:
    prototype - string pointing to parent prototype of this structure.
    key - string, the main object identifier.
    typeclass - string, if not set, will use `settings.BASE_OBJECT_TYPECLASS`.
    location - this should be a valid object or #dbref.
    home - valid object or #dbref.
    destination - only valid for exits (object or dbref).

    permissions - string or list of permission strings.
    locks - a lock-string.
    aliases - string or list of strings.

    ndb_<name> - value of a nattribute (the "ndb_" part is ignored).
    any other keywords are interpreted as Attributes and their values.

See the `@spawn` command and `evennia.utils.spawner` for more info.

"""

#from random import randint
#
#GOBLIN = {
# "key": "goblin grunt",
# "health": lambda: randint(20,30),
# "resists": ["cold", "poison"],
# "attacks": ["fists"],
# "weaknesses": ["fire", "light"]
# }
#
#GOBLIN_WIZARD = {
# "prototype": "GOBLIN",
# "key": "goblin wizard",
# "spells": ["fire ball", "lighting bolt"]
# }
#
#GOBLIN_ARCHER = {
# "prototype": "GOBLIN",
# "key": "goblin archer",
# "attacks": ["short bow"]
#}
#
# This is an example of a prototype without a prototype
# (nor key) of its own, so it should normally only be
# used as a mix-in, as in the example of the goblin
# archwizard below.
#ARCHWIZARD_MIXIN = {
# "attacks": ["archwizard staff"],
# "spells": ["greater fire ball", "greater lighting"]
#}
#
#GOBLIN_ARCHWIZARD = {
# "key": "goblin archwizard",
# "prototype" : ("GOBLIN_WIZARD", "ARCHWIZARD_MIXIN")
#}