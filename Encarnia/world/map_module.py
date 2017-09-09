# -*- coding: utf-8 -*-

# We place our map into a sting here.
world_map = """\
≈≈↑↑↑↑↑∩∩
≈≈↑╔═╗↑∩∩
≈≈↑║O║↑∩∩
≈≈↑╚∞╝↑∩∩
≈≈≈↑│↑∩∩∩
≈≈O─O─O⌂∩
≈≈≈↑│↑∩∩∩
≈≈↑▲O▲↑∩∩
≈≈↑↑▲↑↑∩∩
≈≈↑↑↑↑↑∩∩
"""

# This turns our map string into a list of rows. Because python
# allows us to treat strings as a list of characters, we can access
# those characters with world_map[5][5] where world_map[row][column].
world_map = world_map.split('\n')

# This allows UTF-8 charcters to be handled cleanly.
world_map = [character.decode('UTF-8') if isinstance(character, basestring)
             else character for character in world_map]


def return_map():
    """
    This function returns the whole map
    """
    map = ""

    # For each row in our map, add it to map
    for valuey in world_map:
        map += valuey
        map += "\n"

    return map


def return_minimap(x, y, radius=2):
    """
    This function returns only part of the map.
    Returning all chars in a 2 char radius from (x,y)
    """
    map = ""

    # For each row we need, add the characters we need.
    for valuey in world_map[y - radius:y + radius + 1]:
        for valuex in valuey[x - radius:x + radius + 1]:
            map += valuex
        map += "\n"

    return map