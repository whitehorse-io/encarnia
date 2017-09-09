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
                                       |g..
                                    ,o"\"""o
                                 ,o$"     o
    |rAmrall|n,|g                   ,o$$$
    |nBitches!|g                ,o$$$'
                          ,o$"o$'
                        ,o$$"$"'
                     ,o$"$o"$"'
                  ,oo$"$"$"$"$$`,                  ,oooo$$$$$$$$oooooo.
               ,o$$$"$"$"$"$"$"o$`..             ,$o$"$$"$"`oo.o
            ,oo$$$o"$"$"$"$  $"$$$"$`o        ,o$$"o$$$o$'`o
         ,o$"$"$o$"$"$"$  $"$$o$$o $$o`o   ,$$$$$o$"$$o'$
       ,o"$$"'  `$"$o$" o$o$o"  $$$o$o$oo"$$$o$"$$"$o"'$
    ,o$"'        `"$ "$$o$$" $"$o$o$$"$o$$o$o$o"$"$"`""o'
  ,o$'          o$ `"$"$o "$o$$o$$$"$$$o"$o$$o"$$$    `$$
 ,o'           (     `" o$"$o"$o$$$"$o$"$"$o$"$$"$ooo|  ``
$"$             `    (   `"o$$"$o$o$$ "o$o"   $o$o"$"$    )
(  `                   `    `o$"$$o$" "o$$     "o /|"$o"
`     |WArt By|g                 `$o$$$$"" o$      "o$\|"$o'
      |W-Darren Hall-|g          `$o"$"$ $ "       `"$"$o$
                              "$$"$$ "oo         ,$""$
                              $"$o$$""o"          ,o$"$
                              $$"$$"$ "o           `,",
                      ,oo$oo$$$$$$"$o$$$ ""o
                 ,o$$"o"o$o$$o$$$"$o$$oo"oo      |wconnect <accountname> <password>|g
               ,$"oo"$$$$o$$$$"$$$o"o$o"o"$o o   |wcreate  <accountname> <password>|g
              ,$$$""$$o$,      `$$$$"$$$o""$o $o
              $o$o$"$,          `$o$"$o$o"$$o$ $$o
             $$$o"o$$           ,$$$$o$$o"$"$$ $o$$oo      ,
             "$o$$$ $`.        ,"$$o$"o$""$$$$ `"$o$$oo    `o
             `$o$o$"$o$o`.  ,.$$"$o$$"$$"o$$$$   `$o$$ooo    $$ooooooo
               `$o$"$o"$"$$"$$"$"$$o$$o"$$o"        `"$o$o            `"o
                  `$$"$"$o$$o$"$$"$ $$$  $ "           `$"$o            `o
                     `$$"o$o"$o"$o$ "  o $$$o            `$$"o          ,$
                        (" ""$""\"     o"" "o$o             `$$ooo     ,o$$
                             $$""\"o   (   "$o$$$"o            `$o$$$o$"$'
                               ) ) )           )  ) )            ` "'
                               """ \
    .format(settings.SERVERNAME, utils.get_evennia_version())
