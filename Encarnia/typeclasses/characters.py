"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from evennia import TICKER_HANDLER as tickerhandler
import re
from world import rules, english_utils
from random import randint
from evennia.contrib import custom_gametime

class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(player) -  when Player disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Player has disconnected" 
                    to the room.
    at_pre_puppet - Just before Player re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "PlayerName has entered the game" to the room.

    """
    def at_object_creation(self):
        """
        Called only at initial creation. This is a rather silly
        example since ability scores should vary from Character to
        Character and is usually set during some character 
        generation step instead.
        """

        # under = Anything that would be worn under outer clothing.
        # outer = Normal clothing like shirt pants ect...
        # over = Any clothing type that could be worn over armour... cape, cloak
        self.db.wearing = []
        self.db.shown_clothes = []
        self.db.clothes_objects = []
        self.db.wielding = []
        self.db.girdle = []
        self.db.handed = "right"
        self.db.canteen_type = ""
        self.db.canteen_max_sips = 4
        self.db.canteen_current_sips = 4

        # Affiliation stuff
        self.db.citizenship = "none"
        self.db.guild = "none"
        self.db.prefix = False
        self.db.suffix = False
                           
        # Stats and skills
        self.db.base_strength = 10
        self.db.strength = 10
        self.db.current_strength = 10

        self.db.base_agility = 10
        self.db.agility = 10
        self.db.armored_agility = 10
        self.db.current_agility = 10

        self.db.base_constitution = 10
        self.db.constitution = 10
        self.db.current_constitution = 10

        self.db.endurance = 10

        self.db.base_magic = 10
        self.db.magic = 10
        self.db.current_magic = 0

        self.db.enchantments = []

        self.db.base_health = 110
        self.db.health = 110
        self.db.max_health = 110

        # Monies
        self.db.silver_carried = 0
        self.db.tower_bank_account = 0

        # Election stuff
        self.db.last_election_voted = 0
        self.db.last_election_voted_2 = 0
        self.db.last_election_voted_3 = 0
        self.db.last_election_voted_4 = 0
        self.db.last_election_voted_5 = 0

        # Lessons
        self.db.sub_lessons = 0
        self.db.lessons = 0
        self.db.lessons_spent = 0

        # Did you just assume my gender?
        self.db.gender = "male"
        self.db.genders = "he"
        self.db.gendero = "him"
        self.db.genderp = "his"
        self.db.genderl = "himself"

        #Race related properties.
        self.db.race = "slime"
        self.db.move_delay_default = 0.2
        self.db.last_move = "out"

        #Class or skill access stuff
        self.db.char_class = "none"
        self.db.physique = "athletic"

        #Acquired or special traits stuff
        self.db.scars = []

        #Combat stuff
        self.db.stamina = 10
        self.db.max_stamina = 10

        self.db.prepped = []
        self.db.stance = "no stance"

        self.db.move_message = "walking"

        self.db.wounds = []

        self.db.dizzy = False
        self.db.chilled = 0

        self.db.bleeding = 0

        self.db.regen_rate = 0.1

        self.db.loaded_aff = None

        self.db.shielded = None

        self.db.aura = None

        self.db.auto_walking = False
        self.db.auto_walk_target = "none"

        #Balance timers
        self.db.balance_time = 0.0
        self.db.balance_time_magic = 0.0
        self.db.balance_time_dizzy= 0.0
        self.db.balance_time_cold = 0.0
        self.db.balance_time_webbed = 0.0
        self.db.balance_time_weakness = 0.0
        self.db.balance_time_clumsiness = 0.0
        self.db.balance_time_paralysis = 0.0
        self.db.web_curse = 0.0
        self.db.heal_delay = 0.0
        self.db.shield_delay = 0.0

        # Quests
        self.db.perma_quests_completed = []
        self.db.timed_quests_completed = {}

        # PvP Tracking Stuff
        self.db.duel_target = "none"
        self.db.duel_timer = 0.0

        self.db.feuds = []

        self.db.player_kills = 0
        self.db.player_PvP_deaths = 0
        self.db.consecutive_player_kills = 0

        self.db.open_pvp = False
        self.db.open_pvp_timer = 0.0 # Useful for so many things!

        # Special play mode trackers
        self.db.nightmare_points = 0
        self.db.hunger = 0
        self.db.dead = False # not undead!

        # Level and EXP values
        self.db.level = 1
        self.db.exp = 0
        self.db.exp_multiplier = 30

        # Equipment-related attributes
        self.db.armor_bonus = 0
        self.db.armor_type = "leather"
        self.db.base_girdle_size = 2
        self.db.girdle_size = 2


        # Ticker handler for timed effects; regeneration, bleeding, etc.
        tickerhandler.add(7, self.player_character_ticks)
        self.db.death_ticker = 0

        # More Misc stuff
        self.db.birth_year, self.db.birth_month, self.db.birth_day, self.db.birth_hour, self.db.birth_min, self.db.birth_sec = custom_gametime.custom_gametime(absolute=True)
        self.db.following = "nobody"
        self.db.gods_follow = False

    def show_prompt(self):
        """
        This hook is called after the command has finished executing
        (after self.func()).
        """

        if (float(self.db.health) / float(self.db.max_health)) > 0.80:
            prompt_hp_color = "|g"
        elif (float(self.db.health) / float(self.db.max_health)) > 0.36:
            prompt_hp_color = "|y"
        else:
            prompt_hp_color = "|r"

        if self.db.stamina > 6:
            prompt_stamina_color = "|g"
        elif self.db.stamina > 3:
            prompt_stamina_color = "|y"
        else:
            prompt_stamina_color = "|r"

        magic_level = "Asleep"
        if self.db.current_magic == 0:
            magic_level = "Asleep"
        elif self.db.current_magic > 7:
            magic_level = "|rRaging|n"
        elif self.db.current_magic > 4:
            magic_level = "|yIrate|n"
        elif self.db.current_magic > 0:
            magic_level = "|gAwoken|n"

        prompt = "%sHealth|n: %s%s|n - |gMagic|n: %s|n - %sStamina|n: %s%s." % (prompt_hp_color, prompt_hp_color, self.db.health, magic_level, prompt_stamina_color, prompt_stamina_color, self.db.stamina)
        self.msg(prompt)

    def player_character_ticks(self, *args, **kwargs):
        "ticked at regular intervals"
        # Stamina regeneration
        if self.db.stamina < 10:
            self.db.stamina = self.db.stamina + 1

        if self.db.current_magic > 0:
            self.db.current_magic -= 1

        # Health regeneration
        if self.db.health < self.db.max_health:
            heal_amount = int(self.db.max_health * self.db.regen_rate)
            self.db.health = self.db.health + heal_amount

            if self.db.health > self.db.max_health:
                self.db.health = self.db.max_health

        # Guarding endurance loss
        if self.db.stance == "defensive":
            d20 = randint(1, 20)

            if d20 > self.db.endurance:
                self.msg("Your stamina drains as you maintain your guard.")
                if self.db.stamina > 1:
                    self.db.stamina = self.db.stamina - 2
                else:
                    self.db.stamina = 0
                    self.db.stance = "no stance"
                    self.msg("You can maintain your guard no longer!")
                self.show_prompt()

    def return_appearance(self, looker):
        """
        This is what they look like when looked at.
        """

        if self.db.wielding:
            appearance = self.db.desc + "\n|w%s is wielding %s.|n\n" % (str.capitalize(self.db.genders), self.db.wielding[0])
        else:
            appearance = self.db.desc + "\n"

        if self.db.shown_clothes:
            appearance = appearance + "|c%s|n is %s %s %s.  %s is wearing %s." % (self.name, english_utils.iart(self.db.gender), self.db.physique, str.capitalize(self.db.race), str.capitalize(self.db.genders), english_utils.iart_list(self.db.shown_clothes))
        else:
            appearance = appearance + "|c%s|n is %s %s %s.  %s is completely naked!" % (
            self.name, english_utils.iart(self.db.physique), self.db.race, self.db.gender,
            str.capitalize(self.db.genders))

        return appearance

    def at_post_puppet(self):
        """
        Called just after puppeting has been completed and all
        Player<->Object links have been established.

        Note:
            You can use `self.player` and `self.sessions.get()` to get
            player and sessions at this point; the last entry in the
            list from `self.sessions.get()` is the latest Session
            puppeting this Object.

        """
        self.msg("\nYou become |c%s|n.\n" % self.name)
        self.msg(self.at_look(self.location))

        def message(obj, from_obj):
            obj.msg("The form of %s emerges from the ether as %s soul descends to use it." % (self.get_display_name(obj), self.db.genderp), from_obj=from_obj)
        self.location.for_contents(message, exclude=[self], from_obj=self)

        self.db.enchantments = []
        self.db.regen_rate = 0.1

        tickerhandler.add(7, self.player_character_ticks)

    def at_post_unpuppet(self, player, session=None):
        """
        We stove away the character when the player goes ooc/logs off,
        otherwise the character object will remain in the room also
        after the player logged off ("headless", so to say).

        Args:
            player (Player): The player object that just disconnected
                from this object.
            session (Session): Session controlling the connection that
                just disconnected.
        """
        if not self.sessions.count():
            tickerhandler.remove(7, self.player_character_ticks)

            # only remove this char from grid if no sessions control it anymore.
            if self.location:
                def message(obj, from_obj):
                    obj.msg("The form of %s shimmers briefly, then fades away into the ether." % self.get_display_name(obj), from_obj=from_obj)
                self.location.for_contents(message, exclude=[self], from_obj=self)
                self.db.prelogout_location = self.location
                self.location = None