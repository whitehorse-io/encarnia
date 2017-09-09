"""
Evennia settings file.

The available options are found in the default settings file found
here:

/home/ubuntu/muddev/evennia/evennia/settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Encarnia"

# TCN: Trying to open ports to the outside now.
# Internal use ports are 5000, 5001.
# Probrem: Amazon Lightsail only has ports 22 and 80 open by default
TELNET_PORTS = [4000]
WEBSOCKET_CLIENT_PORT = 4001
WEBSERVER_PORTS = [(4002, 5000)]
AMP_PORT = 5001

# Register with the Evennia game index (see games.evennia.com)
GAME_DIRECTORY_LISTING = {
	'game_status': 'pre-alpha',
	'game_website': 'http://54.200.123.230:4002/',
	'listing_contact': '/u/spark-001',
	'telnet_hostname': '54.200.123.230',
	'telnet_port': 4000,
	'short_description': "Encarnia custom PvP MUD!",
	'long_description': 'Encarnia is a PvP MUD with custom game mechanics inspired by Gemstone IV and Achaea.'
}

# Trying to change to account mode.
MULTISESSION_MODE = 2
MAX_NR_CHARACTERS = 6

# Setting up new channels to get rid of the public channel.
# DEFAULT_CHANNELS = [
#                   # public channel
#                   {"key": "OOC",
#                   "aliases": ('ooc', 'pub'),
#                   "desc": "Public OOC Discussion.",
#                   "locks": "control:perm(Wizards);listen:all();send:all()"},
#                   # connection/mud info
#                   {"key": "MudInfo",
#                    "aliases": "",
#                    "desc": "Connection log.",
#                    "locks": "control:perm(Immortals);listen:perm(Wizards);send:false()"},
#                   {"key": "Newbie",
#                    "aliases": "",
#                   "desc": "Public newbie channel.",
#                   "locks": "control:perm(Wizards);listen:all();send:all()"},
#                   {"key": "Corinth",
#                    "aliases": "ct",
#                   "desc": "Public newbie channel.",
#                   "locks": "control:perm(Wizards);listen:all();send:all()"},
#                   {"key": "Rage",
#                    "aliases": "rt",
#                   "desc": "Public newbie channel.",
#                   "locks": "control:perm(Wizards);listen:all();send:all()"}
#                   ]

# Newbie starting location.
START_LOCATION = "#19"

# Game time modifier:
TIME_FACTOR = 6
TIME_GAME_EPOCH = 1499584913
TIME_UNITS = {
    "sec": 1,
    "min": 60,
    "hr": 60 * 60,
    "hour": 60 * 60,
    "day": 60 * 60 * 24,
    #"week": 60 * 60 * 24 * 7,
    "month": 60 * 60 * 24 * 7 * 4,
    "yr": 60 * 60 * 24 * 7 * 4 * 12,
    "year": 60 * 60 * 24 * 7 * 4 * 12 }

COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print "secret_settings.py file not found or failed to import."


######################################################################
# IRC Settings
######################################################################
IRC_ENABLED = False

# Prototype location for items, NPCs etc.
PROTOTYPE_MODULES = ["world.prototypes"]