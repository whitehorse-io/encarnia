from evennia.contrib import custom_gametime

from commands.command import Command

class CmdTime(Command):

    """
    Display the time.

    Syntax:
        time

    """

    key = "time"
    locks = "cmd:all()"

    def func(self):
        """Execute the time command."""
        # Get the absolute game time
        # unknown, year, month, day, hour, min, sec = custom_gametime.custom_gametime(absolute=True)
        # string = "unknown: %s, year: %s, month: %s, day: %s, hour: %s, min: %s, sec: %s" % (unknown, year, month, day, hour, min, sec)
        # self.caller.msg(string)

        # Get the absolute game time
        year, month, day, hour, min, sec = custom_gametime.custom_gametime(absolute=True)
        #string = "We are in year {year}, day {day}, month {month}."
        #string += "\nIt's {hour:02}:{min:02}:{sec:02}."
        #self.msg(string.format(year=year, month=month, day=day,
                 #hour=hour, min=min, sec=sec))

        #self.caller.msg("You estimate that it's about %s hours in Encarnia." % hour)

        #self.caller.msg("Year: %s, Month: %s, Day: %s, Hour: %s, min: %s, sec: %s." % (year, month, day, hour, min, sec))

        hour = int(hour)

        this_month = "Omeo"
        season = "winter"

        if month == 1:
            this_month = "Velis"
            season = "winter"
        elif month == 2:
            this_month = "Delfas"
            season = "winter"
        elif month == 3:
            this_month = "Flyrnio"
            season = "spring"
        elif month == 4:
            this_month = "Ultera"
            season = "spring"
        elif month == 5:
            this_month = "Magna"
            season = "spring"
        elif month == 6:
            this_month = "Altas"
            season = "summer"
        elif month == 7:
            this_month = "Helios"
            season = "summer"
        elif month == 8:
            this_month = "Icarus"
            season = "summer"
        elif month == 9:
            this_month = "Yarnos"
            season = "fall"
        elif month == 10:
            this_month = "Demio"
            season = "fall"
        elif month == 11:
            this_month = "Servia"
            season = "fall"
        elif month == 12:
            this_month = "Omeo"
            season = "winter"

        day_suffix = "th"

        if day == 1:
            day_suffix = "st"
        elif day == 2:
            day_suffix = "nd"
        elif day == 3:
            day_suffix = "rd"
        elif day == 21:
            day_suffix = "st"
        elif day == 22:
            day_suffix = "nd"
        elif day == 23:
            day_suffix = "rd"

        self.caller.msg("It is the %s%s day of %s, in the %s of the year %s AC." % (day, day_suffix, this_month, season, year))

        if hour == 0:
            self.caller.msg("It's midnight in Encarnia.")
        elif 0 < hour <= 5:
            self.caller.msg("It's past midnight in Encarnia.")
        elif 5 < hour <= 7:
            self.caller.msg("It's early morning in Encarnia.")
        elif 7 < hour <= 11:
            self.caller.msg("It's morning in Encarnia.")
        elif 11 < hour < 12:
            self.caller.msg("It's almost high noon in Encarnia.")
        elif hour == 12:
            self.caller.msg("It's high noon in Encarnia.")
        elif 12 < hour <= 13:
            self.caller.msg("It's just after noon in Encarnia.")
        elif 13 < hour <= 15:
            self.caller.msg("It's afternoon in Encarnia.")
        elif 15 < hour <= 17:
            self.caller.msg("It's getting on towards the evening in Encarnia.")
        elif 17 < hour <= 19:
            self.caller.msg("It's evening in Encarnia.")
        elif 19 < hour <= 22:
            self.caller.msg("It's night in Encarnia.")
        elif 22 < hour <= 23:
            self.caller.msg("It's late night in Encarnia.")
        else:
            self.caller.msg("It's almost midnight in Encarnia.")