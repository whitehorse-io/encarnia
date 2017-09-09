from evennia import Command as BaseCommand

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
        - at_pre_command(): If this returns True, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_command(): Extra actions, often things done after
            every command, like prompts.

    """

    def show_prompt(self, target):
        """
        This hook is called after the command has finished executing
        (after self.func()).
        """

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

        # Not needed from the command's perspective.
        #if target.db.health != None:
        #    target.msg(prompt)

    pass

########################################################################
#WHN: Emotes start here.
########################################################################

class CmdAnger(Command):
    """
    An anger emote.

    Usage: 
      anger

    """ 

    key = "anger"
    aliases = ["mad"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s looks mad. Really mad. You mad?" % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You are looking really mad right now!")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s looks really angry right now!" % caller.name
            target.msg(string)
            string = "You catch yourself looking angrily at %s." % target.name
            caller.msg(string)
            string = "%s looks upset and angry with %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdSmirk(Command):
    """
    A smirk emote.

    Usage: 
      smirk

    """ 

    key = "smirk"
    aliases = ["wry"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s smirks wryly." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You smirk wryly.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s smirks wryly at you." % caller.name
            target.msg(string)
            string = "You smirk wryly at %s." % target.name
            caller.msg(string)
            string = "%s smirks wryly at %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdNod(Command):
    """
    A nod emote.

    Usage: 
      nod

    """ 

    key = "nod"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s nods %s head." % (caller.name, caller.db.genderp)
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You nod your head.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s gives you a nod of %s head." % (caller.name, caller.db.genderp)
            target.msg(string)
            string = "You nod your head towards %s." % target.name
            caller.msg(string)
            string = "%s gives a nod of %s head to %s." % (caller.name, caller.db.genderp, target.name)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdShake(Command):
    """
    A shake emote.

    Usage: 
      shake

    """ 

    key = "shake"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s shakes %s head." % (caller.name, caller.db.genderp)
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You shake your head.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s shakes %s head at you." % (caller.name, caller.db.genderp)
            target.msg(string)
            string = "You shake your head at %s." % target.name
            caller.msg(string)
            string = "%s shakes %s head at %s." % (caller.name, caller.db.genderp, target.name)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdSalute(Command):
    """
    A salute emote.

    Usage: 
      salute

    """ 

    key = "salute"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip()

    def func(self):
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s stands at attention and gives a crisp salute." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You stand at attention and give a crisp salute.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s stands at attention and gives you a crisp salute." % caller.name
            target.msg(string)
            string = "You stand at attention and give %s a crisp salute." % target.name
            caller.msg(string)
            string = "%s stands at attention and gives %s a crisp salute." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdWink(Command):
    """
    A wink emote.

    Usage: 
      wink

    """ 

    key = "wink"
    aliases = ["winky"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s winks charmingly." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You wink a charming wink of winklyness.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s winks charmingly at you." % caller.name
            target.msg(string)
            string = "You wink charmingy at %s." % target.name
            caller.msg(string)
            string = "%s winks charmingly at %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdDance(Command):
    """
    A dance emote.

    Usage: 
      dance

    """ 

    key = "dance"
    aliases = ["tango"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s dances the tango. Apparently it doesn't take two after all." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You dance the tango -- alone. Skills!")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s dances dramatically with you." % caller.name
            target.msg(string)
            string = "You dance the dance of love and suffering with %s." % target.name
            caller.msg(string)
            string = "%s dances the dance of love and suffering with %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdPat(Command):
    """
    A pat emote.

    Usage: 
      pat

    """ 

    key = "pat"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s pats themselves on the back." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You pat yourself on the back. Good job!")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s pats you on the back." % caller.name
            target.msg(string)
            string = "You pat %s on the back." % target.name
            caller.msg(string)
            string = "%s pats %s on the back." % (caller.name, target.name)

            caller.location.msg_contents(string, exclude=[caller,target])

class CmdWince(Command):
    """
    A wince emote.

    Usage: 
      wince

    """ 

    key = "wince"
    #aliases = ["wince at"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s winces awkwardly." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You wince awkwardly.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s winces awkwardly at you." % caller.name
            target.msg(string)
            string = "You wince awkwardly at %s." % target.name
            caller.msg(string)
            string = "%s winces awkwardly at %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdApologize(Command):
    """
    An apologize emote.

    Usage: 
      apologize

    """ 

    key = "apologize"
    #aliases = ["apologize to"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s formally apologizes." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You formally apologize.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s formally apologizes to you." % caller.name
            target.msg(string)
            string = "You formally apologize to %s." % target.name
            caller.msg(string)
            string = "%s formally apologizes to %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdThank(Command):
    """
    A thank emote.

    Usage: 
      thank

    """ 

    key = "thank"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s humbly thanks everyone." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You humbly thank everyone.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s humbly thanks you." % caller.name
            target.msg(string)
            string = "You humbly thank %s." % target.name
            caller.msg(string)
            string = "%s humbly thanks %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdLaugh(Command):
    """
    A laugh emote.

    Usage: 
      laugh

    """ 

    key = "laugh"
    aliases = ["lol"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s laughs out loud!" % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You laugh out loud!")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s laughs out loud at you!" % caller.name
            target.msg(string)
            string = "You laugh out loud at %s." % target.name
            caller.msg(string)
            string = "%s laughs out loud at %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdWave(Command):
    """
    A wave emote.

    Usage: 
      wave

    """ 

    key = "wave"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s waves." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You wave.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s waves at you." % caller.name
            target.msg(string)
            string = "You wave at %s." % target.name
            caller.msg(string)
            string = "%s waves at %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdCurtsey(Command):
    """
    A curtsey emote.

    Usage: 
      curtsey

    """ 

    key = "curtsey"
    aliases = ["curtsy"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s curtseys gracefully." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You curtsey gracefully.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s curtseys gracefully before for you." % caller.name
            target.msg(string)
            string = "You curtsey gracefully before %s." % target.name
            caller.msg(string)
            string = "%s curtseys gracefully before %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdHug(Command):
    """
    A hug emote.

    Usage: 
      hug

    """ 

    key = "hug"
    aliases = ["embrace"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s awaits a hug with open arms." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You await your hug with open arms.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s gives you a hug!" % caller.name
            target.msg(string)
            string = "You give %s a hug!" % target.name
            caller.msg(string)
            string = "%s hugs %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdKiss(Command):
    """
    A kiss emote.

    Usage: 
      kiss

    """ 

    key = "kiss"
    aliases = ["smooch", "snog"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s purses those lips for a smooch." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You purse those kissers for a smooch.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s gives you a smooch!" % caller.name
            target.msg(string)
            string = "You give %s a smooch!" % target.name
            caller.msg(string)
            string = "%s gives %s a smooch!" % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdFrown(Command):
    """
    A frown emote.

    Usage: 
      frown

    """ 

    key = "frown"
    #aliases = ["frown at"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s frowns darkly." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You frown darkly.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s frowns darkly at you." % caller.name
            target.msg(string)
            string = "You frown darkly at %s." % target.name
            caller.msg(string)
            string = "%s frowns darkly at %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdMutter(Command):
    """
    A mutter emote.

    Usage: 
      mutter

    """ 

    key = "mutter"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s mutters angrily, unmindful of who hears." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You mutter angrily, not mindful of who might hear you.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s mutters angrily in your general direction." % caller.name
            target.msg(string)
            string = "You mutter angrily in the general direction of %s." % target.name
            caller.msg(string)
            string = "%s mutters angrily in the general direction of %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdGreet(Command):
    """
    Raise a hand in greeting towards someone.

    Usage:
      greet

    """

    key = "greet"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s raises a hand in greeting." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You raise a hand in greeting.")
        else:
            target = caller.search(self.target)
            if not target:
                # caller.search handles error messages
                return
            string = "%s raises a hand towards you in greeting." % caller.name
            target.msg(string)
            string = "You raise a hand towards %s in greeting." % target.name
            caller.msg(string)
            string = "%s raises a hand towards %s in greeting." % (caller.name, target.name)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdPet(Command):
    """
    Gently pet something (or someone).

    Usage:
      pet <something or someone>

    """

    key = "pet"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s makes a petting motion with %s hand." % (caller.name, caller.db.genderp)
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You make a petting motion with your hand.")
        else:
            target = caller.search(self.target)
            if not target:
                # caller.search handles error messages
                return
            string = "%s gently pets you." % caller.name
            target.msg(string)
            string = "You gently pet %s." % target.name
            caller.msg(string)
            string = "%s gently pets %s." % (caller.name, target.name)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdScream(Command):
    """
    A scream emote.

    Usage: 
      scream

    """ 

    key = "scream"
    #aliases = ["scream at"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s screams loudly! Aaaaaaah! Not awkward." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You scream at the top of your lungs!")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s loudly at you! So weird!" % caller.name
            target.msg(string)
            string = "You scream loudly at %s, not being weird or anything." % target.name
            caller.msg(string)
            string = "%s screams loudly at %s. These two have issues." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdWhine(Command):
    """
    A whine emote.

    Usage: 
      whine [<target>]

    """ 

    key = "whine"
    #aliases = ["whine to", "whine at"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s whines annoyingly." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You whine, trying not to be too annoying.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s whines at you annoyingly." % caller.name
            target.msg(string)
            string = "You whine at %s, trying not to be too annoying." % target.name
            caller.msg(string)
            string = "%s whiens annoyingly towards %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdPoke(Command):
    """
    A poke emote.

    Usage: 
      poke

    """ 

    key = "poke"
    aliases = ["prod"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s lifts a finger, threatening to poke." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You lift your poking finger, ready to poke. You'll do it!")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s pokes you in the ribs." % caller.name
            target.msg(string)
            string = "You poke %s in the ribs, probably not for the first time." % target.name
            caller.msg(string)
            string = "%s pokes %s in the ribs." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdTear(Command):
    """
    A tear emote.

    Usage: 
      tear

    """ 

    key = "tear"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "A single tear slips down the face of %s." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("A single tear slips down your face.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s looks at you and a single tear slips down that face." % caller.name
            target.msg(string)
            string = "You look at %s as a single tear slips down your face." % target.name
            caller.msg(string)
            string = "A single tear slips down the face %s, who is looking at %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdCry(Command):
    """
    A cry emote.

    Usage: 
      cry

    """ 

    key = "cry"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s cries hysterically." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You cry hysterically.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s cries hysterically in front of you." % caller.name
            target.msg(string)
            string = "You cry hysterically in front of %s." % target.name
            caller.msg(string)
            string = "%s cries hysterically in front of %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdPoint(Command):
    """
    A point emote.

    Usage: 
      point <person, direction, up, down>

    """ 

    key = "point"
    aliases = ["point"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s points off into the distance." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You point off into the distance.")
        else:
            if self.target == "north":
                string = "%s points to the north." % caller.name
                caller.location.msg_contents(string, exclude=[caller])
                caller.msg("You point to the north.")
            elif self.target == "east":
                string = "%s points to the east." % caller.name
                caller.location.msg_contents(string, exclude=[caller])
                caller.msg("You point to the east.")
            elif self.target == "south":
                string = "%s points to the south." % caller.name
                caller.location.msg_contents(string, exclude=[caller])
                caller.msg("You point to the south.")
            elif self.target == "west":
                string = "%s points to the west." % caller.name
                caller.location.msg_contents(string, exclude=[caller])
                caller.msg("You point to the west.")
            elif self.target == "up":
                string = "%s points straight up." % caller.name
                caller.location.msg_contents(string, exclude=[caller])
                caller.msg("You point straight up.")
            elif self.target == "down":
                string = "%s points down towards the ground." % caller.name
                caller.location.msg_contents(string, exclude=[caller])
                caller.msg("You point down towards the ground.")
            else:
                target = caller.search(self.target)
                if not target:
                    # caller.search handles error messages
                    return
                string = "%s points directly at you." % caller.name
                target.msg(string)
                string = "You point directly at %s." % target.name
                caller.msg(string)
                string = "%s points directly at %s." % (caller.name, target.name)           
                caller.location.msg_contents(string, exclude=[caller,target])

class CmdFacepalm(Command):
    """
    Face, meet palm.

    Usage: 
      facepalm

    """ 

    key = "facepalm"
    aliases = ["f2p"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s facepalms. Why? I mean, at least it's not a double facepalm." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You facepalm because why?")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s facepalms before you but it coud be worse, right?" % caller.name
            target.msg(string)
            string = "You facepalm right in front of %s because why?" % target.name
            caller.msg(string)
            string = "%s looks at %s and then facepalms." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdPray(Command):
    """
    A pray emote.

    Usage: 
      pray

    """ 

    key = "pray"
    aliases = ["hope"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s prays humbly to the Gods and their Encarnations." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You pray humbly before the Gods and their Encarnations.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s prays for you, to the Gods and their Enarnations." % caller.name
            target.msg(string)
            string = "You pray to the Gods and their Encarnations for mercy for %s." % target.name
            caller.msg(string)
            string = "%s prays humbly to the Gods and their Encarnations to show mercy upon %s." % (caller.name, target.name)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdSmile(Command):
    """
    A smile emote.

    Usage: 
      smile [<someone>]

    Smiles to someone in your vicinity or to the room
    in general.

    """ 

    key = "smile"
    #aliases = ["smile at"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s smiles." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You smile.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s smiles at you." % caller.name
            target.msg(string)
            string = "You smile at %s." % target.name
            caller.msg(string)
            string = "%s smiles at %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdGrin(Command):
    """
    A grin emote.

    Usage: 
      grin [<someone>]

    Grin to someone in your vicinity or to the room
    in general.

    """ 

    key = "grin"
    #aliases = ["grin at"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s grins mischievously." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You grin mischievously.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s grins mischievously at you." % caller.name
            target.msg(string)
            string = "You grin mischievously at %s." % target.name
            caller.msg(string)
            string = "%s grins mischievously at %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdBow(Command):
    """
    A bow emote.

    Usage: 
      bow [<someone>]

    """ 

    key = "bow"
    #aliases = ["bow"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s bows deeply." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You bow deeply.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s bows deeply before you." % caller.name
            target.msg(string)
            string = "You bow deeply before %s." % target.name
            caller.msg(string)
            string = "%s bows deeply before %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdKneel(Command):
    """
    A kneel emote.

    Usage:
      kneel [<someone>]

    """ 

    key = "kneel"
    #aliases = ["kneel before"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s kneels humbly on the ground." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You kneel humbly on the ground.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s kneels humbly on the ground before you." % caller.name
            target.msg(string)
            string = "You kneel humbly on the ground before %s." % target.name
            caller.msg(string)
            string = "%s kneels humbly on the ground before %s." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdBeg(Command):
    """
    A beg emote.

    Usage: 
      beg [<someone>]

    """ 

    key = "beg"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser" 
        self.target = self.args.strip() 

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s begs pitifully to anyone who will listen." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You beg pitifully to anyone who will listen.")
        else:
            target = caller.search(self.target)
            if not target: 
                # caller.search handles error messages
                return
            string = "%s begs you pitifully for mercy." % caller.name
            target.msg(string)
            string = "You beg %s pitifully for mercy." % target.name
            caller.msg(string)
            string = "%s begs %s pitifully for mercy." % (caller.name, target.name)           
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdParagon(Command):
    """
    Looking good!

    Usage:
      paragon

    """

    key = "paragon"
    aliases = ["cool"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s stands tall before you, a virtual paragon!" % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You are looking pretty cool right now!")
        else:
            target = caller.search(self.target)
            if not target:
                # caller.search handles error messages
                return
            string = "%s stands tall before you, a virtual paragon!" % caller.name
            target.msg(string)
            string = "You try to look cool in front of %s." % target.name
            caller.msg(string)
            string = "%s stands tall before %s, trying to look cool." % (caller.name, target.name)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdSmooth(Command):
    """
    Smooth back that hair!

    Usage:
      smooth

    """

    key = "smooth"
    aliases = ["slick"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s slicks back %s hair." % (caller.name, caller.db.genderp)
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You slick back that hair!")
        else:
            target = caller.search(self.target)
            if not target:
                # caller.search handles error messages
                return
            string = "%s looks at you while smoothing back %s hair." % (caller.name, caller.db.genderp)
            target.msg(string)
            string = "You look at %s and smooth back your hair." % target.name
            caller.msg(string)
            string = "Eyes on %s, %s smooths back %s hair." % (target.name, caller.name, caller.db.genderp)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdFistBump(Command):
    """
    Bro (or sister) fister!

    Usage:
      fistbump

    """

    key = "fistbump"
    aliases = ["brofist", "sisfist"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s fist bumps with... no one. Sad!" % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You fist bump with your imaginary bro.  Not awkward.")
        else:
            target = caller.search(self.target)
            if not target:
                # caller.search handles error messages
                return
            string = "Against your better judgment, you fist bump with %s." % caller.name
            target.msg(string)
            string = "You and %s bump fists." % target.name
            caller.msg(string)
            string = "%s and %s bump fists.  Can you feel the bromance?" % (caller.name, target.name)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdHi(Command):
    """
    Raise your hand in a greeting to someone.

    Usage:
      hi <someone>

    """

    key = "hi"
    aliases = ["hello", "nihao"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "\"Hi!\" %s blurts out." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("\"Hi!\" you blurt out.")
        else:
            target = caller.search(self.target)
            if not target:
                # caller.search handles error messages
                return
            string = "\"Hi!\" %s says to you." % caller.name
            target.msg(string)
            string = "\"Hi!\" you say to %s." % target.name
            caller.msg(string)
            string = "\"Hi!\" %s says to %s." % (caller.name, target.name)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdHeh(Command):
    """
    Almost a laugh but not quite...

    Usage:
      heh

    """

    key = "heh"
    aliases = ["hah"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller

        string = "\"Heh,\" %s grunts." % caller.name
        caller.location.msg_contents(string, exclude=caller)
        caller.msg("\"Heh,\" you grunt.")

class CmdOK(Command):
    """
    Express your consent, approval or just maybe, indifference.

    Usage:
      ok <target>

    """

    key = "ok"
    aliases = ["ok!", "kk"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "\"Ok!\" %s blurts out." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("\"Ok!\" you blurt out.")
        else:
            target = caller.search(self.target)
            if not target:
                # caller.search handles error messages
                return
            string = "\"Ok!\" %s says to you." % caller.name
            target.msg(string)
            string = "You look at %s and say, \"Ok!\"" % target.name
            caller.msg(string)
            string = "\"Ok!\", %s says to %s." % (caller.name, target.name)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdYo(Command):
    """
    A "Yo!" emote.

    Usage:
      yo

    """

    key = "yo"
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "\"Yo!\" %s says." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("\"Yo!\" you say.")
        else:
            target = caller.search(self.target)
            if not target:
                # caller.search handles error messages
                return
            string = "\"Yo!\" %s says to you." % caller.name
            target.msg(string)
            string = "\"Yo!\" you say to %s." % target.name
            caller.msg(string)
            string = "\"Yo!\" %s says to %s." % (caller.name, target.name)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdPonder(Command):
    """
    A ponder emote.

    Usage:
      ponder

    """

    key = "ponder"
    aliases = ["think"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s ponders... things." % caller.name
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You ponder... things.")
        else:
            target = caller.search(self.target)
            if not target:
                # caller.search handles error messages
                return
            string = "%s looks at you and rubs %s chin thoughtfully." % (caller.name, caller.db.genderp)
            target.msg(string)
            string = "You look at %s and rub your chin thoughtfully." % target.name
            caller.msg(string)
            string = "%s looks at %s and rubs %s chin thoughtfully." % (caller.name, target.name, caller.db.genderp)
            caller.location.msg_contents(string, exclude=[caller,target])

class CmdShrug(Command):
    """
    A shrug emote.

    Usage:
      shrug <target>

    """

    key = "shrug"
    #aliases = ["mad"]
    locks = "cmd:all()"
    help_category = "Emotes"

    def parse(self):
        "Very trivial parser"
        self.target = self.args.strip()

    def func(self):
        "This actually does things"
        caller = self.caller
        if not self.target or self.target == "here":
            string = "%s shrugs %s shoulders." % (caller.name, caller.db.genderp)
            caller.location.msg_contents(string, exclude=caller)
            caller.msg("You shrug your shoulders.")
        else:
            target = caller.search(self.target)
            if not target:
                # caller.search handles error messages
                return
            string = "%s looks at you and shrugs." % caller.name
            target.msg(string)
            string = "You look at %s and shrug." % target.name
            caller.msg(string)
            string = "%s looks at %s and shrugs." % (caller.name, target.name)
            caller.location.msg_contents(string, exclude=[caller,target])