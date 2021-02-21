import random

survivor_perks = ["Ace in the Hole","Adrenaline","Aftercare","Alert","Appraisal","Autodidact","Babysitter","Balanced Landing","Better Together","Blood Pact","Boil Over","Bond","Borrowed Time","Breakdown","Breakout",
"Buckle Up","Built to Last","Calm Spirit","Camaraderie","Dance With Me","Dark Sense","Dead Hard","Deception","Decisive Strike","Déjà Vu","Deliverance","Desperate Measures","Detective's Hunch",
"Distortion","Diversion","Empathy","Fixated","For the People","Head On","Hope","Inner Strength","Iron Will","Kindred","Leader","Left Behind","Lightweight","Lithe","Lucky Break","Mettle of Man","No Mither",
"No One Left Behind","Object of Obsession","Off the Record","Open-Handed","Pharmacy","Plunderer's Instinct","Poised","Power Struggle","Premonition","Prove Thyself","Quick & Quiet","Red Herring",
"Repressed Alliance","Resilience","Saboteur","Second Wind","Self-Care","Slippery Meat","Small Game","Sole Survivor","Solidarity","Soul Guard","Spine Chill","Sprint Burst","Stake Out","Streetwise",
"Technician","Tenacity","This Is Not Happening","Up the Ante","Unbreakable","Urban Evasion","Vigil","Visionary","Wake Up!","We'll Make It","We're Gonna Live Forever","Windows of Opportunity"]
killer_perks = ["Agitation","Bamboozle","Barbecue & Chilli","Beast of Prey","Bitter Murmur","Blood Echo","Blood Warden","Bloodhound","Brutal Strength","Corrupt Intervention","Coulrophobia","Coup de Grâce",
"Cruel Limits","Dark Devotion","Dead Man's Switch","Deathbound","Deerstalker","Discordance","Distressing","Dragon's Grip","Dying Light","Enduring","Fire Up","Forced Penance","Furtive Chase",
"Gearhead","Hangman's Trick","Hex: Blood Favour","Hex: Haunted Ground","Hex: Huntress Lullaby","Hex: Retribution","Hex: Ruin","Hex: The Third Seal","Hex: Thrill of the Hunt","Hex: Undying",
"Hoarder","I'm All Ears","Infectious Fright","Insidious","Iron Grasp","Iron Maiden","Knock Out","Lightborn","Mad Grit","Make Your Choice","Mindbreaker","Monitor & Abuse","Monstrous Shrine","Nemesis",
"Oppression","Overcharge","Overwhelming Presence","Play with Your Food","Pop Goes the Weasel","Predator","Remember Me","Save the Best for Last","Shadowborn","Sloppy Butcher","Spies from the Shadows",
"Spirit Fury","Stridor","Surge","Surveillance","Territorial Imperative","Thanatophobia","Thrilling Tremors","Tinkerer","Trail of Torment","Unnerving Presence","Unrelenting","Whispers","Zanshin Tactics"]

def get_perks(type):
    perks = []
    if type is None:
        raise Exception("You must specify killer or survivor perks")
    elif type.lower() == "survivor":
        perks = get_perks_from_list(survivor_perks)
    elif type.lower() == "killer":
        perks = get_perks_from_list(killer_perks)
    else:
        raise Exception("Only \"killer\" and \"survivor\" are valid arguments")
    return format_perks_list(perks)

def get_perks_from_list(perk_list):
    perks = []
    while len(perks) < 4:
        perk = random.choice(perk_list)
        if (perk not in perks):
            perks.append(perk)
    return sorted(perks)

def format_perks_list(perks):
    string = "";
    index = 1;
    for perk in perks:
        string += str(index) + ". " + perk + "\r\n"
        index = index + 1
    return [string]
        
    
