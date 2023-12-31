alb = {
    'Armsman': 0xFF0000,
    'Cabalist': 0xFF0000,
    'Cleric': 0xFF0000,
    'Friar': 0xFF0000,
    'Heretic': 0xFF0000,
    'Infiltrator': 0xFF0000,
    'Mauler': 0xFF0000,
    'Mercenary': 0xFF0000,
    'Minstrel': 0xFF0000,
    'Necromancer': 0xFF0000,
    'Paladin': 0xFF0000,
    'Reaver': 0xFF0000,
    'Scout': 0xFF0000,
    'Sorcerer': 0xFF0000,
    'Theurgist': 0xFF0000,
    'Wizard': 0xFF0000,
}

# 0x00ff00
hib = {
    'Animist': 0x00FF00,
    'Bainshee': 0x00FF00,
    'Bard': 0x00FF00,
    'Blademaster': 0x00FF00,
    'Champion': 0x00FF00,
    'Druid': 0x00FF00,
    'Eldritch': 0x00FF00,
    'Enchanter': 0x00FF00,
    'Hero': 0x00FF00,
    'Mauler': 0x00FF00,
    'Mentalist': 0x00FF00,
    'Nightshade': 0x00FF00,
    'Ranger': 0x00FF00,
    'Valewalker': 0x00FF00,
    'Vampiir': 0x00FF00,
    'Warden': 0x00FF00,
}

mid = {
    'Berserker': 0x0000FF,
    'Bonedancer': 0x0000FF,
    'Healer': 0x0000FF,
    'Hunter': 0x0000FF,
    'Mauler': 0x0000FF,
    'Runemaster': 0x0000FF,
    'Savage': 0x0000FF,
    'Shadowblade': 0x0000FF,
    'Shaman': 0x0000FF,
    'Skald': 0x0000FF,
    'Spiritmaster': 0x0000FF,
    'Thane': 0x0000FF,
}

def get_color(realm, player_class):
    if player_class in alb:
        color = alb[player_class]
    elif player_class in hib:
        color = hib[player_class]
    elif player_class in mid:
        color = mid[player_class]
    else:
        color = 0x808080  # gray

    return color
