# in a file ingame_time.py in mygame/world/

from evennia.utils import gametime
from typeclasses.rooms import Room

# Sunrise!
def at_sunrise():
    """When the sun rises, display a message in every room."""
    # Browse all rooms
    for room in Room.objects.all():
        room.msg_contents("The sun rises from the eastern horizon.")

def start_sunrise_event():
    """Schedule an sunrise event to happen every day at 6 AM."""
    script = gametime.schedule(at_sunrise, repeat=True, hour=6, min=0, sec=0)
    script.key = "at sunrise"

# noon
def at_noon():
    """Noon message."""
    # Browse all rooms
    for room in Room.objects.all():
        room.msg_contents("The sun sits high and mighty, directly above Encarnia.")

def start_noon_event():
    """Schedule a noon event to happen every day at 6 AM."""
    script = gametime.schedule(at_noon, repeat=True, hour=12, min=0, sec=0)
    script.key = "at noon"

# sunset
def at_sunset():
    """Sunset message."""
    # Browse all rooms
    for room in Room.objects.all():
        room.msg_contents("The sun begins to settle into the horizon, inviting Lady Moon to take his place.")

def start_sunset_event():
    """Schedule sunset."""
    script = gametime.schedule(at_sunset, repeat=True, hour=17, min=0, sec=0)
    script.key = "at sunset"

# night
def at_nightstart():
    """nightstart event."""
    # Browse all rooms
    for room in Room.objects.all():
        room.msg_contents("The last of the sun's light has disappeared; it is now night.")

def start_nightstart_event():
    """Schedule nightstart event to happen every day at 6 AM."""
    script = gametime.schedule(at_nightstart, repeat=True, hour=20, min=0, sec=0)
    script.key = "at nightstart"

#midnight stars
def at_midnight():
    """midnight event message."""
# Browse all rooms
    for room in Room.objects.all():
        room.msg_contents("Thousands of stars twinkle in the clear midnight sky.")

def start_midnight_event():
    """Schedule a midnight event message to happen every day at 6 AM."""
    script = gametime.schedule(at_midnight, repeat=True, hour=0, min=0, sec=0)
    script.key = "at midnight"