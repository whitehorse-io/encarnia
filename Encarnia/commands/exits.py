"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia import DefaultExit, utils, Command
from random import randint
import time

class Exit(DefaultExit):
    """
    Exits are connectors between rooms. Exits are normal Objects except
    they defines the `destination` property. It also does work in the
    following methods:

     basetype_setup() - sets default exit locks (to change, use `at_object_creation` instead).
     at_cmdset_get(**kwargs) - this is called when the cmdset is accessed and should
                              rebuild the Exit cmdset along with a command matching the name
                              of the Exit object. Conventionally, a kwarg `force_init`
                              should force a rebuild of the cmdset, this is triggered
                              by the `@alias` command when aliases are changed.
     at_failed_traverse() - gives a default error message ("You cannot
                            go there") if exit traversal fails and an
                            attribute `err_traverse` is not defined.

    Relevant hooks to overload (compared to other types of Objects):
        at_traverse(traveller, target_loc) - called to do the actual traversal and calling of the other hooks.
                                            If overloading this, consider using super() to use the default
                                            movement implementation (and hook-calling).
        at_after_traverse(traveller, source_loc) - called by at_traverse just after traversing.
        at_failed_traverse(traveller) - called by at_traverse if traversal failed for some reason. Will
                                        not be called if the attribute `err_traverse` is
                                        defined, in which case that will simply be echoed.
    """

    def at_after_traverse(self, traversing_object, source_location):
        """
        Called just after an object successfully used this object to
        traverse to another object (i.e. this object is a type of
        Exit)

        Args:
            traversing_object (Object): The object traversing us.
            source_location (Object): Where `traversing_object` came from.

        Notes:
            The target location should normally be available as `self.destination`.

        Ashlan note: This has to be defined before the rest of the code, probably it's similar for other exit hooks.
        """

        if traversing_object.db.dead:
            destination = traversing_object.search("#740", global_search=True)
            traversing_object.move_to(destination, quiet=True)

        if traversing_object.db.followed_by:
            destination = traversing_object.location
            for i in traversing_object.db.followed_by:
                if i.db.following == traversing_object:
                    i.move_to(destination)
                    i.msg("You followed %s %s." % (traversing_object.name, traversing_object.db.last_move))
                else:
                    traversing_object.db.followed_by.remove[i]

        if traversing_object.db.stamina:
            if (float(traversing_object.db.health) / float(traversing_object.db.max_health)) > 0.80:
                prompt_hp_color = "|g"
            elif (float(traversing_object.db.health) / float(traversing_object.db.max_health)) > 0.36:
                prompt_hp_color = "|y"
            else:
                prompt_hp_color = "|r"

            if traversing_object.db.stamina > 6:
                prompt_stamina_color = "|g"
            elif traversing_object.db.stamina > 3:
                prompt_stamina_color = "|y"
            else:
                prompt_stamina_color = "|r"

            prompt = "%sHealth|n: %s%s|n - |gMagic|n: |nAsleep|n - %sStamina|n: %s%s." % (prompt_hp_color, prompt_hp_color, traversing_object.db.health, prompt_stamina_color, prompt_stamina_color, traversing_object.db.stamina)
            traversing_object.msg(prompt)

    def at_traverse(self, traversing_object, target_location):
        """
        Implements the actual traversal, using utils.delay to delay the move_to.
        """

        # if the traverser has an Attribute move_speed, use that,
        # otherwise default to "walk" speed

        # WHN: Turning this from move_speed to moves.  His system was coded pretty well though! I could partially copy it for the cold system, for example, each 10% of cold could be rounded to double it's value x .1, so 100% cold would be a 2 second move delay.

        # MOVE_DELAY = {"stroll": 6,
        #       "walk": 4,
        #       "run": 2,
        #       "sprint": 1}

        # WHN: Slow movement is handled down here.
        #move_speed = traversing_object.db.moves  # or "walk"
        # move_delay = MOVE_DELAY.get(moves, 4)
        move_delay = 0.2

        if traversing_object.db.stamina == 0:
            traversing_object.msg("You are too tired to move any further!")
            return
        elif traversing_object.db.stamina:
            traversing_object.db.last_move = self.key # This should be the name of the exit.
            if traversing_object.db.moving:
                traversing_object.msg("You are already moving.")
                return

            move_delay = traversing_object.db.move_delay_default
            if time.time() < traversing_object.db.balance_time:
                move_delay = move_delay + 1.3

            if traversing_object.db.stamina < 10:
                move_delay_increase = 10.0 - traversing_object.db.stamina
                move_delay_increase = move_delay_increase / 10.0
                move_delay = move_delay + move_delay_increase

            if not traversing_object.location.tags.get("city", category = 'corinth'):
                d19 = randint(1,18)
                if d19 > traversing_object.db.endurance:
                    traversing_object.db.stamina = traversing_object.db.stamina - 1

                if not traversing_object.location.tags.get("trail_ends"):
                    if not traversing_object.location.db.trails:
                        traversing_object.location.db.trails = {}
                    traversing_object.location.db.trails[str(traversing_object.name)] = str(traversing_object.db.last_move)

            traversing_object.db.moving = True
            traversing_object.db.stance = "no stance"

            if traversing_object.db.stamina:
                traversing_object.db.move_message = "walking"

            if time.time() < traversing_object.db.balance_time:
                traversing_object.db.move_message = "maneuvering"

            if traversing_object.db.stamina < 4:
                traversing_object.db.move_message = "staggering"

        def move_callback():
            "This callback will be called by utils.delay after move_delay seconds."

            traversing_object.db.moving = False

            source_location = traversing_object.location
            if traversing_object.move_to(target_location):
                self.at_after_traverse(traversing_object, source_location)
            else:
                if self.db.err_traverse:
                    # if exit has a better error message, let's use it.
                    self.caller.msg(self.db.err_traverse)
                else:
                    # No shorthand error message. Call hook.
                    self.at_failed_traverse(traversing_object)

            if self.db.test_attr == "blocked":
                #TODO: change this attribute to "blocked_by" later, and look into a hook that triggers on attempt to exit for rooms later on.
                # Also look into at_failed_traverse here.
                traversing_object.msg("That exit was blocked!")

        traversing_object.location.msg_contents("%s is %s %sward." % (traversing_object.name, traversing_object.db.move_message, self.key), exclude=[traversing_object])
        traversing_object.msg("You begin %s %sward." % (traversing_object.db.move_message, self.key))
        # traversing_object.msg(traversing_object.db.hp) -- this works, so I can reference plenty of attributes from here.

        # create a delayed movement
        deferred = utils.delay(move_delay, callback=move_callback)

        # we store the deferred on the character, this will allow us
        # to abort the movement. We must use an ndb here since
        # deferreds cannot be pickled.
        traversing_object.ndb.currently_moving = deferred