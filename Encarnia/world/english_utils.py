nonvowel_exceptions = {"historic", "honor", "hour", "honest", "habitual", "herb"}
vowel_exceptions = {"union", "united", "unicorn", "used", "one", "university", "unicycle", "universal", "unit", "usuability", "ewe", "used"}

# Return if it needs an or a in front
def iart(word, obj = False):
    # Check if it needs a name.
    if obj:
        word = word.name
        
    if word in vowel_exceptions:
        return "a " + word
    if word[0] in "aeiIou":
        return "an " + word
    elif word in nonvowel_exceptions:
        return "an " + word
    else:
        return "a " + word

# Return a list with iart added to each item.
def iart_list(inlist, endsep="and", obj = False):

    if not endsep:
        endsep = ","
    else:
        endsep = " " + endsep
    if not inlist:
        return ""
    if len(inlist) == 1:
        return inlist[0]

    english_list = []
    for word in inlist:
        english_list.append(word)
        
    return ", ".join(str(v) for v in english_list[:-1]) + "%s %s" % (endsep, english_list[-1])

def possessive(word):
    word = str(word)

    if word.endswith('s'):
        word = word + '\''
    else:
        word = word + '\'s'

    return word