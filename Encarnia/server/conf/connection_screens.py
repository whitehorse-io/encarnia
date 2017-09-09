# -*- coding: utf-8 -*-
"""
Connection screen

Texts in this module will be shown to the user at login-time.

Evennia will look at global string variables (variables defined
at the "outermost" scope of this module and use it as the
connection screen. If there are more than one, Evennia will
randomize which one it displays.

The commands available to the user when the connection screen is shown
are defined in commands.default_cmdsets. UnloggedinCmdSet and the
screen is read and displayed by the unlogged-in "look" command.

"""

from django.conf import settings
from evennia import utils

CONNECTION_SCREEN = """

Welcome to |wEncarnia|n, Clash of the Fae!

|wcreate <accountname> <password>|n to create an account and make characters.

|wconnect <accountname> <password>|n to connect to an account and select characters.
                               """ \
    .format(settings.SERVERNAME, utils.get_evennia_version())
